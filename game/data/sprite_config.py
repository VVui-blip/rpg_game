"""
row_map chuẩn ứng với cấu trúc sprite sheet do tools/generate_assets.py sinh ra.
Nếu sau này thay bằng asset tải từ Kenney.nl/itch.io, chỉ cần sửa lại dict này
cho khớp thứ tự hàng thật trong sheet mới — không cần đụng vào game logic.
"""

from game.data.animations import AnimState, Direction

FULL_ROW_MAP = {
    (AnimState.IDLE, Direction.DOWN): 0,
    (AnimState.WALK, Direction.DOWN): 1,
    (AnimState.ATTACK, Direction.DOWN): 2,
    (AnimState.HURT, Direction.DOWN): 3,
    (AnimState.IDLE, Direction.UP): 4,
    (AnimState.WALK, Direction.UP): 5,
    (AnimState.ATTACK, Direction.UP): 6,
    (AnimState.HURT, Direction.UP): 7,
    (AnimState.IDLE, Direction.LEFT): 8,
    (AnimState.WALK, Direction.LEFT): 9,
    (AnimState.ATTACK, Direction.LEFT): 10,
    (AnimState.HURT, Direction.LEFT): 11,
    (AnimState.IDLE, Direction.RIGHT): 12,
    (AnimState.WALK, Direction.RIGHT): 13,
    (AnimState.ATTACK, Direction.RIGHT): 14,
    (AnimState.HURT, Direction.RIGHT): 15,
    (AnimState.DIE, None): 16,
}

# NPC chỉ sinh idle+walk x4 hướng (8 hàng) — dùng map rút gọn riêng
NPC_ROW_MAP = {
    (AnimState.IDLE, Direction.DOWN): 0,
    (AnimState.WALK, Direction.DOWN): 1,
    (AnimState.IDLE, Direction.UP): 2,
    (AnimState.WALK, Direction.UP): 3,
    (AnimState.IDLE, Direction.LEFT): 4,
    (AnimState.WALK, Direction.LEFT): 5,
    (AnimState.IDLE, Direction.RIGHT): 6,
    (AnimState.WALK, Direction.RIGHT): 7,
}

TILE_INDEX = {
    "GRASS": 0, "DIRT": 1, "GRASS_DIRT_EDGE": 2, "STONE_FLOOR": 3,
    "STONE_WALL": 4, "WATER": 5, "SAND": 6, "PATH": 7,
}
