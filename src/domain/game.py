from typing import List, Optional

from .model import Player, Round, Card
from .service import PatternParser


class Game:
    def __init__(self):
        self.players: List[Player] = []
        self.current_round: Optional[Round] = None
        self.current_player_idx: int = 0
        self.is_first_round: bool = True
        self.winner: Optional[Player] = None

    def initialize(self, player_names: List[str], raw_deck: List[Card]):
        self.players = [Player(i, name) for i, name in enumerate(player_names)]

        # 發牌
        temp_deck = raw_deck[:]
        while temp_deck:
            for i in range(4):
                if temp_deck: self.players[i].add_card(temp_deck.pop())

        # 找到起始玩家，並建立回合
        c3 = Card('C', '3')
        self.current_player_idx = next(i for i, p in enumerate(self.players) if p.has_card(c3))
        self.current_round = Round()

    def get_current_player(self) -> Player:
        return self.players[self.current_player_idx]

    def pass_turn(self):
        if self.current_round.top_player_idx == -1:
            raise ValueError("你不能在新的回合中喊 PASS")

        is_round_over = self.current_round.pass_turn()
        self._advance_player()

        if is_round_over:
            self.current_player_idx = self.current_round.top_player_idx
            self.current_round = Round()
            return True
        return False

    def play_cards(self, card_idx: List[int]) -> str:
        player = self.get_current_player()

        try:
            selected_cards = [player.hand[i] for i in card_idx]
        except IndexError:
            raise ValueError("索引錯誤")

        pattern = PatternParser.parser(selected_cards)

        if self.is_first_round:
            if Card('C', '3') not in pattern.cards:
                raise ValueError("第一回合必須出梅花3")

        if self.current_round.top_play:
            if not (pattern > self.current_round.top_play):
                raise ValueError("牌型太小或類型不符")

        player.remove_cards(selected_cards)
        self.current_round.submit_play(pattern, self.current_player_idx)
        self.is_first_round = False

        pattern_str = str(pattern)

        if player.is_finished:
            self.winner = player
        else:
            self._advance_player()

        return pattern_str

    def _advance_player(self):
        self.current_player_idx = (self.current_player_idx + 1) % 4