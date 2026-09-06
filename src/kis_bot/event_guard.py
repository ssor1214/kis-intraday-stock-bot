from dataclasses import dataclass
from datetime import datetime, timezone
@dataclass
class EventGuard:
    max_age_seconds: float = 10
    last_event: dict[str,str] = None
    last_time: dict[str,datetime] = None
    def __post_init__(self): self.last_event=self.last_event or {}; self.last_time=self.last_time or {}
    def accept(self, symbol: str, event_id: str, event_time: datetime, now: datetime | None = None) -> bool:
        now=now or datetime.now(timezone.utc)
        if self.last_event.get(symbol)==event_id: return False
        if event_time.tzinfo is None: event_time=event_time.replace(tzinfo=timezone.utc)
        if event_time < self.last_time.get(symbol,event_time) or (now-event_time).total_seconds()>self.max_age_seconds: return False
        self.last_event[symbol]=event_id; self.last_time[symbol]=event_time; return True
