import pytest
from kis_bot.broker import MockBroker, Order

def test_unowned_sell_is_rejected():
    with pytest.raises(ValueError, match="insufficient position"):
        MockBroker().submit(Order("A", "SELL", 1, 100))

def test_oversell_is_rejected_and_position_is_preserved():
    broker = MockBroker(); broker.submit(Order("A", "BUY", 1, 100))
    with pytest.raises(ValueError, match="insufficient position"):
        broker.submit(Order("A", "SELL", 2, 100))
    assert broker.positions["A"] == 1

def test_cash_limit_and_accounting():
    broker = MockBroker(cash=1_000)
    with pytest.raises(ValueError, match="insufficient mock cash"):
        broker.submit(Order("A", "BUY", 11, 100))
    broker.submit(Order("A", "BUY", 2, 100)); broker.submit(Order("A", "SELL", 1, 110))
    assert broker.cash == 910 and broker.positions["A"] == 1

def test_invalid_side_is_rejected():
    with pytest.raises(ValueError, match="side"):
        MockBroker().submit(Order("A", "SHORT", 1, 100))
