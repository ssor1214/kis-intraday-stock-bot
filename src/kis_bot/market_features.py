"""Normalize KIS websocket messages into strategy-friendly market observations."""
from dataclasses import dataclass
from .safety import SafetySnapshot
from .strategy import Features

@dataclass(frozen=True)
class MarketObservation:
    symbol: str; price: float; volume: float = 0; turnover: float = 0
    bid_price: float = 0; ask_price: float = 0; bid_size: float = 0; ask_size: float = 0
    trade_strength: float = 0

    @property
    def spread_bps(self) -> float:
        return ((self.ask_price - self.bid_price) / self.price * 10000) if self.price and self.ask_price and self.bid_price else 0

    @property
    def imbalance(self) -> float:
        total = self.bid_size + self.ask_size
        return (self.bid_size - self.ask_size) / total if total else 0

def _f(values: list[str], index: int) -> float:
    try: return float(values[index].replace(',', ''))
    except (IndexError, ValueError, AttributeError): return 0.0

def parse_pipe_message(raw: str) -> MarketObservation | None:
    parts = raw.split('|')
    if len(parts) < 4 or parts[0] != '0': return None
    tr_id, values = parts[1], parts[3].split('^')
    if tr_id == 'H0STCNT0':
        # KIS domestic tick schema: code, time, price, signed change, ..., cumulative volume, turnover.
        return MarketObservation(values[0] if values else '', _f(values, 2), _f(values, 13), _f(values, 14), trade_strength=_f(values, 18))
    if tr_id == 'H0STASP0':
        # KIS orderbook schema has ask/bid prices followed by ask/bid sizes.
        return MarketObservation(values[0] if values else '', _f(values, 0), bid_price=_f(values, 11), ask_price=_f(values, 1), bid_size=_f(values, 21), ask_size=_f(values, 10))
    return None

def to_strategy_inputs(obs: MarketObservation, previous_price: float | None = None,
                       min_turnover: float = 100_000_000) -> tuple[Features, SafetySnapshot]:
    change = (obs.price / previous_price - 1) if previous_price else 0
    momentum = max(0, min(100, 50 + change * 10000))
    liquidity = 80 if obs.turnover >= min_turnover else 20
    orderbook = max(0, min(100, 50 + obs.imbalance * 50))
    features = Features(market=50, catalyst=0, foreign=0, program=0,
        liquidity=liquidity, chart=momentum, orderbook=orderbook,
        pullback_support=previous_price is not None,
        volume_reacceleration=obs.volume > 0,
        trade_strength_rising=obs.trade_strength > 0,
        breakout=change > 0)
    safety = SafetySnapshot(avg_turnover=obs.turnover, spread_bps=obs.spread_bps)
    return features, safety
