from datetime import datetime, timedelta, timezone
from kis_bot.event_guard import EventGuard
def test_event_guard_rejects_duplicate_and_stale():
    g=EventGuard(10); now=datetime.now(timezone.utc); assert g.accept('A','1',now,now); assert not g.accept('A','1',now,now); assert not g.accept('A','2',now-timedelta(seconds=11),now)
