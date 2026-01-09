from enum import Enum

from src.core import Card


class Color(Enum):
    BLUE = "B"
    RED = "R"
    YELLOW = "Y"
    GREEN = "G"

class Number(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    # SKIP = "S"
    # REVERSE = "R"
    # DRAW_TWO = "D"

class UnoCard(Card):
    def __init__(self, color: Color, number: Number):
        self._color = color
        self._number = number

    @property
    def color(self):
        return self._color

    @property
    def number(self):
        return self._number

    def __str__(self):
        return f"{self._color.value}-{self._number.value}"