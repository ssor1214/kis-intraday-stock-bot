from dataclasses import dataclass
from .data_sources import FlowSource, NewsSource, UniverseSource, parse_flow, parse_instruments, parse_risk_flags
from .universe import Instrument, build_universe

@dataclass(frozen=True)
class Candidate:
    instrument: Instrument; flow: dict; sector: str; theme: str; news: list[dict]

class DataPipeline:
    def __init__(self, universe: UniverseSource, flows: FlowSource | None = None,
                 news: NewsSource | None = None):
        self.universe_source, self.flow_source, self.news_source = universe, flows, news

    def candidates(self, since, *, min_price=3000, max_price=150000, min_turnover=100_000_000) -> list[Candidate]:
        raw = self.universe_source.instruments()
        normalized = parse_instruments(raw)
        instruments = [Instrument(x['symbol'], x['name'], x['market'], x['price'], x['avg_turnover'],
                                  parse_risk_flags(x), x['is_etf'], x['is_spac']) for x in normalized]
        allowed = build_universe(instruments, min_price, max_price, min_turnover)
        result=[]
        for instrument in allowed:
            flow = parse_flow(self.flow_source.flow(instrument.symbol)) if self.flow_source else {}
            articles = self.news_source.news(instrument.symbol, since) if self.news_source else []
            result.append(Candidate(instrument, flow, '', '', articles))
        return result
