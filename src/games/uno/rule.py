from typing import Tuple, Optional

from src.core import GameRule, Deck, GameContext, Player
from .models import Color, Number, UnoCard


class UnoRule(GameRule):
    @property
    def player_range(self) -> Tuple[int, int]:
        return 4, 4

    def create_deck(self) -> Deck:
        return Deck([UnoCard(color, number) for color in Color for number in Number])

    def on_game_start(self, context: GameContext):
        print("\n===== 洗牌與發牌 =====")
        # 洗牌/發牌
        context.shuffle_deck()
        context.deal_cards(8)

        # 初始化牌桌資訊
        context.table_data["round"] = 1
        context.table_data["discard"] = []
        context.table_data["winner"] = None

        # 翻一張牌到台上
        start_card = context.draw_card()
        context.table_data["discard"].append(start_card)
        print(f"\n----- 起始牌：{start_card} -----")

    def play_step(self, context: GameContext) -> bool:
        print(f"\n===== 回合 {context.table_data['round']} =====")

        for player in context.players:

            # 計算可出得牌
            valid = [idx for idx, card in enumerate(player.hand)
                     if card.color == context.table_data["discard"][-1].color
                     or card.number == context.table_data["discard"][-1].number]

            card = context.player_play_card(player, {"valid_indices": valid})
            if card:
                # 出牌
                context.table_data["discard"].append(card)

            else:
                # 檢查牌組是否為空
                if context.is_card_empty():
                    print("\n ===== 牌組重新洗牌中 =====")
                    cards_to_add = context.table_data["discard"][:-1]
                    context.table_data["discard"] = cards_to_add
                    context.add_card(cards_to_add)
                    context.shuffle_deck()

                print(f"\n----- {player.name} 抽牌 -----")
                context.player_draw_card(player)

            # 檢查獲勝者
            if len(player.hand) == 0:
                context.table_data["winner"] = player
                return False

        context.table_data["round"] += 1
        return True

    def get_winner(self, context: GameContext) -> Optional[Player]:
        return context.table_data["winner"]