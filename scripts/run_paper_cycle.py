from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from kis_bot.broker import MockBroker
from kis_bot.journal import TradeJournal
from kis_bot.paper_engine import PaperEngine, Tick
from kis_bot.safety import SafetySnapshot
from kis_bot.strategy import Features

def main() -> None:
    features = Features(90, 80, 70, 70, 90, 85, 80, True, True, True, True)
    safe = SafetySnapshot(avg_turnover=1_000_000_000, spread_bps=10)
    broker = MockBroker()
    engine = PaperEngine(broker, TradeJournal('data/paper_trades.csv'))
    print(engine.on_tick(Tick('005930', 32000, 1, features, safe, 31600, 32000)))
    weak = Features(20, 20, 20, 20, 20, 20, 20)
    print(engine.on_tick(Tick('005930', 31900, 5, weak, safe, 31600, 32000)))
    print('orders=', len(broker.orders), 'journal=data/paper_trades.csv')

if __name__ == '__main__': main()
