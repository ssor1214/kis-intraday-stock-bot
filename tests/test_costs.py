from kis_bot.costs import expected_net_positive, net_pnl

def test_costs_are_included():
    assert net_pnl(10_000, 10_100, 10, .00015, .002, .0005) < 1_000
    assert expected_net_positive(10_000, 10_100, 10, .00015, .002, .0005)
