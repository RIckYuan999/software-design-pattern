from __future__ import annotations
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class Attributes:
    hp: int
    mp: int
    str_val: int

    def modify_hp(self, amount: int) -> Attributes:
        new_hp = max(0, self.hp + amount)
        return replace(self, hp=new_hp)

    def modify_mp(self, amount: int) -> Attributes:
        new_mp = max(0, self.mp + amount)
        return replace(self, mp=new_mp)