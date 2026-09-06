from pathlib import Path
from kis_bot.account_guard import ExposureManager
from kis_bot.broker import MockBroker
from kis_bot.journal import TradeJournal
from kis_bot.paper_engine import PaperEngine, Tick
from kis_bot.safety import SafetySnapshot
from kis_bot.strategy import Features
def test_engine_uses_shared_exposure(tmp_path: Path):
    f=Features(100,100,100,100,100,100,100,True,True,True,True); s=SafetySnapshot(avg_turnover=1e9)
    a=ExposureManager(10_000_000); b=MockBroker(10_000_000); e=PaperEngine(b,TradeJournal(str(tmp_path/'x')),10_000_000,exposure=a)
    assert e.on_tick(Tick('A',100,1,f,s,99)) in {'POSITION_OPEN','COST_FILTER'}
