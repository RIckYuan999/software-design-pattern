from abc import ABC, abstractmethod
from typing import List, Optional

from .model import Card, RANK_ORDER


class CardPattern(ABC):
    name: str = None

    def __init__(self, cards: List[Card]):
        self.cards = cards

    @property
    def value(self) -> int:
        return self.cards[-1].sort_idx

    def __gt__(self, other):
        if not isinstance(other, type(self)):
            raise ValueError(f"不同牌型無法比較 {self.name} vs {other.name}")
        return self.value > other.value

    @classmethod
    @abstractmethod
    def match(cls, cards: List[Card]) -> Optional['CardPattern']:
        pass

    def __str__(self):
        return f"{self.name} " + " ".join(str(c) for c in self.cards)


class Single(CardPattern):
    name = "單張"

    @classmethod
    def match(cls, cards: List[Card]) -> Optional['CardPattern']:
        return cls(cards) if len(cards) == 1 else None

class Pair(CardPattern):
    name = "對子"

    @classmethod
    def match(cls, cards: List[Card]) -> Optional['CardPattern']:
        return cls(cards) if len(cards) == 2 and cards[0].rank==cards[1].rank else None

class Straight(CardPattern):
    name ="順子"

    @classmethod
    def match(cls, cards: List[Card]) -> Optional['CardPattern']:
        if len(cards) != 5:
            return None

        idx = {RANK_ORDER[c.rank if c.rank != '10' else '0'] for c in cards}

        if len(idx) != 5:
            return None

        valid_straights = [{(i + k) % 13 for k in range(5)} for i in range(13)]

        if idx in valid_straights:
            return cls(cards)

        return None

class FullHouse(CardPattern):
    name = "葫蘆"

    @property
    def value(self) -> int:
        return self.cards[2].sort_idx

    @classmethod
    def match(cls, cards: List[Card]) -> Optional['CardPattern']:
        if len(cards) != 5:
            return None

        s = cards
        r = [c.rank for c in s]

        if (r[0] == r[1] == r[2] and r[3] == r[4]) or (r[0] == r[1] and r[2] == r[3] == r[4]):
            return cls(s)

        return None