from dataclasses import dataclass, field
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .parterns import CardPattern


SUIT_ORDER = {s: i for i, s in enumerate('CDHS')}
RANK_ORDER = {r: i for i, r in enumerate('34567890JQKA2')}

@dataclass(order=True, frozen=True)
class Card:
    sort_idx: int = field(init=False, repr=False)
    suit: str
    rank: str

    def __post_init__(self):
        r_key = self.rank if self.rank != '10' else '0'
        object.__setattr__(self, 'sort_idx', RANK_ORDER[r_key] * 10 + SUIT_ORDER[self.suit])

    def __str__(self):
        return f"{self.suit}[{self.rank}]"

@dataclass
class Round:
    top_play: Optional['CardPattern'] = None
    top_player_idx: int = -1
    pass_count: int = 0

    def pass_turn(self) -> bool:
        """ 3人 pass 回傳 turn """
        self.pass_count += 1
        return self.pass_count == 3

    def submit_play(self, pattern: 'CardPattern', player_idx: int):
        self.top_play = pattern
        self.top_player_idx = player_idx
        self.pass_count = 0

@dataclass
class Player:
    id: int
    name: str
    hand: List[Card] = field(default_factory=list)

    def add_card(self, card: Card):
        self.hand.append(card)
        self.hand.sort()

    def remove_cards(self, cards: List[Card]):
        for c in cards:
            if c in self.hand:
                self.hand.remove(c)
            else:
                # 理論上不會發生，防患未然
                raise ValueError(f"玩家 {self.name} 手中沒有這張牌")

    def has_card(self, target: Card) -> bool:
        return target in self.hand

    @property
    def is_finished(self) -> bool:
        return len(self.hand) == 0
