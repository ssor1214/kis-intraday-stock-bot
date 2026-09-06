def net_pnl(entry: float, exit: float, quantity: int, commission_rate: float,
            sell_tax_rate: float, slippage_rate: float = 0.0) -> float:
    gross = (exit - entry) * quantity
    fees = (entry + exit) * quantity * commission_rate
    tax = exit * quantity * sell_tax_rate
    slippage = (entry + exit) * quantity * slippage_rate
    return gross - fees - tax - slippage

def expected_net_positive(entry: float, expected_exit: float, quantity: int,
                          commission_rate: float, sell_tax_rate: float,
                          slippage_rate: float) -> bool:
    return net_pnl(entry, expected_exit, quantity, commission_rate,
                   sell_tax_rate, slippage_rate) > 0
