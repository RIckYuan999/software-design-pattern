from src.player import HumanPlayer, AIPlayer
from src.showdown import Showdown


def main():
    game = Showdown()

    print("\n========== Showdown 撲克遊戲 ==========")
    print(f"請依序設定 {game.MAX_PLAYERS} 位玩家")

    existing_names = set()
    for i in range(game.MAX_PLAYERS):
        while True:
            print(f"\n--- 設定第 {i + 1} 位玩家 ---")
            p_type = input("請選擇類型 (1: 人類, 2: 電腦): ").strip()
            
            if p_type in ("1", "2"):
                if p_type == "1":
                    while True:
                        name = input("請輸入名稱: ").strip()
                        if not name:
                            name = f"Player-{i+1}"
                        if name in existing_names:
                            print(f"名稱 '{name}' 已被使用，請重新輸入。")
                        else:
                            break
                    print(f"已自動命名為: {name}")
                    player = HumanPlayer(name)
                else:
                    name = f"AI-{i+1}"
                    suffix = 1
                    while name in existing_names:
                        name = f"AI-{i+1}-{suffix}"
                        suffix += 1
                    print(f"已自動命名為: {name}")
                    player = AIPlayer(name)

                existing_names.add(name)
                game.add_player(player)
                break
            print("輸入錯誤，請輸入 1 或 2")

    game.start_game()
    game.play()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
