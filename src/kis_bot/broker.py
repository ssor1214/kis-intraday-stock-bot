from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class Order:
    symbol: str
    side: str
    quantity: int
    price: float

class Broker(Protocol):
    def submit(self, order: Order) -> str: ...

class MockBroker:
    def __init__(self): self.orders: list[Order] = []
    def submit(self, order: Order) -> str:
        if order.quantity <= 0: raise ValueError("quantity must be positive")
        self.orders.append(order)
        return f"MOCK-{len(self.orders):06d}"

class LiveBroker:
    """Placeholder: live adapter must be implemented and separately enabled."""
    def submit(self, order: Order) -> str:
        raise RuntimeError("live order adapter is intentionally locked")
