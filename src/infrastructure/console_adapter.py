import sys

from ..application.game_service import GameService


class ConsoleAdapter:
    def __init__(self):
        self.service = GameService()

    def run(self):
        lines = sys.stdin.readlines()
        if not lines:
            return

        deck_str = lines[0].strip()
        names = [lines[i].strip() for i in range(1, 5)]
        actions = lines[5:]

        self.service.start_game(deck_str, names)
        print("新的回合開始了。")

        for action in actions:

            # 顯示狀態
            p_dto = self.service.get_current_player_info()
            print(f"輪到{p_dto.name}了")
            self._print_hand(p_dto.hand_strings)

            # 執行指令
            result = self.service.execute_turn(action)

            # 處理輸出
            if result.action_type == 'ERROR':
                print(result.message)
                continue

            if result.action_type == 'PASS':
                print(f"玩家 {result.player_name} PASS.")
                if result.is_round_reset:
                    print("新的回合開始了。")

            if result.action_type == 'PLAY':
                print(f"玩家 {result.player_name} 打出了 {result.message}")
                if result.is_game_over:
                    print(f"遊戲結束，遊戲的勝利者為 {result.player_name}")
                    return

    def _print_hand(self, hand_strs):
        idx_parts = []
        card_parts = []

        for i, c_str in enumerate(hand_strs):
            width = len(c_str)
            idx_parts.append(str(i).ljust(width))
            card_parts.append(c_str)
        print(" ".join(idx_parts))
        print(" ".join(card_parts))