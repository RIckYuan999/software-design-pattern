from typing import List, Dict

from src.individual import Individual
from src.match_strategy import MatchStrategy


class MatchmakingSystem:
    def __init__(self, strategy: MatchStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: MatchStrategy):
        self._strategy = strategy

    def _match_one(self, me: Individual, candidates: List[Individual]) -> Individual:
        if not candidates:
            raise ValueError("No candidates available")

        sorted_candidates = self._strategy.sort_candidates(me, candidates)

        return sorted_candidates[0]

    def match_all(self, individuals: List[Individual]) -> Dict[Individual, Individual]:

        results = {}

        print(f"--- 開始執行配對 ---")

        for me in individuals:
            others = [p for p in individuals if p.id != me.id]

            if not others:
                print(f"User {me.id} 沒有其他候選人可配對")

            best_match = self._match_one(me, others)
            results[me] = best_match

            print(f"user {me.id} -> match User {best_match.id}")

        return results