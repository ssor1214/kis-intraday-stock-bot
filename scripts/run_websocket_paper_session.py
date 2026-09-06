import os
import time
import websocket
from datetime import datetime, time as clock_time
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from kis_bot.config import Settings
from kis_bot.kis_websocket import KisMarketStream
from kis_bot.realtime_paper import RealtimePaperRouter

def main():
    settings = Settings(); settings.validate()
    symbols = [x.strip() for x in os.getenv('PAPER_SYMBOLS', '005930').split(',') if x.strip()]
    start = clock_time(8, 30)
    while datetime.now().time() < start:
        remaining = int((datetime.combine(datetime.today(), start) - datetime.now()).total_seconds())
        print(f'waiting for paper session start 08:30 KST ({max(0, remaining)}s)', flush=True)
        time.sleep(min(30, max(1, remaining)))
    router = RealtimePaperRouter(symbols)
    stream = KisMarketStream(settings, symbols, router.on_message, timeout=2)
    try:
        while True:
            try:
                stream.run_once()
            except websocket.WebSocketTimeoutException:
                print('waiting for KIS market data...')
                time.sleep(1)
            except websocket.WebSocketConnectionClosedException:
                print('KIS WebSocket closed; reconnecting...')
                stream.close(); time.sleep(3)
            except KeyboardInterrupt:
                print('stopping paper session...', flush=True)
                break
    finally: stream.close()
    print('paper websocket session stopped; orders=', len(router.broker.orders))

if __name__ == '__main__': main()
