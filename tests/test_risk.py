from kis_bot.risk import can_trade, size_position

def test_position_size_respects_risk_and_capital():
    s = size_position(1_500_000, 32_000, 31_600, 600_000)
    assert s.quantity == 11
    assert s.quantity * 400 <= 4_500

def test_daily_kill_switch():
    assert not can_trade(-15_000, 1_500_000)
    assert can_trade(-14_999, 1_500_000)
