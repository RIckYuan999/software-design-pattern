import sys
import os
from rpg.infrastructure.input_parser import InputParser
from rpg.application.game_service import GameService

if __name__ == "__main__":
    try:
        parser = InputParser()
        
        if len(sys.argv) > 1:
            input_file = sys.argv[1]
            if not os.path.exists(input_file):
                print(f"錯誤: 找不到檔案 {input_file}")
                sys.exit(1)
            battle = parser.parse_file(input_file)
        else:
            lines = sys.stdin.readlines()
            if not lines:
                print("錯誤: 沒有提供輸入數據")
                sys.exit(1)
            battle = parser.parse_lines(lines)

        service = GameService(battle)
        service.start()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"發生錯誤: {e}")