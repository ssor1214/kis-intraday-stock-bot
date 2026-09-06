"""External-data boundaries. Parsers are pure; network adapters can be replaced/tested independently."""
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

@dataclass(frozen=True)
class SupplySnapshot:
    symbol: str; foreign: float=0; institution: float=0; program: float=0
    sector: str=''; theme: str=''; risk_flags: frozenset[str]=frozenset()

class UniverseSource(Protocol):
    def instruments(self) -> list[dict]: ...
class FlowSource(Protocol):
    def flow(self, symbol: str) -> dict: ...
class NewsSource(Protocol):
    def news(self, symbol: str, since: datetime) -> list[dict]: ...

def parse_instruments(rows: list[dict]) -> list[dict]:
    return [{'symbol': str(r.get('stck_shrn_iscd') or r.get('symbol','')).zfill(6),
             'name': r.get('hts_kor_isnm', r.get('name','')), 'market': r.get('market',''),
             'price': float(r.get('stck_prpr', r.get('price',0)) or 0),
             'avg_turnover': float(r.get('acml_tr_pbmn', r.get('avg_turnover',0)) or 0),
             'flags': frozenset(r.get('flags', ())), 'is_etf': bool(r.get('is_etf',False)),
             'is_spac': bool(r.get('is_spac',False))} for r in rows if r.get('stck_shrn_iscd', r.get('symbol'))]

def parse_flow(row: dict) -> dict:
    return {'foreign': float(row.get('frgn_ntby_qty', row.get('foreign',0)) or 0),
            'institution': float(row.get('orgn_ntby_qty', row.get('institution',0)) or 0),
            'program': float(row.get('prgm_ntby_qty', row.get('program',0)) or 0)}

def parse_risk_flags(row: dict) -> frozenset[str]:
    return frozenset(x for x in row.get('risk_flags', []) if x)
