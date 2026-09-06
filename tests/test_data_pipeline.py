from datetime import datetime, timezone
from kis_bot.data_pipeline import DataPipeline
class U:
    def instruments(self): return [{'symbol':'005930','name':'A','market':'KOSPI','price':70000,'avg_turnover':200000000}]
class F:
    def flow(self, symbol): return {'foreign': 1}
def test_pipeline_filters_and_merges():
    xs=DataPipeline(U(),F()).candidates(datetime.now(timezone.utc))
    assert len(xs)==1 and xs[0].flow['foreign']==1
