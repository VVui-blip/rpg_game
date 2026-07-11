"""
Định nghĩa toàn bộ animation states dùng chung cho Player và 15 NPC.
Mỗi state tương ứng với 1 hàng (row) trong sprite sheet, hỗ trợ 4-directional
(UP, DOWN, LEFT, RIGHT). Tổng cộng 19 animation logic (một số state không
cần 4 hướng, ví dụ DIE / CELEBRATE chỉ có 1 hướng mặc định).
"""

from enum import Enum, auto


class Direction(Enum):
    DOWN = "down"
    UP = "up"
    LEFT = "left"
    RIGHT = "right"


class AnimState(Enum):
    IDLE = auto()
    WALK = auto()
    RUN = auto()
    ATTACK = auto()
    ATTACK_HEAVY = auto()
    ATTACK_RANGED = auto()
    CAST_SPELL = auto()
    HURT = auto()
    DIE = auto()
    BLOCK = auto()
    DODGE_ROLL = auto()
    JUMP = auto()
    FALL = auto()
    SIT = auto()
    SLEEP = auto()
    EMOTE_WAVE = auto()
    EMOTE_LAUGH = auto()
    PICKUP_ITEM = auto()
    CELEBRATE = auto()


# Các state không cần chia 4 hướng riêng (dùng chung 1 clip)
OMNIDIRECTIONAL_STATES = {
    AnimState.DIE,
    AnimState.SIT,
    AnimState.SLEEP,
    AnimState.CELEBRATE,
    AnimState.EMOTE_LAUGH,
}

# Số frame mặc định gợi ý cho từng state (có thể override theo sprite sheet thật)
DEFAULT_FRAME_COUNT = {
    AnimState.IDLE: 4,
    AnimState.WALK: 6,
    AnimState.RUN: 6,
    AnimState.ATTACK: 5,
    AnimState.ATTACK_HEAVY: 6,
    AnimState.ATTACK_RANGED: 5,
    AnimState.CAST_SPELL: 7,
    AnimState.HURT: 2,
    AnimState.DIE: 6,
    AnimState.BLOCK: 2,
    AnimState.DODGE_ROLL: 5,
    AnimState.JUMP: 4,
    AnimState.FALL: 3,
    AnimState.SIT: 2,
    AnimState.SLEEP: 3,
    AnimState.EMOTE_WAVE: 4,
    AnimState.EMOTE_LAUGH: 4,
    AnimState.PICKUP_ITEM: 4,
    AnimState.CELEBRATE: 6,
}

# Animation riêng cho bụi cỏ trong môi trường (không thuộc entity)
class FoliageAnim(Enum):
    SWAY = auto()      # đung đưa nhẹ theo gió
    TRAMPLED = auto()  # phản ứng khi bị dẫm/chém


FOLIAGE_FRAME_COUNT = {
    FoliageAnim.SWAY: 4,
    FoliageAnim.TRAMPLED: 3,
}
