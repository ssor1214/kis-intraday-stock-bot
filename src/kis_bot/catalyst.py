from dataclasses import dataclass
from datetime import datetime, timezone
@dataclass(frozen=True)
class Catalyst:
    symbol: str; published_at: datetime; sentiment: float; relevance: float; duplicate: bool=False
    def score(self, now=None):
        if self.duplicate: return 0
        age=(now or datetime.now(timezone.utc))-self.published_at
        freshness=max(0,1-age.total_seconds()/86400)
        return max(0,min(100,50+50*self.sentiment*self.relevance*freshness))
