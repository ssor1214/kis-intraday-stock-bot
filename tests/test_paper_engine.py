from pathlib import Path
from kis_bot.broker import MockBroker
from kis_bot.journal import TradeJournal
from kis_bot.paper_engine import PaperEngine, Tick
from kis_bot.safety import SafetySnapshot
from kis_bot.strategy import Features

def test_paper_cycle(tmp_path: Path):
    f = Features(90,80,70,70,90,85,80,True,True,True,True)
    safe = SafetySnapshot(avg_turnover=1e9, spread_bps=10)
    b = MockBroker(); e = PaperEngine(b, TradeJournal(str(tmp_path/'t.csv')))
    assert e.on_tick(Tick('005930', 32000, 1, f, safe, 31600)) == 'POSITION_OPEN'
    assert e.on_tick(Tick('005930', 31500, 2, f, safe, 31600)) == 'HARD_SL'
    assert len(b.orders) == 2 and (tmp_path/'t.csv').exists()

def test_cost_filter_skips_tiny_edge(tmp_path: Path):
    f = Features(90,80,70,70,90,85,80,True,True,True,True)
    safe = SafetySnapshot(avg_turnover=1e9, spread_bps=10)
    b = MockBroker(); e = PaperEngine(b, TradeJournal(str(tmp_path/'t.csv')), reward_risk=.01)
    assert e.on_tick(Tick('005930', 32000, 1, f, safe, 31999)) == 'COST_FILTER'
    assert not b.orders
