from datetime import datetime, timezone
from kis_bot.universe import Instrument, build_universe
from kis_bot.indicators import ema, vwap, atr
from kis_bot.catalyst import Catalyst
from kis_bot.ranking import rank_candidates
def test_universe_and_indicators():
    xs=[Instrument('A','A','KOSPI',10000,2e8),Instrument('B','B','KOSPI',2000,2e8)]
    assert len(build_universe(xs))==1 and ema([1,2,3],2)>2 and vwap([10,20],[1,1])==15 and atr([11,12],[9,10],[10,11])>0
def test_catalyst_and_ranking():
    c=Catalyst('A',datetime.now(timezone.utc),1,1); assert c.score()>90
    assert rank_candidates([{'score':2,'value':1},{'score':5,'value':1}],1_500_000)[0]['score']==5
