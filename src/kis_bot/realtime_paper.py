from dataclasses import dataclass, field
from .broker import MockBroker
from .journal import TradeJournal
from .market_features import MarketObservation, parse_pipe_message, to_strategy_inputs
from .paper_engine import PaperEngine, Tick
from .context import session_at
from datetime import datetime

@dataclass
class RealtimePaperRouter:
    symbols: list[str]
    journal_path: str = 'data/paper_trades.csv'
    broker: MockBroker = field(default_factory=MockBroker)

    def __post_init__(self):
        journal = TradeJournal(self.journal_path)
        self.engines = {s: PaperEngine(self.broker, journal) for s in self.symbols}
        self.previous: dict[str, float] = {}
        self.minute = 0
        self.events: list[tuple[str, str]] = []

    def on_message(self, message: str | dict) -> None:
        if not isinstance(message, str): return
        obs = parse_pipe_message(message)
        if not obs or obs.symbol not in self.engines or obs.price <= 0: return
        features, safety = to_strategy_inputs(obs, self.previous.get(obs.symbol))
        self.previous[obs.symbol] = obs.price
        self.minute += 1
        result = self.engines[obs.symbol].on_tick(Tick(obs.symbol, obs.price, self.minute, features, safety, obs.price * .99, obs.price, session_at(datetime.now().time())))
        self.events.append((obs.symbol, result))
