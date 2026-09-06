from dataclasses import dataclass
from datetime import time
@dataclass(frozen=True)
class MarketContext:
    session: str='MAIN'; market_score: float=0; sector_score: float=0
    def score(self): return max(0,min(100,(self.market_score+self.sector_score)/2))

def session_at(t: time) -> str:
    if time(8,30) <= t < time(9,0): return 'PRE'
    if time(9,0) <= t < time(15,30): return 'MAIN'
    if time(15,40) <= t <= time(20,0): return 'AFTER'
    return 'CLOSED'

def session_policy(session: str) -> tuple[float, float]:
    return {'PRE': (85, 150_000_000), 'MAIN': (75, 100_000_000), 'AFTER': (85, 200_000_000)}.get(session, (101, float('inf')))
