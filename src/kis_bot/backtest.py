import csv
from dataclasses import dataclass
from pathlib import Path
from .broker import MockBroker
from .journal import TradeJournal
from .paper_engine import PaperEngine, Tick
from .safety import SafetySnapshot
from .strategy import Features

@dataclass(frozen=True)
class BacktestResult:
    rows: int; orders: int; trades: int; final_equity: float

def run_csv(path: str, initial_equity: float = 10_000_000) -> BacktestResult:
    required={'symbol','price','minute','stop','turnover','score','trigger'}
    rows=list(csv.DictReader(Path(path).open(encoding='utf-8-sig')))
    if rows and not required.issubset(rows[0]): raise ValueError(f'missing columns: {sorted(required-set(rows[0]))}')
    broker=MockBroker(initial_equity); journal=TradeJournal('data/backtest_trades.csv')
    engines={}; count=0
    for row in rows:
        symbol=row['symbol']; engine=engines.setdefault(symbol, PaperEngine(broker,journal,initial_equity))
        price=float(row['price']); score=float(row['score']); trigger=row['trigger'].lower()=='true'
        f=Features(score,score,score,score,score,score,score,trigger,trigger,trigger,trigger)
        result=engine.on_tick(Tick(symbol,price,int(row['minute']),f,SafetySnapshot(avg_turnover=float(row['turnover'])),float(row['stop'])))
        if result=='POSITION_OPEN': count+=1
    return BacktestResult(len(rows),len(broker.orders),count,initial_equity)
