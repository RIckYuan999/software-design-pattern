from __future__ import annotations

from typing import List, Protocol, runtime_checkable, TYPE_CHECKING

if TYPE_CHECKING:
    from .unit import Unit
    from .action import Action


@runtime_checkable
class ControlStrategy(Protocol):
    def decide_action(self, all_actions: List[Action]) -> Action:
        ...

    def select_targets(self, candidates: List[Unit], count: int) -> List[Unit]:
        ...

class AIStrategy:
    def __init__(self, seed: int = 0):
        self.seed = seed

    def decide_action(self, all_actions: List[Action]) -> Action:
        if not all_actions:
            raise ValueError("No actions available")
        idx = self.seed % len(all_actions)
        self.seed += 1
        return all_actions[idx]

    def select_targets(self, candidates: List[Unit], count: int) -> List[Unit]:
        if len(candidates) <= count:
            return candidates

        targets = []
        if not candidates: return targets
        for i in range(count):
            idx = (self.seed + i) % len(candidates)
            targets.append(candidates[idx])
        self.seed += 1
        return targets


class HeroStrategy:
    def __init__(self, input_buffer: List[int]):
        self.input_buffer = input_buffer
        self._idx = 0

    def _next_int(self) -> int:
        if self._idx < len(self.input_buffer):
            val = self.input_buffer[self._idx]
            self._idx += 1
            return val
        return -1

    def decide_action(self, all_actions: List[Action]) -> Action:
        if not all_actions:
            raise ValueError("No actions available")
        
        while True:
            choice_idx = self._next_int()
            if choice_idx == -1:
                return all_actions[0]
            if 0 <= choice_idx < len(all_actions):
                return all_actions[choice_idx]

    def select_targets(self, candidates: List[Unit], count: int) -> List[Unit]:
        if len(candidates) <= count:
            return candidates

        targets = []
        while len(targets) < count:
            choice_idx = self._next_int()
            if choice_idx == -1:
                break

            if 0 <= choice_idx < len(candidates):
                targets.append(candidates[choice_idx])
            else:
                continue
        return targets