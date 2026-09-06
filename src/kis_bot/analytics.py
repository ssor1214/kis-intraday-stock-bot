import csv
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Performance:
    trades: int; wins: int; win_rate: float; net_pnl: float
    expectancy: float; profit_factor: float; max_drawdown: float; avg_mae: float; avg_mfe: float

def report(path: str = 'data/paper_trades.csv') -> Performance:
    rows = list(csv.DictReader(Path(path).open(encoding='utf-8'))) if Path(path).exists() else []
    pnls = [float(r.get('net_pnl',0) or 0) for r in rows]
    wins = sum(p > 0 for p in pnls); gross_profit=sum(p for p in pnls if p>0); gross_loss=-sum(p for p in pnls if p<0)
    equity=peak=drawdown=0.0
    for p in pnls:
        equity += p; peak=max(peak,equity); drawdown=max(drawdown,peak-equity)
    n=len(pnls)
    return Performance(n,wins,wins/n if n else 0,sum(pnls),sum(pnls)/n if n else 0,
        gross_profit/gross_loss if gross_loss else (float('inf') if gross_profit else 0),drawdown,
        sum(float(r.get('mae',0) or 0) for r in rows)/n if n else 0,
        sum(float(r.get('mfe',0) or 0) for r in rows)/n if n else 0)
