"""Deterministic paper-trading engine. It never calls a live order endpoint."""
from dataclasses import dataclass
from .broker import Broker, Order
from .costs import net_pnl, expected_net_positive
from .exits import Position, exit_reason
from .journal import TradeJournal, TradeRecord
from .risk import size_position
from .safety import SafetySnapshot, trade_allowed
from .strategy import Features, momentum_pullback_entry, entry_score

@dataclass(frozen=True)
class Tick:
    symbol: str; price: float; minute: int; features: Features
    safety: SafetySnapshot; stop: float; vwap: float | None = None
    session: str = 'MAIN'

class PaperEngine:
    def __init__(self, broker: Broker, journal: TradeJournal, equity: float = 1_500_000,
                 commission_rate: float = .00015, tax_rate: float = .002,
                 slippage_rate: float = .0005, reward_risk: float = 1.5, exposure=None):
        self.broker, self.journal, self.equity = broker, journal, equity
        self.commission_rate, self.tax_rate, self.slippage_rate = commission_rate, tax_rate, slippage_rate
        self.reward_risk = reward_risk
        self.exposure = exposure
        self.daily_net_pnl = 0.0
        self.position: Position | None = None
        self.entry_tick: Tick | None = None
        self.order_id: str | None = None

    def on_tick(self, tick: Tick) -> str:
        if self.daily_net_pnl <= -(self.equity * .01): return 'NO_TRADE_KILL_SWITCH'
        if self.position:
            reason = exit_reason(self.position, tick.price, tick.minute, tick.vwap,
                                 momentum_alive=momentum_pullback_entry(tick.features, 0), max_minutes=60)
            if reason: self._close(tick, reason)
            return reason or 'MANAGING'
        from .context import session_policy
        threshold, min_turnover = session_policy(tick.session)
        # Optional flow/news data may be delayed intraday; permit a bounded 15-point relaxation.
        threshold -= 15 if 0 < tick.features.data_quality < 1 else 0
        if tick.safety.avg_turnover < min_turnover or not trade_allowed(tick.safety) or not momentum_pullback_entry(tick.features, threshold): return 'NO_TRADE'
        sizing = size_position(self.equity, tick.price, tick.stop, self.equity * .60, cash=self.equity)
        if sizing.quantity <= 0: return 'NO_TRADE'
        value = sizing.quantity * tick.price
        if self.exposure and not self.exposure.can_open(tick.symbol, value): return 'NO_TRADE_EXPOSURE'
        target = tick.price + (tick.price - tick.stop) * self.reward_risk
        if not expected_net_positive(tick.price, target, sizing.quantity,
                                     self.commission_rate, self.tax_rate, self.slippage_rate):
            return 'COST_FILTER'
        self.order_id = self.broker.submit(Order(tick.symbol, 'BUY', sizing.quantity, tick.price))
        if self.exposure: self.exposure.reserve(tick.symbol, value)
        self.position = Position(tick.price, tick.stop, sizing.quantity, tick.minute)
        self.entry_tick = tick
        return 'POSITION_OPEN'

    def _close(self, tick: Tick, reason: str) -> None:
        assert self.position and self.entry_tick
        self.broker.submit(Order(tick.symbol, 'SELL', self.position.quantity, tick.price))
        gross = (tick.price - self.position.entry) * self.position.quantity
        net = net_pnl(self.position.entry, tick.price, self.position.quantity,
                      self.commission_rate, self.tax_rate, self.slippage_rate)
        self.journal.append(TradeRecord(tick.symbol, self.position.entry, tick.price,
            self.position.quantity, str(self.entry_tick.minute), str(tick.minute),
            self.position.stop, self.position.stop, reason,
            gross_pnl=gross, net_pnl=net, holding_minutes=tick.minute-self.position.opened_minute,
            entry_score=entry_score(self.entry_tick.features)))
        self.equity += net
        self.daily_net_pnl += net
        if self.exposure: self.exposure.release(tick.symbol, self.position.quantity * self.position.entry, self.position.quantity * tick.price)
        self.position = None; self.entry_tick = None
