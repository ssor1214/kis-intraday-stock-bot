from dataclasses import dataclass
import os
from datetime import date
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

@dataclass(frozen=True)
class Settings:
    mode: str = os.getenv("KIS_MODE", "mock").lower()
    mock_app_key: str = os.getenv("KIS_MOCK_APP_KEY", "")
    mock_app_secret: str = os.getenv("KIS_MOCK_APP_SECRET", "")
    mock_account_no: str = os.getenv("KIS_MOCK_ACCOUNT_NO", "")
    live_app_key: str = os.getenv("KIS_LIVE_APP_KEY", "")
    live_app_secret: str = os.getenv("KIS_LIVE_APP_SECRET", "")
    live_account_no: str = os.getenv("KIS_LIVE_ACCOUNT_NO", "")
    strategy_capital: int = int(os.getenv("STRATEGY_CAPITAL", "1500000"))
    risk_per_trade: float = float(os.getenv("MAX_RISK_PER_TRADE", "0.003"))
    max_daily_loss: float = float(os.getenv("MAX_DAILY_LOSS", "0.01"))
    live_trading_enabled: bool = os.getenv("LIVE_TRADING_ENABLED", "false").lower() == "true"
    paper_trading_until: date = date.fromisoformat(os.getenv("PAPER_TRADING_UNTIL", "2099-12-31"))

    def validate(self) -> None:
        if self.mode not in {"mock", "live"}:
            raise ValueError("KIS_MODE must be mock or live")
        if self.strategy_capital <= 0 or not 0 < self.risk_per_trade <= .01:
            raise ValueError("invalid capital or risk limit")
        if self.mode == "live" and not self.live_trading_enabled:
            raise ValueError("live mode is locked; set LIVE_TRADING_ENABLED=true deliberately")
        key = (self.mock_app_key, self.mock_app_secret, self.mock_account_no) if self.mode == "mock" else (self.live_app_key, self.live_app_secret, self.live_account_no)
        if any(not value.strip() for value in key):
            raise ValueError(f"missing {self.mode} KIS credentials")
        account = self.account_no.replace('-', '').replace(' ', '')
        if len(account) < 8 or not account[:8].isdigit():
            raise ValueError('KIS account number must start with 8 digits')

    def paper_trading_active(self, today: date | None = None) -> bool:
        return self.mode == "mock" and (today or date.today()) <= self.paper_trading_until

    @property
    def app_key(self) -> str:
        return self.mock_app_key if self.mode == "mock" else self.live_app_key

    @property
    def app_secret(self) -> str:
        return self.mock_app_secret if self.mode == "mock" else self.live_app_secret

    @property
    def account_no(self) -> str:
        value = self.mock_account_no if self.mode == "mock" else self.live_account_no
        return value.replace('-', '').replace(' ', '')
