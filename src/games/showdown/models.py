from enum import IntEnum

from src.core import Card


class Suit(IntEnum):
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4

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

class ShowdownCard(Card):
    _RANK_MAPPING = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
    _SUIT_SYMBOLS = {1: "♣", 2: "♦", 3: "♥", 4: "♠"}

    def __init__(self, suit: Suit, rank: Rank):
        self._suit = suit
        self._rank = rank

    @property
    def suit(self):
        return self._suit

    @property
    def rank(self):
        return self._rank

    def __str__(self) -> str:
        rank_symbol = self._RANK_MAPPING.get(self._rank, str(self._rank))
        suit_symbol = self._SUIT_SYMBOLS[self._suit]
        return f"{suit_symbol}{rank_symbol}"

    def __lt__(self, other) -> bool:
        return self._rank < other.rank if self._rank != other.rank else self._suit < other.suit

