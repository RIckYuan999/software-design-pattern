from src.player import Player
from src.hand import Hand


class ExchangeHands:
    def __init__(self, actor: Player, target: Player):
        self._actor: Player = actor
        self._target: Player = target
        self._countdown: int = 3

        # 實例建立時執行交換手牌
        self._swap()
        self._actor.has_used_exchange = True

    def tick(self) -> None:
        """ 計數交換回合"""
        self._countdown -= 1
        if self._countdown == 0:
            print(f"玩家 {self._actor.name} 向玩家 {self._target.name} 交換回合結束")
            self._swap()
        else:
            print(f'玩家 {self._actor.name} 向玩家 {self._target.name} 交換回合剩餘: {self._countdown}')

    def is_expired(self) -> bool:
        """ 查詢是否完成"""
        return self._countdown <= 0

    def _swap(self) -> None:
        """ 交換手牌 """

        actor_hand: Hand = self._actor.hand
        target_hand: Hand = self._target.hand
        actor_hand.swap_content(target_hand)