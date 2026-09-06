import json
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from kis_bot.config import Settings
from kis_bot.kis_api import KisClient

def main() -> int:
    symbol = os.getenv('KIS_VERIFY_SYMBOL', '005930')
    try:
        client = KisClient(Settings())
        client.authenticate()
        print('OAuth: OK')
        quote = client.quote(symbol)
        print('Quote: OK', quote.get('rt_cd', 'unknown'))
        balance = client.balance()
        print('Balance: OK', balance.get('rt_cd', 'unknown'))
        print(json.dumps({'symbol': symbol, 'quote_code': quote.get('rt_cd'), 'balance_code': balance.get('rt_cd')}, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(f'KIS verification failed: {type(exc).__name__}: {exc}', file=sys.stderr)
        return 1

if __name__ == '__main__': raise SystemExit(main())
