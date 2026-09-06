from datetime import time
from kis_bot.context import session_at, session_policy
def test_sessions():
    assert session_at(time(8,30))=='PRE' and session_at(time(10))=='MAIN' and session_at(time(16))=='AFTER' and session_at(time(21))=='CLOSED'
    assert session_policy('AFTER')[0] > session_policy('MAIN')[0]
