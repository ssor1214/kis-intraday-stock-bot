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
    def __init__(self, cash: float = 1_500_000):
        self.orders: list[Order] = []
        self.cash = cash
        self.positions: dict[str, int] = {}
    def submit(self, order: Order) -> str:
        if order.side not in {"BUY", "SELL"}:
            raise ValueError("side must be BUY or SELL")
        if order.quantity <= 0 or order.price <= 0:
            raise ValueError("quantity and price must be positive")
        value = order.quantity * order.price
        if order.side == "BUY":
            if value > self.cash:
                raise ValueError("insufficient mock cash")
            self.cash -= value
            self.positions[order.symbol] = self.positions.get(order.symbol, 0) + order.quantity
        else:
            held = self.positions.get(order.symbol, 0)
            if held < order.quantity:
                raise ValueError("insufficient position to sell")
            self.positions[order.symbol] = held - order.quantity
            self.cash += value
        self.orders.append(order)
        return f"MOCK-{len(self.orders):06d}"

class LiveBroker:
    """Placeholder: live adapter must be implemented and separately enabled."""
    def submit(self, order: Order) -> str:
        raise RuntimeError("live order adapter is intentionally locked")
