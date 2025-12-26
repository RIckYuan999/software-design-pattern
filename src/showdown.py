from typing import List, Dict, Optional

from src.card import Deck, Card
from src.exchange import ExchangeHands
from src.player import Player


class Showdown:
    MAX_PLAYERS = 4
    ROUNDS = 13

    def __init__(self):
        self._current_round: int = 0
        self._deck = Deck()
        self._players: List[Player] = []
        self._exchange_hands: List[ExchangeHands] = []

    def add_player(self, player: Player) -> None:
        """ 加入玩家"""
        if len(self._players) < self.MAX_PLAYERS:
            self._players.append(player)
        else:
            raise ValueError("已達到最大玩家數量")

    def start_game(self) -> None:
        """ 開始遊戲 """
        print("\n========== 遊戲開始 ==========\n")

        self._deck.shuffle() # 洗牌
        self._deal_cards() # 發牌

    def play(self) -> None:
        """ 回合循環 """
        for r in range(self.ROUNDS):
            self._process_round(r)

        self._announce_winner()

    def _deal_cards(self) -> None:
        """ 發牌 """
        print("洗牌與發牌中...")
        # 根據設定的回合數發牌，確保每位玩家都有足夠的手牌
        for _ in range(self.ROUNDS):
            for p in self._players:
                card = self._deck.draw_card()
                p.add_card_to_hand(card)
                
    @staticmethod
    def _compare_and_award_point(round_cards: Dict[Player, Optional[Card]]) -> None:
        """ 根據權重判定玩家得分"""

        valid_players = {p: c for p, c in round_cards.items() if c is not None}
        if not valid_players: return

        round_winner = max(valid_players.keys(), key=lambda p: valid_players[p].get_weight())
        print(f"本回合獲勝者: {round_winner.name} (+1 分)")
        round_winner.gain_point()

    def _exchange_lifecycle(self) -> None:
        """ 維護 exchange 生命週期 """
        to_remove = []
        for eh in self._exchange_hands:
            eh.tick()
            if eh.is_expired():
                to_remove.append(eh)

        for eh in to_remove:
            self._exchange_hands.remove(eh)

    def _announce_winner(self) -> None:
        """ 宣告勝利"""
        print("\n========== 最終結算 ==========")
        
        # 依分數排序顯示
        sorted_players = sorted(self._players, key=lambda x: x.point, reverse=True)
        for rank, p in enumerate(sorted_players, 1):
            print(f"第 {rank} 名: {p.name} (得分: {p.point})")

        final_winner = max(self._players, key=lambda x: x.point)
        print(f"\n遊戲勝利者: {final_winner.name}\n")


    def _process_round(self, round_num: int) -> None:
        """ 單一回合 """

        self._current_round = round_num
        print(f"\n========== 第 {self._current_round + 1} 回合 ==========")

        # 換牌到期維護
        self._exchange_lifecycle()

        # 記錄本回合的牌
        round_cards = {}

        # 詢問是否換牌
        for p in self._players:
            target = p.decide_exchange(self._players)
            if target and not p.has_used_exchange:
                new_exchange = ExchangeHands(p, target)
                self._exchange_hands.append(new_exchange)

        # 玩家出牌
        for p in self._players:
            card = p.show()
            round_cards[p] = card

        # 亮牌
        for p, card in round_cards.items():
            print(f"{p.name} 出牌: {card}")

        # 判定本回合勝負
        Showdown._compare_and_award_point(round_cards)