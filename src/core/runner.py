from typing import List

from .context import GameContext
from .interfaces import GameRule
from .models import Player, CardGame


class GameRunner:
    def __init__(self, rule: GameRule, players: List[Player]):
        self._rule = rule
        self._game = CardGame()
        self._game.players = players

    def run(self):
        print(f"\n====== 遊戲引擎 {self._rule.__class__.__name__} 啟動 =====")

        # Step 1: 創建牌組
        self._game.deck = self._rule.create_desk()

        # 建立防腐層
        safe_ctx = GameContext(self._game)

        # Step 2: 開始遊戲
        self._rule.on_game_start(safe_ctx)

        # Step 3: 回合控制
        is_running = True
        step_count = 0
        while is_running:
            step_count += 1
            is_running = self._rule.play_step(safe_ctx)

        # Step 4: 遊戲結束，找勝利者
        winner = self._rule.get_winner(safe_ctx)
        print(f"\n===== 遊戲結束 =====")
        print(f"贏家：{winner.name if winner else '平手'}")