from typing import List, Optional, Tuple

from .models import CardGame, Player, Card


class GameContext:
    def __init__(self, game: CardGame):
        self._game = game

    # ----- 唯獨屬性 -----
    @property
    def players(self) -> Tuple[Player, ...]:
        return tuple(self._game.players)

    @property
    def table_data(self) -> dict:
        return self._game.table_data

    # ----- 受控動作 -----
    def shuffle_deck(self):
        if self._game.deck:
            self._game.deck.shuffle()

    def deal_cards(self, count: int):
        for _ in range(count):
            for player in self._game.players:
                if card := self._game.deck.draw_card():
                    player.add_card(card)

    def add_card(self, cards: List[Card]):
        self._game.deck.add_cards(cards)

    def draw_card(self) -> Optional[Card]:
        if self._game.deck:
            return self._game.deck.draw_card()
        return None

    def player_draw_card(self, player: Player) -> Optional[Card]:
        if self._game.deck:
            card = self._game.deck.draw_card()
            if card:
                player.add_card(card)
                return card
        return None

    def player_play_card(self, player: Player, context: dict) -> Optional[Card]:
        return player.take_turn(context)

    def set_winner(self, player: Player):
        self._game.table_data["winner"] = player

    def is_card_empty(self):
        return self._game.deck.is_empty()