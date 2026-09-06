from pathlib import Path
from kis_bot.analytics import report
def test_report(tmp_path: Path):
    p=tmp_path/'t.csv'; p.write_text('net_pnl,mae,mfe\n10,-2,5\n-4,-3,2\n', encoding='utf-8')
    r=report(str(p)); assert r.trades==2 and r.wins==1 and r.net_pnl==6 and r.max_drawdown==4 and r.profit_factor==2.5
