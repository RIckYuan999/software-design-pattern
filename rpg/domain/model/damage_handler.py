from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

from state import StateType

if TYPE_CHECKING:
    from .unit import Unit

class DamageResult:
    def __init__(self, damage: int, repeat: int = 1, clear_state: bool = False):
        self.damage = damage
        self.repeat = repeat
        self.clear_state = clear_state

class OnePunchHandler(ABC):
    def __init__(self, next_handler: Optional[OnePunchHandler] = None):
        self.next_handler = next_handler

    def set_next(self, handler: OnePunchHandler) -> OnePunchHandler:
        self.next_handler = handler
        return handler

    def handle(self, user: Unit, target: Unit) -> DamageResult:
        if result := self.calculate(user, target):
            return result
        
        if self.next_handler:
            return self.next_handler.handle(user, target)
        
        return DamageResult(damage=0)

    @abstractmethod
    def calculate(self, user: Unit, target: Unit) -> Optional[DamageResult]:
        pass


class HighHpHandler(OnePunchHandler):
    def calculate(self, user: Unit, target: Unit) -> Optional[DamageResult]:
        if target.hp >= 500:
            return DamageResult(damage=300)
        return None

class AbnormalStateHandler(OnePunchHandler):
    def calculate(self, user: Unit, target: Unit) -> Optional[DamageResult]:
        if target.is_in_state(StateType.ABNORMAL):
            return DamageResult(damage=80, repeat=3)
        return None

class BuffStateHandler(OnePunchHandler):
    def calculate(self, user: Unit, target: Unit) -> Optional[DamageResult]:
        if target.is_in_state(StateType.BUFF):
            return DamageResult(damage=100, clear_state=True)
        return None

class DefaultHandler(OnePunchHandler):
    def calculate(self, user: Unit, target: Unit) -> Optional[DamageResult]:
        return DamageResult(damage=100)
