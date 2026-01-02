from src.individual import Individual, Gender, Coord
from src.match_strategy import DistanceBasedStrategy, HabitBasedStrategy, ReverseStrategy
from src.matchmaking_system import MatchmakingSystem

if __name__ == "__main__":
    users = [
        Individual(1, Gender.MALE, 25, "A", {"Code", "Game"}, Coord(0, 0)),
        Individual(2, Gender.FEMALE, 24, "B", {"Code"}, Coord(1, 1)),
        Individual(3, Gender.FEMALE, 26, "C", {"Game"}, Coord(10, 10)),
        Individual(4, Gender.MALE, 28, "D", set(), Coord(2, 2)),
    ]

    system = MatchmakingSystem(DistanceBasedStrategy())

    print("\n=== 距離優先 ===")
    results_distance = system.match_all(users)

    print("\n=== 反向距離優先 ===")
    system.set_strategy(ReverseStrategy(DistanceBasedStrategy()))
    results_reverse_distance = system.match_all(users)

    print("\n=== 興趣優先 ==")
    system.set_strategy(HabitBasedStrategy())
    results_habit = system.match_all(users)

    print("\n=== 反向興趣優先 ===")
    system.set_strategy(ReverseStrategy(HabitBasedStrategy()))
    results_reverse_habit = system.match_all(users)