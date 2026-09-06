from dataclasses import dataclass
@dataclass(frozen=True)
class MarketContext:
    session: str='MAIN'; market_score: float=0; sector_score: float=0
    def score(self): return max(0,min(100,(self.market_score+self.sector_score)/2))
