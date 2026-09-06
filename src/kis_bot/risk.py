from dataclasses import dataclass
from math import floor

@dataclass(frozen=True)
class Sizing:
    quantity: int
    risk_budget: float
    capital_fit: float

def size_position(equity: float, entry: float, stop: float, target_value: float,
                  risk_fraction: float = .003, cash: float | None = None) -> Sizing:
    if entry <= 0 or stop >= entry or target_value <= 0:
        return Sizing(0, equity * risk_fraction, 0.0)
    risk_budget = equity * risk_fraction
    risk_per_share = entry - stop
    risk_qty = floor(risk_budget / risk_per_share)
    cash_qty = floor((cash if cash is not None else equity) / entry)
    capital_qty = floor(target_value / entry)
    qty = max(0, min(risk_qty, cash_qty, capital_qty))
    fit = qty * entry / target_value if target_value else 0.0
    return Sizing(qty, risk_budget, fit)

def can_trade(daily_net_pnl: float, equity: float, max_daily_loss: float = .01) -> bool:
    return daily_net_pnl > -(equity * max_daily_loss)

