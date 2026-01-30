from __future__ import annotations
from typing import List, TYPE_CHECKING
from ..shared.event_bus import DomainEventBus, UnitDiedEvent
from .attributes import Attributes
from state import StatusEffect, NormalState, StateType
from .action import Action

if TYPE_CHECKING:
    from .strategy import ControlStrategy


class Unit:
    def __init__(self, name: str, hp: int, mp: int, str_val: int, strategy: ControlStrategy, troop_id: int):
        self.name = name
        self.troop_id = troop_id
        self._attrs = Attributes(hp, mp, str_val)
        self.strategy = strategy
        self.state: StatusEffect = NormalState()
        self.state_turns = 0
        self.actions: List[Action] = []
        self.is_dead = False
        self.display_name = f"[{troop_id}]{name}"

    @property
    def hp(self) -> int:
        return self._attrs.hp

    @property
    def mp(self) -> int:
        return self._attrs.mp

    @property
    def str_val(self) -> int:
        return self._attrs.str_val

    def add_action(self, action: Action):
        if action: self.actions.append(action)

    def is_alive(self) -> bool:
        return not self.is_dead

    def set_state(self, new_state: StatusEffect):
        self.state = new_state
        self.state_turns = new_state.duration

    def get_outgoing_damage(self, base: int) -> int:
        return self.state.modify_damage(base)

    def take_damage(self, amount: int):
        self._attrs = self._attrs.modify_hp(-amount)
        if self.hp == 0 and not self.is_dead:
            self.die()

    def heal(self, amount: int):
        self._attrs = self._attrs.modify_hp(amount)

    def recover_mp(self, amount: int):
        self._attrs = self._attrs.modify_mp(amount)

    def consume_mp(self, amount: int):
        self._attrs = self._attrs.modify_mp(-amount)

    def die(self):
        self.is_dead = True
        print(f"{self.display_name} 死亡。")
        DomainEventBus.publish(UnitDiedEvent(self))

    def _update_state_duration(self):
        if self.state_turns > 0:
            self.state_turns -= 1
            if self.state_turns == 0:
                self.state = NormalState()

    def process_turn_start(self) -> bool:
        print(
            f"輪到 {self.display_name} (HP: {self.hp}, MP: {self.mp}, STR: {self.str_val}, State: {self.state.name})。")

        can_act = True
        if self.state_turns > 0:
            can_act = self.state.on_turn_start(self)
            if not can_act:
                self._update_state_duration()
        return can_act

    def process_turn_end(self):
        self._update_state_duration()

    def decide_action(self, all_actions: List['Action']) -> 'Action':
        return self.strategy.decide_action(all_actions)

    def select_targets(self, candidates: List['Unit'], count: int) -> List['Unit']:
        return self.strategy.select_targets(candidates, count)

    def is_in_state(self, state_type: StateType) -> bool:
        return self.state is not None and self.state.type == state_type