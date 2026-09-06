"""Live execution preparation. Network submission stays explicitly disabled."""
from dataclasses import dataclass
from .broker import Order

@dataclass(frozen=True)
class OrderRequest:
    tr_id: str; body: dict; headers: dict

def build_order_request(order: Order, app_key: str, app_secret: str, account_no: str, token: str, mock=False) -> OrderRequest:
    if order.side not in {'BUY','SELL'} or order.quantity <= 0 or order.price <= 0: raise ValueError('invalid order')
    tr_id = ('VTTC0802U' if mock else 'TTTC0802U') if order.side == 'BUY' else ('VTTC0801U' if mock else 'TTTC0801U')
    body={'CANO':account_no[:8], 'ACNT_PRDT_CD':'01', 'PDNO':order.symbol, 'ORD_DVSN':'00',
          'ORD_QTY':str(order.quantity), 'ORD_UNPR':str(int(order.price))}
    headers={'authorization':f'Bearer {token}','appkey':app_key,'appsecret':app_secret,'tr_id':tr_id,
             'custtype':'P','content-type':'application/json; charset=utf-8'}
    return OrderRequest(tr_id, body, headers)

def parse_order_response(payload: dict) -> str:
    if payload.get('rt_cd') not in (None, '0'):
        raise RuntimeError(f"order rejected {payload.get('msg_cd')}: {payload.get('msg1')}")
    output=payload.get('output', {})
    order_no=output.get('KRX_FWDG_ORD_ORGNO') or output.get('ODNO')
    if not order_no: raise RuntimeError('order response missing order number')
    return str(order_no)
