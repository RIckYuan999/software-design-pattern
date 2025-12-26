import random
from enum import IntEnum, Enum
from typing import Optional


_SUIT_SYMBOLS = {1: '♣', 2: '♦', 3: '♥', 4: '♠'}
_RANK_MAPPING = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}


class Suit(Enum):
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4

    def __str__(self):
        return _SUIT_SYMBOLS[self.value]

class Rank(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def __str__(self):
        return _RANK_MAPPING.get(self.value, str(self.value))

class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self._suit = suit
        self._rank = rank

    def get_weight(self) -> int:
        """ 取得卡牌權重 """
        return self._rank.value * 10 + self._suit.value

    def __repr__(self):
        return f"{self._suit}{self._rank}"


class Deck:
    def __init__(self):
        self._cards = []
        for suit in Suit:
            for rank in Rank:
                self._cards.append(Card(suit, rank))

    def shuffle(self) -> None:
        """ 洗牌 """
        random.shuffle(self._cards)

    def draw_card(self) -> Optional[Card]:
        """ 從牌堆抽牌 """
        return self._cards.pop() if self._cards else None

