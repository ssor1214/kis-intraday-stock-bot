import pytest
from kis_bot.broker import MockBroker
from kis_bot.execution import OrderIntent, OrderStatus, PaperExecution, LiveExecution
def intent(): return OrderIntent('A','BUY',1,100,99,102,'MAIN',80,1,1)
def test_shared_intent_paper_path():
    status, oid=PaperExecution(MockBroker()).submit(intent()); assert status==OrderStatus.FILLED and oid
def test_live_path_stays_locked():
    with pytest.raises(PermissionError): LiveExecution().submit(intent())
def test_cash_strategy_rejects_short_intent():
    with pytest.raises(ValueError): PaperExecution(MockBroker()).submit(OrderIntent('A','SELL',1,100,99,102,'MAIN',80,1,1))
