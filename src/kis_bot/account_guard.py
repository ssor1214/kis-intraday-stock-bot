from dataclasses import dataclass

@dataclass
class ExposureManager:
    equity: float
    max_total_fraction: float = .50
    max_symbol_fraction: float = .30
    cash: float | None = None
    positions: dict[str, float] | None = None

    def __post_init__(self):
        if self.cash is None: self.cash = self.equity
        if self.positions is None: self.positions = {}
    @property
    def total_exposure(self): return sum(self.positions.values())
    def can_open(self, symbol: str, value: float) -> bool:
        current = self.positions.get(symbol, 0)
        return value > 0 and current + value <= self.equity*self.max_symbol_fraction and self.total_exposure + value <= self.equity*self.max_total_fraction and value <= self.cash
    def reserve(self, symbol: str, value: float) -> None:
        if not self.can_open(symbol, value): raise ValueError('exposure or cash limit exceeded')
        self.positions[symbol] = self.positions.get(symbol, 0) + value; self.cash -= value
    def release(self, symbol: str, value: float, proceeds: float | None = None) -> None:
        held=self.positions.get(symbol,0)
        if value > held: raise ValueError('release exceeds position exposure')
        self.positions[symbol]=held-value; self.cash += proceeds if proceeds is not None else value
