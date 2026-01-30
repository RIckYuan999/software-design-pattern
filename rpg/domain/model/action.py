from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING, Optional

from ..shared.event_bus import DomainEventBus, UnitDiedEvent
from state import NormalState, PoisonedState, PetrochemicalState, CheerupState
from .damage_handler import HighHpHandler, AbnormalStateHandler, BuffStateHandler, DefaultHandler

if TYPE_CHECKING:
    from .unit import Unit
    from .battle import Battle


class Action(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def mp_cost(self) -> int:
        pass

    @property
    @abstractmethod
    def target_count(self) -> int:
        pass

    @property
    @abstractmethod
    def target_type(self) -> str:
        pass

    @abstractmethod
    def execute(self, user: Unit, targets: List[Unit], battle: Battle):
        pass


class BasicAttack(Action):
    name = "普通攻擊"
    mp_cost = 0
    target_count = 1
    target_type = "ENEMY"

    def execute(self, user, targets, battle):
        t = targets[0]
        print(f"{user.display_name} 攻擊 {t.display_name}。")
        dmg = user.get_outgoing_damage(user.str_val)
        print(f"{user.display_name} 對 {t.display_name} 造成 {dmg} 點傷害。")
        t.take_damage(dmg)


class Waterball(Action):
    name = "水球"
    mp_cost = 50
    target_count = 1
    target_type = "ENEMY"

    def execute(self, user, targets, battle):
        t = targets[0]
        print(f"{user.display_name} 對 {t.display_name} 使用了 水球。")
        dmg = user.get_outgoing_damage(120)
        print(f"{user.display_name} 對 {t.display_name} 造成 {dmg} 點傷害。")
        t.take_damage(dmg)


class Fireball(Action):
    name = "火球"
    mp_cost = 50
    target_count = -1
    target_type = "ENEMY"

    def execute(self, user, targets, battle):
        names = ", ".join([t.display_name for t in targets])
        print(f"{user.display_name} 對 {names} 使用了 火球。")
        for t in targets:
            dmg = user.get_outgoing_damage(50)
            print(f"{user.display_name} 對 {t.display_name} 造成 {dmg} 點傷害。")
            t.take_damage(dmg)


class SelfHealing(Action):
    name = "自我治療"
    mp_cost = 50
    target_count = 1
    target_type = "SELF"

    def execute(self, user, targets, battle):
        print(f"{user.display_name} 使用了 自我治療。")
        user.heal(150)


class Petrochemical(Action):
    name = "石化"
    mp_cost = 100
    target_count = 1
    target_type = "ENEMY"

    def execute(self, user, targets, battle):
        t = targets[0]
        print(f"{user.display_name} 對 {t.display_name} 使用了 石化。")
        t.set_state(PetrochemicalState())


class Poison(Action):
    name = "下毒"
    mp_cost = 80
    target_count = 1
    target_type = "ENEMY"

    def execute(self, user, targets, battle):
        t = targets[0]
        print(f"{user.display_name} 對 {t.display_name} 使用了 下毒。")
        t.set_state(PoisonedState())


class Summon(Action):
    name = "召喚"
    mp_cost = 150
    target_count = 0
    target_type = "NONE"

    def execute(self, user, targets, battle):
        print(f"{user.display_name} 使用了 召喚。")
        slime = battle.spawn_unit("Slime", 100, 0, 50, user.troop_id)

        def on_die(e: UnitDiedEvent):
            if e.dead_unit == slime and user.is_alive():
                user.heal(30)

        DomainEventBus.subscribe(on_die)


class SelfExplosion(Action):
    name = "自爆"
    mp_cost = 200
    target_count = 0
    target_type = "NONE"

    def execute(self, user, targets, battle):
        real_targets = [u for u in battle.get_all_units() if u != user]
        names = ", ".join([t.display_name for t in real_targets])
        print(f"{user.display_name} 對 {names} 使用了 自爆。")
        dmp = user.get_outgoing_damage(150)

        for u in real_targets:
            print(f"{user.display_name} 對 {u.display_name} 造成 {dmp} 點傷害。")
            u.take_damage(dmp)
        
        user.take_damage(user.hp)


class Cheerup(Action):
    name = "鼓舞"
    mp_cost = 100
    target_count = 3
    target_type = "ALLY"

    def execute(self, user, targets, battle):
        if targets:
            names = ", ".join([t.display_name for t in targets])
            print(f"{user.display_name} 對 {names} 使用了 鼓舞。")
            for t in targets:
                t.set_state(CheerupState())
        else:
            print(f"{user.display_name} 使用了 鼓舞。")


class Curse(Action):
    name = "詛咒"
    mp_cost = 100
    target_count = 1
    target_type = "ENEMY"

    def execute(self, user, targets, battle):
        t = targets[0]
        print(f"{user.display_name} 對 {t.display_name} 使用了 詛咒。")

        def on_die(e: UnitDiedEvent):
            if e.dead_unit == t and user.is_alive():
                user.heal(e.dead_unit.mp)

        DomainEventBus.subscribe(on_die)


class OnePunch(Action):
    name = "一拳攻擊"
    mp_cost = 180
    target_count = 1
    target_type = "ENEMY"

    def __init__(self):
        self.chain = HighHpHandler()
        self.chain.set_next(AbnormalStateHandler()) \
                  .set_next(BuffStateHandler()) \
                  .set_next(DefaultHandler())

    def execute(self, user, targets, battle):
        t = targets[0]
        print(f"{user.display_name} 對 {t.display_name} 使用了 一拳攻擊。")

        result = self.chain.handle(user, t)

        if result.clear_state:
            t.set_state(NormalState())

        for _ in range(result.repeat):
            print(f"{user.display_name} 對 {t.display_name} 造成 {result.damage} 點傷害。")
            t.take_damage(result.damage)
            if not t.is_alive(): break

class ActionFactory:
    @staticmethod
    def create(name: str) -> Optional[Action]:
        mapping = {
            "水球": Waterball,
            "火球": Fireball,
            "自我治療": SelfHealing,
            "石化": Petrochemical,
            "下毒": Poison,
            "召喚": Summon,
            "自爆": SelfExplosion,
            "鼓舞": Cheerup,
            "詛咒": Curse,
            "一拳攻擊": OnePunch,
            "普通攻擊": BasicAttack
        }
        cls = mapping.get(name)
        return cls() if cls else None
