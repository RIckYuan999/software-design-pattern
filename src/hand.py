from typing import Optional, List

from src.card import Card


class Hand:
    def __init__(self):
        self._cards: List[Card] = []
        
    @property
    def cards(self) -> List[Card]:
        """ 手牌"""
        return self._cards
        
    def add_card(self, card: Card) -> None:
        """ 新增卡牌到手牌 """
        self._cards.append(card)
        
    def play_card(self, index: int) -> Optional[Card]:
        """ 取出一張手牌 """
        if 0 <= index < len(self._cards):
            return self._cards.pop(index)
        return None
    
    def swap_content(self, other_hand: 'Hand') -> None:
        """ 交換手牌內容 """
        self._cards, other_hand._cards = other_hand._cards, self._cards

    def __len__(self):
        return len(self._cards)

    def __iter__(self):
        return iter(self._cards)