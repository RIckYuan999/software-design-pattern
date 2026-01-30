from __future__ import annotations
from ..domain.model.battle import Battle
from ..domain.shared.event_bus import DomainEventBus


class GameService:
    def __init__(self, battle: Battle):
        self.battle = battle

    def start(self):
        DomainEventBus.reset()
        while not self.battle.is_over():
            self.battle.process_turn()

        if self.battle.troops[1] and self.battle.troops[1][0].is_alive():
            print("你獲勝了！")
        else:
            print("你失敗了！")