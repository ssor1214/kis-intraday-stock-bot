from enum import StrEnum

class SymbolState(StrEnum):
    DISCOVERED = "DISCOVERED"
    WATCHING = "WATCHING"
    ARMED = "ARMED"
    ENTRY_PENDING = "ENTRY_PENDING"
    POSITION_OPEN = "POSITION_OPEN"
    MANAGING = "MANAGING"
    EXIT_PENDING = "EXIT_PENDING"
    EXITED = "EXITED"
    COOLDOWN = "COOLDOWN"

TRANSITIONS = {
    SymbolState.DISCOVERED: {SymbolState.WATCHING},
    SymbolState.WATCHING: {SymbolState.ARMED, SymbolState.COOLDOWN},
    SymbolState.ARMED: {SymbolState.ENTRY_PENDING, SymbolState.COOLDOWN},
    SymbolState.ENTRY_PENDING: {SymbolState.POSITION_OPEN, SymbolState.COOLDOWN},
    SymbolState.POSITION_OPEN: {SymbolState.MANAGING, SymbolState.EXIT_PENDING},
    SymbolState.MANAGING: {SymbolState.EXIT_PENDING},
    SymbolState.EXIT_PENDING: {SymbolState.EXITED},
    SymbolState.EXITED: {SymbolState.COOLDOWN},
    SymbolState.COOLDOWN: {SymbolState.WATCHING},
}

def transition(current: SymbolState, target: SymbolState) -> SymbolState:
    if target not in TRANSITIONS.get(current, set()):
        raise ValueError(f'invalid transition: {current} -> {target}')
    return target
