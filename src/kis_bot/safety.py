from dataclasses import dataclass

BLOCKED_FLAGS = frozenset({'관리종목','투자경고','투자위험','투자주의','거래정지','정리매매','상장폐지','단기과열','신규상장','우선주','SPAC','ETN','ETF'})

@dataclass(frozen=True)
class SafetySnapshot:
    flags: frozenset[str] = frozenset()
    avg_turnover: float = 0.0
    spread_bps: float = 0.0
    halted: bool = False

def trade_allowed(s: SafetySnapshot, min_avg_turnover: float = 100_000_000, max_spread_bps: float = 50) -> bool:
    return not (s.halted or s.flags & BLOCKED_FLAGS or s.avg_turnover < min_avg_turnover or s.spread_bps > max_spread_bps)
