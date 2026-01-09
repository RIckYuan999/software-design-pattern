from typing import List, Type, TypedDict, Any
from src.core import Player, GameRunner
from src.games.showdown.minds import ShowdownHumanMind, ShowdownAIMind
from src.games.showdown.rule import ShowdownRule
from src.games.uno.minds import UnoHumanMind, UnoAIMind
from src.games.uno.rule import UnoRule

class GameConfig(TypedDict):
    name: str
    minds: List[Type[Any]]
    rule: Type[Any]

GAMES: List[GameConfig] = [
    {
        "name": "簡易撲克牌比大小遊戲",
        "minds": [ShowdownHumanMind, ShowdownAIMind],
        "rule": ShowdownRule
    },
    {
        "name": "簡易 UNO",
        "minds": [UnoHumanMind, UnoAIMind],
        "rule": UnoRule
    }
]

def get_valid_input(prompt: str, valid_range: range, error_msg: str) -> int:
    while True:
        try:
            value = int(input(prompt).strip())
            if value in valid_range:
                return value
        except ValueError:
            pass
        print(error_msg)

def setup():
    print("\n=====  卡牌遊戲引擎啟動 =====")

    # Step 1: 設定遊戲種類
    print("\n請選擇要遊玩的遊戲")
    for idx, game in enumerate(GAMES, start=1):
        print(f"{idx}. {game['name']}")

    game_idx = get_valid_input(
        prompt="請輸入選項: ",
        valid_range=range(1, len(GAMES) + 1),
        error_msg=f"請輸入 1-{len(GAMES)} 的數字"
    ) - 1

    selected_game = GAMES[game_idx]

    # Step 2: 玩家配置
    min_player, max_player = selected_game["rule"]().player_range
    print(f"\n{selected_game['name']} 支援 {min_player} 至 {max_player} 位玩家")

    # 設定玩家數
    player_num = get_valid_input(
        prompt="請輸入玩家數量：",
        valid_range=range(min_player, max_player + 1),
        error_msg=f"請輸入 {min_player} 至 {max_player} 的數字"
    )

    # 選擇玩家類型
    players = []
    for i in range(player_num):
        player_type = get_valid_input(
            prompt=f"\n請選擇 P{i + 1} 玩家類型（1. 人類 2. 電腦）：",
            valid_range=range(1, 3),
            error_msg="請輸入 1 或 2"
        )

        if player_type == 2:
            player_name = f"AI-{i + 1}"
        else:
            player_name = input(f"請輸入 P{i + 1} 玩家名稱：").strip()
        
        mind_class = selected_game["minds"][player_type - 1]
        players.append(Player(player_name, mind_class()))

    # Step 3: 執行
    engine = GameRunner(selected_game["rule"](), players)
    engine.run()

if __name__ == "__main__":
    setup()