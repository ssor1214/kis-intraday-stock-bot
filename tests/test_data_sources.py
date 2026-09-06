from kis_bot.data_sources import parse_flow, parse_instruments, parse_risk_flags
def test_data_parsers():
    xs=parse_instruments([{'stck_shrn_iscd':'5930','stck_prpr':'70000','acml_tr_pbmn':'100'}])
    assert xs[0]['symbol']=='005930' and xs[0]['price']==70000
    assert parse_flow({'frgn_ntby_qty':'2'})['foreign']==2
    assert '투자경고' in parse_risk_flags({'risk_flags':['투자경고']})
