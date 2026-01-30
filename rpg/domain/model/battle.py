from __future__ import annotations
from typing import List
from .unit import Unit
from .strategy import AIStrategy
from .action import BasicAttack


class Battle:
    def __init__(self, troop1: List[Unit], troop2: List[Unit]):
        self.troops = {1: troop1, 2: troop2}

    def spawn_unit(self, name: str, hp: int, mp: int, str_val: int, troop_id: int) -> Unit:
        u = Unit(name, hp, mp, str_val, AIStrategy(0), troop_id)
        u.add_action(BasicAttack())
        self.add_unit_dynamic(u)
        return u

    def add_unit_dynamic(self, unit: Unit):
        self.troops[unit.troop_id].append(unit)

    def get_all_units(self) -> List[Unit]:
        return [u for u in self.troops[1] + self.troops[2] if u.is_alive()]

    def get_candidates(self, unit: Unit, target_type: str) -> List[Unit]:
        my_troop_id = unit.troop_id
        if target_type == "ENEMY":
            enemy_id = 2 if my_troop_id == 1 else 1
            return [u for u in self.troops[enemy_id] if u.is_alive()]
        elif target_type == "ALLY":
            return [u for u in self.troops[my_troop_id] if u.is_alive() and u is not unit]
        elif target_type == "SELF":
            return [unit] if unit.is_alive() else []
        return []

    def is_over(self) -> bool:
        t1_alive = any(u.is_alive() for u in self.troops[1])
        t2_alive = any(u.is_alive() for u in self.troops[2])
        if not self.troops[1]:
            return True
        hero = self.troops[1][0]
        if not hero.is_alive():
            return True
        return not t1_alive or not t2_alive

    def process_turn(self):
        units_order = [u for u in self.troops[1] if u.is_alive()] + [u for u in self.troops[2] if u.is_alive()]

        for unit in units_order:
            if self.is_over():
                return
            if not unit.is_alive():
                continue
            if not unit.process_turn_start():
                continue
            if not unit.is_alive():
                continue

            while True:
                print("選擇行動：", end="")
                for i, a in enumerate(unit.actions):
                    print(f"({i}) {a.name} ", end="")
                print("")

                action = unit.decide_action(unit.actions)

                if action.mp_cost > unit.mp:
                    print("你缺乏 MP，不能進行此行動。")
                    continue
                
                break

            candidates = self.get_candidates(unit, action.target_type)
            targets = []

            if action.target_count == -1:
                targets = candidates
            elif action.target_count > 0 and candidates:
                if unit.name == "英雄" and len(candidates) > action.target_count:
                    print(f"選擇 {action.target_count} 位目標: ", end="")
                    for i, c in enumerate(candidates): print(f"({i}) {c.display_name} ", end="")
                    print("")

                targets = unit.select_targets(candidates, action.target_count)


            unit.consume_mp(action.mp_cost)
            action.execute(unit, targets, self)
            unit.process_turn_end()