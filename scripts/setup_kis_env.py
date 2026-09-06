"""Interactively create a local .env with separate KIS mock/live credentials."""
from getpass import getpass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def ask(label: str, secret: bool = False) -> str:
    value = getpass(label + ": ") if secret else input(label + ": ")
    return value.strip()

def main() -> None:
    print("KIS credentials are written only to .env (ignored by git).")
    mock_key = ask("Mock APP KEY")
    mock_secret = ask("Mock APP SECRET", True)
    mock_account = ask("Mock account number (8 digits)")
    live_key = ask("Live APP KEY (leave blank to keep disabled)")
    live_secret = ask("Live APP SECRET", True) if live_key else ""
    live_account = ask("Live account number (8 digits)") if live_key else ""
    text = f'''KIS_MODE=mock
KIS_MOCK_APP_KEY={mock_key}
KIS_MOCK_APP_SECRET={mock_secret}
KIS_MOCK_ACCOUNT_NO={mock_account}
KIS_LIVE_APP_KEY={live_key}
KIS_LIVE_APP_SECRET={live_secret}
KIS_LIVE_ACCOUNT_NO={live_account}
KIS_PRODUCT_CODE=01
STRATEGY_CAPITAL=1500000
MAX_RISK_PER_TRADE=0.003
MAX_DAILY_LOSS=0.01
LIVE_TRADING_ENABLED=false
'''
    (ROOT / ".env").write_text(text, encoding="utf-8")
    print(f"Saved {ROOT / '.env'}; mode remains mock and live trading remains disabled.")

if __name__ == "__main__":
    main()
