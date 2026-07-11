"""
Hệ thống Entity gốc cho toàn bộ game: Player, NPC, Mob đều kế thừa từ Entity.
Bao gồm chỉ số chiến đấu (HP/MP/ATK/DEF/EXP), state machine cơ bản,
và hook cập nhật animation mỗi frame.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from game.core.sprite_animation import AnimationController
from game.data.animations import AnimState, Direction


@dataclass
class Stats:
    hp: int
    max_hp: int
    mp: int = 0
    max_mp: int = 0
    atk: int = 1
    defense: int = 0
    exp_reward: int = 0
    level: int = 1

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, raw_damage: int) -> int:
        mitigated = max(1, raw_damage - self.defense)
        self.hp = max(0, self.hp - mitigated)
        return mitigated

    def heal(self, amount: int):
        self.hp = min(self.max_hp, self.hp + amount)


class Entity:
    """Lớp cơ sở cho mọi thực thể sống trong world: Player / NPC / Mob."""

    def __init__(self, entity_id: str, name: str, x: float, y: float,
                 stats: Stats, anim: Optional[AnimationController] = None):
        self.entity_id = entity_id
        self.name = name
        self.x = x
        self.y = y
        self.stats = stats
        self.anim = anim
        self.direction = Direction.DOWN
        self.speed = 90.0  # pixel/s
        self.is_moving = False

    def move(self, dx: float, dy: float, dt: float):
        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt
        self.is_moving = (dx != 0 or dy != 0)
        if dx > 0:
            self.direction = Direction.RIGHT
        elif dx < 0:
            self.direction = Direction.LEFT
        elif dy > 0:
            self.direction = Direction.DOWN
        elif dy < 0:
            self.direction = Direction.UP

    def attack_target(self, target: "Entity") -> int:
        return target.stats.take_damage(self.stats.atk)

    def update(self, dt: float):
        if self.anim is None:
            return
        if not self.stats.is_alive():
            self.anim.set_state(AnimState.DIE, loop=False)
        elif self.is_moving:
            self.anim.set_state(AnimState.WALK, self.direction)
        else:
            self.anim.set_state(AnimState.IDLE, self.direction)
        self.anim.update(dt)


class Player(Entity):
    def __init__(self, entity_id: str, name: str, x: float, y: float, stats: Stats,
                 hairstyle_id: str, outfit_id: str, weapon_id: str,
                 anim: Optional[AnimationController] = None):
        super().__init__(entity_id, name, x, y, stats, anim)
        self.hairstyle_id = hairstyle_id
        self.outfit_id = outfit_id
        self.weapon_id = weapon_id
        self.inventory: List[Dict[str, Any]] = []
        self.gold = 0


class DialogueNode:
    def __init__(self, text: str, options: Optional[List["DialogueOption"]] = None):
        self.text = text
        self.options = options or []


class DialogueOption:
    def __init__(self, label: str, next_node: Optional[DialogueNode] = None,
                 quest_trigger: Optional[str] = None):
        self.label = label
        self.next_node = next_node
        self.quest_trigger = quest_trigger


class NPC(Entity):
    def __init__(self, entity_id: str, name: str, x: float, y: float, stats: Stats,
                 dialogue_root: DialogueNode, quest_id: Optional[str] = None,
                 anim: Optional[AnimationController] = None):
        super().__init__(entity_id, name, x, y, stats, anim)
        self.dialogue_root = dialogue_root
        self.quest_id = quest_id

    def start_dialogue(self) -> DialogueNode:
        return self.dialogue_root


class Mob(Entity):
    def __init__(self, entity_id: str, name: str, x: float, y: float, stats: Stats,
                 mob_type: str, aggro_range: float = 120.0,
                 anim: Optional[AnimationController] = None):
        super().__init__(entity_id, name, x, y, stats, anim)
        self.mob_type = mob_type
        self.aggro_range = aggro_range
        self.target: Optional[Entity] = None

    def try_aggro(self, player: Player) -> bool:
        dist = ((self.x - player.x) ** 2 + (self.y - player.y) ** 2) ** 0.5
        if dist <= self.aggro_range:
            self.target = player
            return True
        return False
