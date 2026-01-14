from dataclasses import dataclass


@dataclass
class PlayerDTO:
    name: str
    hand_strings: list[str]

@dataclass
class TurnResult:
    player_name: str
    action_type: str
    message: str = ""
    is_game_over: bool = False
    is_round_reset: bool = False