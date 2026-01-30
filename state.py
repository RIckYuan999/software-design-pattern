from __future__ import annotations
import abc
from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rpg.domain.model.unit import Unit


class StateType(Enum):
    NORMAL = auto()
    ABNORMAL = auto()  # 中毒, 石化
    BUFF = auto()      # 受到鼓舞


class StatusEffect(abc.ABC):
    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def type(self) -> StateType:
        pass

    @property
    def duration(self) -> int:
        return 0

    @abc.abstractmethod
    def on_turn_start(self, unit: Unit) -> bool:
        pass

    def modify_damage(self, damage: int) -> int:
        return damage

class NormalState(StatusEffect):
    name = "正常"
    type = StateType.NORMAL

    def on_turn_start(self, unit: Unit) -> bool:
        return True


class PoisonedState(StatusEffect):
    name = "中毒"
    type = StateType.ABNORMAL

    @property
    def duration(self) -> int:
        return 3

    def on_turn_start(self, unit: Unit) -> bool:
        unit.take_damage(30)
        return unit.is_alive()


class PetrochemicalState(StatusEffect):
    name = "石化"
    type = StateType.ABNORMAL

    @property
    def duration(self) -> int:
        return 3

    def on_turn_start(self, unit: Unit) -> bool:
        return False


class CheerupState(StatusEffect):
    name = "受到鼓舞"
    type = StateType.BUFF

    @property
    def duration(self) -> int:
        return 3

    def on_turn_start(self, unit: Unit) -> bool:
        return True

    def modify_damage(self, damage: int) -> int:
        return damage + 50