import argparse
from kis_bot.backtest import run_csv
p=argparse.ArgumentParser(); p.add_argument('csv_path'); a=p.parse_args(); print(run_csv(a.csv_path))
