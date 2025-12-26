from abc import ABC, abstractmethod
from typing import Optional, List
import random

from src.card import Card
from src.hand import Hand


class Player(ABC):
    def __init__(self, name):
        self._name: str = name
        self._has_used_exchange: bool = False
        self._point: int = 0
        self._hand: Hand = Hand()

    @property
    def name(self) -> str:
        return self._name

    @property
    def has_used_exchange(self) -> bool:
        """ 是否使用交換手牌特權 """
        return self._has_used_exchange

    @has_used_exchange.setter
    def has_used_exchange(self, value) -> None:
        """ 設定是否使用交換手牌特權 """
        self._has_used_exchange = value

    @property
    def point(self) -> int:
        """ 玩家得分 """
        return self._point

    @property
    def hand(self) -> Hand:
        """ 玩家手牌 """
        return self._hand

    def gain_point(self) -> None:
        """ 得分加一 """
        self._point += 1

    def add_card_to_hand(self, card: Card) -> None:
        """ 抽到手牌委派給 Hand """
        self._hand.add_card(card)

    @abstractmethod
    def show(self) -> Optional[Card]:
        """ 出牌 """
        pass

    @abstractmethod
    def decide_exchange(self, other_players: List['Player']) -> Optional['Player']:
        """ 選擇跟哪位玩家交換牌 """
        pass

class HumanPlayer(Player):

    def show(self) -> Optional[Card]:
        if len(self._hand) == 0:
            return None

        print(f"\n--- {self.name} 的手牌 ---")
        for idx, card in enumerate(self._hand, start=1):
            print(f'  [{idx}]: {card}')

        while True:
            card_input = input(f'請選擇要出的牌 (1-{len(self._hand)}): ')

            try:
                card_idx = int(card_input)
            except ValueError:
                continue

            if 1 <= card_idx <= len(self._hand):
                return self._hand.play_card(card_idx -1)
            print(f'輸入錯誤，請輸入 1 到 {len(self._hand)} 之間的數字')

    def decide_exchange(self, other_players: List['Player']) -> Optional['Player']:
        """ 選擇跟哪位玩家交換牌"""
        if self._has_used_exchange:
            return None

        while True:
            choice = input(f"\n[{self._name}] 是否使用「交換手牌」特權？(剩餘 1 次) [y/n]: ").lower()
            if choice in ('y', 'n'):
                break

        if choice != 'y':
            return None

        candidates = [p for p in other_players if p != self]

        print('請選擇交換對象:')

        for idx, p in enumerate(candidates, start=1):
            print(f'  [{idx}]: {p.name}')

        while True:
            target_input = input(f'請輸入對象編號 (1-{len(candidates)})，或輸入 0 取消: ')

            try:
                target_idx = int(target_input)
            except ValueError:
                continue

            if target_idx == 0:
                return None

            if 1 <= target_idx <= len(candidates):
                print(f'玩家 {self._name} 選擇與 {candidates[target_idx - 1].name} 交換手牌！')
                return candidates[target_idx - 1]

            print(f'輸入錯誤，請輸入 0 到 {len(candidates)} 之間的數字')

class AIPlayer(Player):

    def show(self) -> Optional[Card]:
        """ 出牌 """
        if len(self._hand) == 0:
            return None
        rand_idx = random.randint(0, len(self._hand) - 1)
        return self._hand.play_card(rand_idx)


    def decide_exchange(self, other_players: List['Player']) -> Optional['Player']:
        """ 選擇跟哪位玩家交換牌"""
        if self._has_used_exchange:
            return None

        if random.random() < 0.1:
            candidates = [p for p in other_players if p != self]
            if candidates:
                target = random.choice(candidates)
                print(f'玩家 {self._name} 發動了交換手牌，對象是 {target.name}！')
                return target
        return None