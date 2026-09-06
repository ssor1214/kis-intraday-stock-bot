import pytest
from kis_bot.live_execution import build_cancel_request, kill_switch
def test_cancel_and_kill_switch():
    r=build_cancel_request('123',2,'k','s','12345678','t',mock=False)
    assert r.tr_id=='TTTT0803U' and r.body['ORGN_ODNO']=='123'
    assert kill_switch(-100000,10_000_000) and not kill_switch(-99999,10_000_000)
    with pytest.raises(ValueError): build_cancel_request('',1,'k','s','12345678','t')
