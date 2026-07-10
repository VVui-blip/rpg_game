"""
Bản đồ là 1 lưới ký tự (python thuần, không JSON/XML). Mỗi ký tự map sang tile
qua LEGEND. Muốn vẽ map mới: chỉnh GRID hoặc viết hàm generate() cho map random.
"""

LEGEND = {
    ".": {"walkable": True, "color_key": "grass", "image": "tile_grass.png"},
    "#": {"walkable": False, "color_key": "wall", "image": "tile_wall.png"},
    "~": {"walkable": False, "color_key": "water", "image": "tile_water.png"},
}

GRID = [
    "####################",
    "#..................#",
    "#..#####......##...#",
    "#..#...#......##...#",
    "#..#...#..~~~......#",
    "#..#####..~~~..###.#",
    "#..........~~..#.#.#",
    "#..............#...#",
    "#....####......#...#",
    "#....#..#..........#",
    "#....#..#....###...#",
    "#....####....#.#...#",
    "#............#.#...#",
    "####################",
]

PLAYER_SPAWN = (2, 1)  # (tile_x, tile_y)

NPCS = [
    {"id": "elder", "name": "Trưởng làng", "pos": (10, 3), "dialog": "Chào chiến binh, hãy cẩn thận với slime!"},
    {"id": "merchant", "name": "Thương nhân", "pos": (15, 9), "dialog": "Ghé mua ít bình máu không?"},
]

ITEM_SPAWNS = [
    {"item_id": "potion", "pos": (6, 8)},
    {"item_id": "sword", "pos": (16, 4)},
    {"item_id": "key_gold", "pos": (5, 11)},
]


def generate():
    """
    Ví dụ hàm sinh dữ liệu bằng logic Python thay vì set cứng —
    có thể gọi thay cho GRID nếu muốn map random về sau.
    """
    return {
        "grid": GRID,
        "legend": LEGEND,
        "player_spawn": PLAYER_SPAWN,
        "npcs": NPCS,
        "item_spawns": ITEM_SPAWNS,
    }
