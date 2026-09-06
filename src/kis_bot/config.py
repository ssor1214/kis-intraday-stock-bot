from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    mode: str = os.getenv("KIS_MODE", "mock").lower()
    strategy_capital: int = int(os.getenv("STRATEGY_CAPITAL", "1500000"))
    risk_per_trade: float = float(os.getenv("MAX_RISK_PER_TRADE", "0.003"))
    max_daily_loss: float = float(os.getenv("MAX_DAILY_LOSS", "0.01"))
    live_trading_enabled: bool = os.getenv("LIVE_TRADING_ENABLED", "false").lower() == "true"

    def validate(self) -> None:
        if self.mode not in {"mock", "live"}:
            raise ValueError("KIS_MODE must be mock or live")
        if self.strategy_capital <= 0 or not 0 < self.risk_per_trade <= .01:
            raise ValueError("invalid capital or risk limit")
        if self.mode == "live" and not self.live_trading_enabled:
            raise ValueError("live mode is locked; set LIVE_TRADING_ENABLED=true deliberately")

