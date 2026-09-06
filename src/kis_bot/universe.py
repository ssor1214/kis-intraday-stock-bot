from dataclasses import dataclass
from .safety import BLOCKED_FLAGS

@dataclass(frozen=True)
class Instrument:
    symbol: str; name: str; market: str; price: float; avg_turnover: float
    flags: frozenset[str] = frozenset(); is_etf: bool = False; is_spac: bool = False

def build_universe(instruments: list[Instrument], min_price=3000, max_price=150000, min_turnover=100_000_000) -> list[Instrument]:
    return [x for x in instruments if min_price <= x.price <= max_price and x.avg_turnover >= min_turnover
            and not x.flags & BLOCKED_FLAGS and not x.is_etf and not x.is_spac]
