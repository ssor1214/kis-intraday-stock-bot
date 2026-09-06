from kis_bot.realtime_paper import RealtimePaperRouter

def msg(price, volume='100', turnover='200000000'):
    values = ['005930','101010',str(price)] + ['0']*10 + [volume, turnover] + ['0']*5
    return '0|H0STCNT0|001|' + '^'.join(values)

def test_websocket_to_paper_router():
    r = RealtimePaperRouter(['005930'], 'data/test_realtime.csv')
    r.on_message(msg(32000)); r.on_message(msg(32100)); r.on_message(msg(31500))
    assert len(r.events) == 3
    assert not any(order.side == 'SELL' for order in r.broker.orders) or len(r.broker.orders) >= 2
