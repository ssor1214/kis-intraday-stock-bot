from kis_bot.kis_websocket import KisMarketStream

def test_stream_dispatches_json_without_network():
    seen = []
    stream = KisMarketStream.__new__(KisMarketStream)
    stream.on_message = seen.append
    stream.ws = type('W', (), {'recv': lambda self: '{"header":{"tr_id":"H0STCNT0"}}'})()
    result = KisMarketStream.run_once(stream)
    assert result['header']['tr_id'] == 'H0STCNT0' and len(seen) == 1
