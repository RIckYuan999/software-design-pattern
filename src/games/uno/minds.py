import random
from typing import List, Dict, Any, Optional

from src.core import Card


class UnoHumanMind:
    def decide(self, hand: List[Card], context: Dict[str, Any]) -> Optional[Card]:
        name = context.get('player_name', 'Unknown')
        valid = context.get("valid_indices", [])
        print(f"\n----- {name} 的回合 -----")

        print(f"  手牌：")
        for idx, card in enumerate(hand, start=1):
            print(f"    [{idx}: {card}]")

        if len(valid) == 0:
            input("\n無牌可出，請按 Enter 鍵繼續")
            return None

        print(f"\n  可出的牌：")
        for i, valid_idx in enumerate(valid, start=1):
            print(f"    [{i}: {hand[valid_idx]}]")


        while True:
            try:
                card_idx = input(f"請選擇要出的牌 (1-{len(valid)})，或直接按 Enter 抽牌: ")
                if not card_idx:
                    return None
                card_idx = int(card_idx)
                
                if 1 <= card_idx <= len(valid):
                    print(f"\n 出牌：{hand[valid[card_idx - 1]]}")
                    return hand[valid[card_idx - 1]]

            except ValueError:
                pass
            print(f"輸入錯誤，請輸入 1 到 {len(valid)} 之間的數字，或直接按 Enter 抽牌")

class UnoAIMind:
    def decide(self, hand: List[Card], context: Dict[str,Any]) -> Optional[Card]:

        name = context.get('player_name', 'Unknown')
        valid = context.get("valid_indices", [])
        print(f"\n----- {name} 的回合 -----")

        if not valid:
            return None

        card = hand[random.choice(valid)]
        print(f"\n 出牌：{card}")
        return card