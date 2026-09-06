from dataclasses import dataclass
from enum import StrEnum
from .broker import MockBroker, Order

class OrderStatus(StrEnum): CREATED='CREATED'; SUBMITTED='SUBMITTED'; FILLED='FILLED'; REJECTED='REJECTED'; CANCELLED='CANCELLED'

@dataclass(frozen=True)
class OrderIntent:
    symbol: str; side: str; quantity: int; signal_price: float; stop_price: float
    target_price: float; session: str; entry_score: float; expected_net_pnl: float; max_risk: float

def validate_intent(i: OrderIntent) -> None:
    if i.side != 'BUY': raise ValueError('cash strategy accepts BUY intents only')
    if i.quantity <= 0 or i.signal_price <= 0 or i.stop_price >= i.signal_price: raise ValueError('invalid order intent')
    if i.expected_net_pnl <= 0 or i.max_risk <= 0: raise ValueError('intent must have positive edge and risk')

class PaperExecution:
    def __init__(self, broker: MockBroker): self.broker=broker
    def submit(self, intent: OrderIntent) -> tuple[OrderStatus,str]:
        validate_intent(intent)
        oid=self.broker.submit(Order(intent.symbol,'BUY',intent.quantity,intent.signal_price))
        return OrderStatus.FILLED, oid

class LiveExecution:
    def submit(self, intent: OrderIntent):
        validate_intent(intent)
        raise PermissionError('live execution is locked pending order/fill validation')
