from kis_bot.market_features import MarketObservation, parse_pipe_message, to_strategy_inputs

def test_parse_tick_message():
    values = ['005930','101010','70000'] + ['0'] * 20
    obs = parse_pipe_message('0|H0STCNT0|001|' + '^'.join(values))
    assert obs and obs.symbol == '005930' and obs.price == 70000

def test_microstructure_metrics():
    values = ['005930'] + ['101'] + ['0'] * 9 + ['20'] + ['0'] * 10 + ['10']
    obs = parse_pipe_message('0|H0STASP0|001|' + '^'.join(values))
    assert obs and obs.spread_bps >= 0

def test_observation_maps_to_strategy_inputs():
    f, safety = to_strategy_inputs(MarketObservation('005930', 101, 100, 200_000_000, 100, 101, 20, 10, 120), 100)
    assert f.breakout and f.liquidity == 80 and safety.spread_bps > 0
