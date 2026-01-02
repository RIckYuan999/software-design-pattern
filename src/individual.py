import math
from dataclasses import dataclass
from enum import Enum
from typing import Set, Optional


class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

@dataclass
class Coord:
    _x: int
    _y: int

    # 計算歐幾里得距離
    def distance_to(self, other: 'Coord') -> float:
        return math.sqrt((self._x - other._x)**2 + (self._y - other._y)**2)

@dataclass
class Individual:
    _id: int
    _gender: Gender
    _age: int
    _intro: str
    _habits: Optional[Set[str]]
    _coord: Coord

    # getter
    id = property(lambda self: self._id)
    habits = property(lambda self: self._habits)
    coord = property(lambda self: self._coord)

    # constraint
    def __post_init__(self):
        if self._id <= 0:
            raise ValueError("ID must be a positive integer")
        if self._age < 18:
            raise ValueError("Age must be at least 18")
        if len(self._intro) > 200:
            raise ValueError("Intro must be less than 200 characters")
        if any(not (1 <= len(habit) <= 10) for habit in self._habits):
            raise ValueError("Each habit must be between 1 and 10 characters")

    # hashable，可做為 dict 的 key
    def __hash__(self):
        return hash(self._id)