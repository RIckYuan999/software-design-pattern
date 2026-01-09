import random
from typing import List, Dict, Any, Optional

from src.core import Card


class ShowdownHumanMind:
    def decide(self, hand: List[Card], context: Dict[str, Any]) -> Optional[Card]:
        if len(hand) == 0:
            return None

        name = context.get('player_name', 'Unknown')
        print(f"\n----- {name} 的回合 -----")
        print(f"  手牌：")

        for idx, card in enumerate(hand, start=1):
            print(f"    [{idx}: {card}]")

        while True:
            try:
                card_idx = int(input(f"請選擇要出的牌 (1-{len(hand)}): "))
                if 1 <= card_idx <= len(hand):
                    return hand[card_idx - 1]
            except ValueError:
                pass
            print(f"輸入錯誤，請輸入 1 到 {len(hand)} 之間的數字")


class ShowdownAIMind:
    def decide(self, hand: List[Card], context: Dict[str,Any]) -> Optional[Card]:
        if len(hand) == 0:
            return None
        rand_idx = random.randint(0, len(hand) - 1)
        return hand[rand_idx]

