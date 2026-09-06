from pathlib import Path
from kis_bot.broker import MockBroker
from kis_bot.journal import TradeJournal
from kis_bot.paper_engine import PaperEngine, Tick
from kis_bot.safety import SafetySnapshot
from kis_bot.strategy import Features
def test_optional_data_relaxation_preserves_short_hold_target(tmp_path: Path):
    f=Features(100,0,0,0,100,100,100,True,True,True,True,.6)
    t=Tick('A',100,1,f,SafetySnapshot(avg_turnover=1e9),99,100,'MAIN')
    assert PaperEngine(MockBroker(),TradeJournal(str(tmp_path/'t.csv'))).on_tick(t)=='POSITION_OPEN'
