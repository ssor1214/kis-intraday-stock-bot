from statistics import mean

def vwap(prices, volumes):
    return sum(p*v for p,v in zip(prices, volumes)) / sum(volumes) if prices and sum(volumes) else 0
def ema(values, period):
    if not values: return 0
    alpha=2/(period+1); result=values[0]
    for value in values[1:]: result=alpha*value+(1-alpha)*result
    return result
def atr(highs, lows, closes, period=14):
    if len(closes)<2: return 0
    tr=[max(h-l, abs(h-closes[i-1]), abs(l-closes[i-1])) for i,(h,l) in enumerate(zip(highs[1:],lows[1:]),1)]
    return mean(tr[-period:]) if tr else 0
def swing_high(values, lookback=5): return max(values[-lookback:]) if values else 0
def swing_low(values, lookback=5): return min(values[-lookback:]) if values else 0
