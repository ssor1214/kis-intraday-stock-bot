from kis_bot.exposure import allowed_exposure, policy
from kis_bot.safety import SafetySnapshot, trade_allowed
from kis_bot.strategy import Features, entry_score, momentum_pullback_entry
from kis_bot.state import SymbolState, transition

def test_exposure_policy():
    assert policy(1_500_000).max_total == 1.0
    assert allowed_exposure(1_500_000, expectancy=-.01) == .5

def test_safety_and_strategy():
    assert not trade_allowed(SafetySnapshot(flags=frozenset({'ETF'}), avg_turnover=1e9))
    f = Features(100,100,100,100,100,100,100,True,True,True,True)
    assert entry_score(f) == 100 and momentum_pullback_entry(f)

def test_state_transition():
    assert transition(SymbolState.DISCOVERED, SymbolState.WATCHING) == SymbolState.WATCHING
