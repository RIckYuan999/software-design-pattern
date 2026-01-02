from typing import Protocol, List

from src.individual import Individual

# interface 使用鴨子型別
class MatchStrategy(Protocol):
    def sort_candidates(self, me: Individual, candidates: List[Individual]) -> List[Individual]:
        pass

class DistanceBasedStrategy:
    def sort_candidates(self, me: Individual, candidates: List[Individual]) -> List[Individual]:
        return sorted(
            candidates,
            # 坐標優先，id 次之
            key=lambda p: (me.coord.distance_to(p.coord), p.id)
        )

class HabitBasedStrategy:
    def sort_candidates(self, me: Individual, candidates: List[Individual]) -> List[Individual]:
        def calculate_score(other: Individual):
            # 計算興趣交集的數量
            intersection_count = len(me.habits & other.habits)
            # 因 sorted 為升冪，故 intersection_count 需加上負號
            return -intersection_count, other.id
        return sorted(candidates, key=calculate_score)

# MatchStrategy 使用鴨子型別，不需繼承
class ReverseStrategy:
    def __init__(self, wrapped: MatchStrategy):
        self._wrapped = wrapped

    def sort_candidates(self, me: Individual, candidates: List[Individual]) -> List[Individual]:
        original_result = self._wrapped.sort_candidates(me, candidates)
        return list(reversed(original_result))