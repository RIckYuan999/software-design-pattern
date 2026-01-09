from typing import List, Optional, Tuple

from .models import CardGame, Player, Card, Deck


class GameContext:
    def __init__(self, game: CardGame):
        self._game = game

    # ----- 唯獨屬性 -----
    @property
    def players(self) -> Tuple[Player, ...]:
        return tuple(self._game.players)

    @property
    def deck(self) -> Deck:
        return self._game.deck

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

    def player_play_card(self, player: Player, card: Card):
        if card in player.hand:
            player.remove_card(card)

    def set_winner(self, player: Player):
        self._game.table_data["winner"] = player