from dataclasses import dataclass

@dataclass(frozen=True)
class Position:
    entry: float; stop: float; quantity: int; opened_minute: int
    highest: float | None = None

def exit_reason(p: Position, price: float, minute: int, vwap: float | None = None,
                momentum_alive: bool = True, max_minutes: int = 60) -> str | None:
    if price <= p.stop: return 'HARD_SL'
    if minute - p.opened_minute >= max_minutes: return 'TIME_EXIT'
    if not momentum_alive or (vwap is not None and price < vwap): return 'MOMENTUM_FAILURE'
    return None

def trailing_stop(current_stop: float, candidate: float) -> float:
    return max(current_stop, candidate)
