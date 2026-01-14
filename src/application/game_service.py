from typing import List

from .dto import PlayerDTO, TurnResult
from ..domain.game import Game
from ..domain.model import Card


class GameService:
    def __init__(self):
        self.game = Game()

    def start_game(self, raw_deck_str: str, names: List[str]):
        deck = [Card(t[0], t[2:-1]) for t in raw_deck_str.split()]
        self.game.initialize(names, deck)

    def get_current_player_info(self) -> PlayerDTO:
        p = self.game.get_current_player()
        return PlayerDTO(name=p.name, hand_strings=[str(c) for c in p.hand])

    def execute_turn(self, input_line: str) -> TurnResult:
        player_name = self.game.get_current_player().name
        line = input_line.strip()

        if line == "-1":
            try:
                is_reset = self.game.pass_turn()
                msg = ""
                return TurnResult(player_name, 'PASS', msg, is_round_reset=is_reset)
            except ValueError as e:
                return TurnResult(player_name, 'ERROR', str(e))

        try:
            idx = [int(x) for x in line.split()]
            pattern_str = self.game.play_cards(idx)
            is_win = (self.game.winner is not None)
            return TurnResult(player_name, 'PLAY', pattern_str, is_game_over=is_win)
        except (ValueError, IndexError):
            return TurnResult(player_name, 'ERROR', "此牌型不合法，請再嘗試一次。")
