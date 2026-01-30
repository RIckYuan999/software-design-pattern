from __future__ import annotations
from typing import Callable, List, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from ..model.unit import Unit

@dataclass
class UnitDiedEvent:
    dead_unit: Unit

class DomainEventBus:
    _subscribers: List[Callable[[UnitDiedEvent], None]] = []

    @classmethod
    def subscribe(cls, handler: Callable[[UnitDiedEvent], None]):
        cls._subscribers.append(handler)

    @classmethod
    def publish(cls, event: UnitDiedEvent):
        for handler in list(cls._subscribers):
            handler(event)


    @classmethod
    def reset(cls):
        cls._subscribers = []