from typing import Tuple, Optional

from src.core import GameContext, Deck, Player, GameRule
from .models import ShowdownCard, Suit, Rank

class ShowdownRule(GameRule):
    @property
    def player_range(self) -> Tuple[int, int]:
        return 4, 4

    def create_desk(self) -> Deck:
        return Deck([ShowdownCard(suit, rank) for suit in Suit for rank in Rank])

    def on_game_start(self, context: GameContext):


        # 洗牌/發牌
        print("\n===== 洗牌與發牌 =====")
        context.shuffle_deck()
        context.deal_cards(13)

        # 初始化牌桌資訊
        context.table_data["round"] = 1
        context.table_data["scores"] = {player: 0 for player in context.players}

    def play_step(self, context: GameContext) -> bool:
        if context.table_data["round"] > 13:
            return False

        print(f"\n===== 回合 {context.table_data['round']} =====")
        # 回合暫存
        moves = []
        for player in context.players:
            card = player.take_turn({})
            if card:
                context.player_play_card(player, card)
                moves.append((player, card))

        print(f"\n----- 回合 {context.table_data['round']} 結算 -----")
        if moves:
            for player, card in moves:
                print(f"{player.name} 出牌：{card}")

            winner, _ = max(moves, key=lambda x: x[1])
            context.table_data["scores"][winner] += 1
            print(f"\n回合贏家：{winner.name}")

        context.table_data["round"] += 1
        return True

    def get_winner(self, context: GameContext) -> Optional[Player]:
        return max(context.table_data["scores"], key=context.table_data["scores"].get)
