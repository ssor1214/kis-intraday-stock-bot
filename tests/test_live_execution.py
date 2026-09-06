import pytest
from kis_bot.broker import Order
from kis_bot.live_execution import build_order_request, parse_order_response
def test_order_payload_is_locked_to_reviewable_request():
    r=build_order_request(Order('005930','BUY',2,70000),'k','s','12345678','t',mock=False)
    assert r.tr_id=='TTTC0802U' and r.body['ORD_QTY']=='2' and r.headers['authorization']=='Bearer t'
def test_order_response():
    assert parse_order_response({'rt_cd':'0','output':{'ODNO':'123'}})=='123'
    with pytest.raises(RuntimeError): parse_order_response({'rt_cd':'1','msg1':'denied'})
