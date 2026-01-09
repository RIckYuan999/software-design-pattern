from abc import ABC, abstractmethod
from typing import Protocol, List, Dict, Any, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .context import GameContext
    from .models import Player, Deck, Card


class IDecisionMaker(Protocol):
    def decide(self, hand: List['Card'], context: Dict[str, Any]) -> Optional['Card']:
        pass

class GameRule(ABC):

    @property
    @abstractmethod
    def player_range(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def create_deck(self) -> 'Deck':
        pass

    @abstractmethod
    def on_game_start(self, context: 'GameContext'):
        pass

    @abstractmethod
    def play_step(self, context: 'GameContext') -> bool:
        pass

    @abstractmethod
    def get_winner(self, context: 'GameContext') -> Optional['Player']:
        pass