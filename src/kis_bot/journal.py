import csv
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass
class TradeRecord:
    symbol: str; entry: float; exit: float; quantity: int; entry_time: str; exit_time: str
    initial_stop: float; final_stop: float; exit_reason: str; commission: float = 0
    tax: float = 0; slippage: float = 0; gross_pnl: float = 0; net_pnl: float = 0
    mae: float = 0; mfe: float = 0; holding_minutes: int = 0; entry_score: float = 0

class TradeJournal:
    def __init__(self, path: str = 'data/trades.csv'): self.path = Path(path)
    def append(self, record: TradeRecord) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        exists = self.path.exists()
        with self.path.open('a', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=asdict(record).keys())
            if not exists: w.writeheader()
            w.writerow(asdict(record))
