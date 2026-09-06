from dataclasses import dataclass

@dataclass(frozen=True)
class ExposurePolicy:
    max_total: float
    max_symbol: float

def policy(equity: float) -> ExposurePolicy:
    if equity < 2_000_000: return ExposurePolicy(1.0, .60)
    if equity < 3_000_000: return ExposurePolicy(.90, .50)
    if equity < 5_000_000: return ExposurePolicy(.75, .40)
    return ExposurePolicy(.50, .30)

def performance_multiplier(expectancy: float, drawdown: float, losing_streak: int) -> float:
    if expectancy < 0 or drawdown >= .05 or losing_streak >= 3: return .50
    if expectancy < .001 or drawdown >= .03: return .70
    return 1.0

def allowed_exposure(equity: float, expectancy: float = .0, drawdown: float = 0, losing_streak: int = 0) -> float:
    p = policy(equity)
    return p.max_total * performance_multiplier(expectancy, drawdown, losing_streak)
