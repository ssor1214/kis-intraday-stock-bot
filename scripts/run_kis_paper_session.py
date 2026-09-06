"""Poll KIS quotes and run the local paper engine; never submits KIS orders."""
import os, sys, time
from datetime import datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from kis_bot.config import Settings
from kis_bot.kis_api import KisClient
from kis_bot.broker import MockBroker
from kis_bot.journal import TradeJournal
from kis_bot.paper_engine import PaperEngine, Tick
from kis_bot.safety import SafetySnapshot
from kis_bot.strategy import Features

def number(payload: dict, *keys: str, default: float = 0) -> float:
    out = payload.get('output', {})
    for key in keys:
        try: return float(out.get(key, default))
        except (TypeError, ValueError): pass
    return default

def main() -> None:
    settings = Settings(); settings.validate()
    if not settings.paper_trading_active(): raise SystemExit('paper trading window has ended')
    symbols = [s.strip() for s in os.getenv('PAPER_SYMBOLS', os.getenv('PAPER_SYMBOL', '005930')).split(',') if s.strip()]
    interval = float(os.getenv('PAPER_INTERVAL_SECONDS', '30'))
    ticks = int(os.getenv('PAPER_MAX_TICKS', '20'))
    client, broker = KisClient(settings), MockBroker()
    journal = TradeJournal('data/paper_trades.csv')
    engines = {s: PaperEngine(broker, journal) for s in symbols}
    prices: dict[str, list[float]] = {s: [] for s in symbols}
    for _ in range(ticks):
        for symbol in symbols:
            payload = client.quote(symbol)
            price = number(payload, 'stck_prpr'); volume = number(payload, 'acml_vol'); turnover = number(payload, 'acml_tr_pbmn')
            if price <= 0: print('skip:', symbol, 'quote has no price'); continue
            prices[symbol].append(price)
            history = prices[symbol]
            change = (price / history[-2] - 1) if len(history) > 1 and history[-2] else 0
            momentum = max(0, min(100, 50 + change * 10000))
            features = Features(market=50, catalyst=0, foreign=0, program=0,
                liquidity=80 if turnover >= 100_000_000 else 20, chart=momentum,
                orderbook=50, pullback_support=len(history) >= 3,
                volume_reacceleration=volume > 0 and len(history) >= 3,
                trade_strength_rising=change > 0, breakout=change > 0)
            result = engines[symbol].on_tick(Tick(symbol, price, len(history), features,
                SafetySnapshot(avg_turnover=turnover, spread_bps=0), price * .99, price))
            print(datetime.now().isoformat(timespec='seconds'), symbol, price, result)
        time.sleep(interval)
    print('paper session complete; orders=', len(broker.orders), 'journal=data/paper_trades.csv')

if __name__ == '__main__': main()
