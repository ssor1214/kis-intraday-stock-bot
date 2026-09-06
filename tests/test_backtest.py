from pathlib import Path
from kis_bot.backtest import run_csv
def test_csv_backtest(tmp_path: Path):
    p=tmp_path/'bars.csv'; p.write_text('symbol,price,minute,stop,turnover,score,trigger\nA,100,1,99,200000000,100,true\nA,98,2,99,200000000,20,false\n',encoding='utf-8')
    r=run_csv(str(p),10000); assert r.rows==2 and r.orders==2 and r.trades==1
