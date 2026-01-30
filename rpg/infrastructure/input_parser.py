from __future__ import annotations
from typing import Dict, Any, List

from ..domain.model.battle import Battle
from ..domain.model.unit import Unit
from ..domain.model.strategy import AIStrategy, HeroStrategy
from ..domain.model.action import ActionFactory, BasicAttack


class InputParser:
    def parse_file(self, file_path: str) -> Battle:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return self.parse_lines(lines)

    def parse_lines(self, lines: List[str]) -> Battle:
        t1_data, t2_data, command_buffer = [], [], []
        current_section = None

        for line in lines:
            line = line.strip()
            if not line: continue

            if line == "#軍隊-1-開始":
                current_section = "T1"
            elif line == "#軍隊-1-結束":
                current_section = "CMD"
            elif line == "#軍隊-2-開始":
                current_section = "T2"
            elif line == "#軍隊-2-結束":
                current_section = "CMD"
            elif current_section == "T1":
                t1_data.append(self._parse_line(line))
            elif current_section == "T2":
                t2_data.append(self._parse_line(line))
            elif current_section == "CMD":
                parts = line.replace(" ", "").split(",")
                for p in parts:
                    if p: command_buffer.append(int(p))

        return self._build_battle(t1_data, t2_data, command_buffer)

    def _parse_line(self, line: str) -> Dict[str, Any]:
        parts = line.split()
        return {
            "name": parts[0], "hp": int(parts[1]),
            "mp": int(parts[2]), "str": int(parts[3]),
            "skills": parts[4:] if len(parts) > 4 else []
        }

    def _build_battle(self, t1_data, t2_data, commands) -> Battle:
        t1_units, t2_units = [], []

        for data in t1_data:
            strat = HeroStrategy(commands) if data["name"] == "英雄" else AIStrategy(0)
            u = Unit(data["name"], data["hp"], data["mp"], data["str"], strat, 1)
            u.add_action(BasicAttack())
            for s in data["skills"]:
                if act := ActionFactory.create(s): u.add_action(act)
            t1_units.append(u)

        for data in t2_data:
            u = Unit(data["name"], data["hp"], data["mp"], data["str"], AIStrategy(0), 2)
            u.add_action(BasicAttack())
            for s in data["skills"]:
                if act := ActionFactory.create(s): u.add_action(act)
            t2_units.append(u)

        return Battle(t1_units, t2_units)
