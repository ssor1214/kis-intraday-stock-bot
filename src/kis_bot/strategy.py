from dataclasses import dataclass

@dataclass(frozen=True)
class Features:
    market: float = 0; catalyst: float = 0; foreign: float = 0; program: float = 0
    liquidity: float = 0; chart: float = 0; orderbook: float = 0
    pullback_support: bool = False; volume_reacceleration: bool = False
    trade_strength_rising: bool = False; breakout: bool = False
    data_quality: float = 1.0

def entry_score(f: Features) -> float:
    return sum((f.market*.10, f.catalyst*.15, f.foreign*.15, f.program*.10,
                f.liquidity*.15, f.chart*.15, f.orderbook*.20))

def entry_trigger(f: Features) -> bool:
    return f.breakout and f.volume_reacceleration and f.trade_strength_rising and f.pullback_support

def momentum_pullback_entry(f: Features, threshold: float = 75) -> bool:
    return entry_score(f) >= threshold and entry_trigger(f)
