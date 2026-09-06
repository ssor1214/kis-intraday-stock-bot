from .exposure import policy
def rank_candidates(candidates, equity: float, current_exposure: float=0):
    cap=policy(equity).max_total*equity
    return sorted([x for x in candidates if current_exposure+x.get('value',0)<=cap], key=lambda x:x.get('score',0), reverse=True)
