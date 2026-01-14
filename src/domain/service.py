from typing import List, Type

from .model import Card
from .parterns import CardPattern, Straight, FullHouse, Pair, Single


class PatternParser:
    CHAIN: List[Type[CardPattern]] = [Straight, FullHouse, Pair, Single]

    @classmethod
    def parser(cls, cards: List[Card]) -> CardPattern:
        for p_cls in PatternParser.CHAIN:
            res = p_cls.match(cards)
            if res:
                return res
        raise ValueError("此牌型不合法")