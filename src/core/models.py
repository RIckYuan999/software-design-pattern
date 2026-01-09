import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .interfaces import IDecisionMaker


class Card(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass

class Deck:
    def __init__(self, cards: List[Card]):
        self._cards = cards

    def shuffle(self):
        random.shuffle(self._cards)

    def draw_card(self) -> Optional[Card]:
        return self._cards.pop() if self._cards else None

    def add_cards(self, card: List[Card]):
        self._cards.extend(card)

    def is_empty(self) -> bool:
        return len(self._cards) == 0

class Player:
    def __init__(self, name: str, mind: 'IDecisionMaker'):
        self._name = name
        self._hand: List[Card] = []
        self._mind = mind

    @property
    def name(self):
        return self._name

    @property
    def hand(self):
        return self._hand

    def add_card(self, card: Card):
        self._hand.append(card)

    def remove_card(self, card: Card):
        if card in self._hand:
            self._hand.remove(card)

    def take_turn(self, context: Dict[str, Any]) -> Optional[Card]:
        context["player_name"] = self._name
        card = self._mind.decide(self._hand, context)
        if card:
            self.remove_card(card)
        return card


@dataclass
class CardGame:
    deck: Optional[Deck] = None
    players: List[Player] = field(default_factory=list)
    table_data: Dict[str, Any] = field(default_factory=dict)