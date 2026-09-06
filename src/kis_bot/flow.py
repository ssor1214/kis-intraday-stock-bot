from dataclasses import dataclass
@dataclass(frozen=True)
class Flow:
    foreign: float=0; institution: float=0; program: float=0
    foreign_momentum: float=0; institution_momentum: float=0; program_momentum: float=0
    @property
    def score(self): return max(0,min(100,50+(self.foreign_momentum+self.institution_momentum+self.program_momentum)*10))
