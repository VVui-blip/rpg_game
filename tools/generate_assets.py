"""
Sinh asset pixel art GỐC (tự vẽ bằng code, không phải asset tải về) cho toàn
bộ dự án, đảm bảo đồng bộ 1 bảng màu duy nhất -> không bao giờ lệch tông.

Cách hoạt động: vẽ trên canvas 16x16 "art pixel" bằng PIL (mỗi putpixel/rect
là 1 pixel nghệ thuật), sau đó upscale NEAREST x2 -> 32x32 để ra pixel art
sắc nét, đúng chuẩn 32x32 mà buildozer.spec / sprite_animation.py đang dùng.

Chạy: python3 tools/generate_assets.py
Kết quả ghi vào assets/sprites/...
"""

from __future__ import annotations
import os
import math
from PIL import Image, ImageDraw

BASE = 16          # canvas "art pixel" gốc
SCALE = 2           # upscale -> 32x32 thực tế trong game
OUT = 32

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITES = os.path.join(ROOT, "assets", "sprites")

# ---------------------------------------------------------------------------
# BẢNG MÀU DUY NHẤT CHO TOÀN BỘ GAME (Stardew/Pokemon-style: sáng, hài hòa)
# ---------------------------------------------------------------------------
PALETTE = {
    "grass":        (126, 200, 80),
    "grass_shadow": (100, 172, 62),
    "grass_hi":     (150, 220, 105),
    "dirt":         (169, 113, 74),
    "dirt_shadow":  (135, 88, 56),
    "stone":        (168, 168, 172),
    "stone_shadow": (125, 125, 130),
    "stone_hi":     (201, 201, 205),
    "water":        (93, 169, 233),
    "water_shadow": (62, 134, 199),
    "water_hi":     (150, 205, 250),
    "sand":         (234, 217, 160),
    "sand_shadow":  (208, 188, 128),
    "path":         (201, 178, 124),
    "path_shadow":  (172, 148, 98),
    "outline":      (40, 32, 28, 255),
}

TRANSPARENT = (0, 0, 0, 0)


def canvas() -> Image.Image:
    return Image.new("RGBA", (BASE, BASE), TRANSPARENT)


def upscale(img: Image.Image) -> Image.Image:
    return img.resize((OUT, OUT), Image.NEAREST)


def save_row_strip(frames: list, path: str):
    """Ghép danh sách frame (đã upscale) thành 1 hàng ngang -> lưu PNG."""
    w = OUT * len(frames)
    sheet = Image.new("RGBA", (w, OUT), TRANSPARENT)
    for i, f in enumerate(frames):
        sheet.paste(f, (i * OUT, 0), f)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    sheet.save(path)


def save_grid_sheet(rows: list, path: str):
    """rows: list các list-frame. Mỗi row -> 1 hàng, căn theo max frame count."""
    max_cols = max(len(r) for r in rows)
    sheet = Image.new("RGBA", (OUT * max_cols, OUT * len(rows)), TRANSPARENT)
    for ri, row in enumerate(rows):
        for ci, f in enumerate(row):
            sheet.paste(f, (ci * OUT, ri * OUT), f)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    sheet.save(path)


# ---------------------------------------------------------------------------
# TILESET: đá, cỏ, cỏ-đất đan xen, sàn đá, tường đá, nước, cát, đường đất
# ---------------------------------------------------------------------------
def dither_fill(draw, base_color, shadow_color, seed_offset=0):
    for y in range(BASE):
        for x in range(BASE):
            c = shadow_color if (x * 3 + y * 5 + seed_offset) % 7 == 0 else base_color
            draw.point((x, y), fill=c)


def tile_grass():
    img = canvas(); d = ImageDraw.Draw(img)
    dither_fill(d, PALETTE["grass"], PALETTE["grass_shadow"])
    for x, y in [(3, 4), (9, 2), (12, 10), (5, 12), (2, 9)]:
        d.point((x, y), fill=PALETTE["grass_hi"])
    return upscale(img)


def tile_dirt():
    img = canvas(); d = ImageDraw.Draw(img)
    dither_fill(d, PALETTE["dirt"], PALETTE["dirt_shadow"], seed_offset=2)
    for x, y in [(4, 5), (10, 3), (7, 11), (13, 8)]:
        d.point((x, y), fill=PALETTE["dirt_shadow"])
    return upscale(img)


def tile_grass_dirt_edge():
    img = canvas(); d = ImageDraw.Draw(img)
    dither_fill(d, PALETTE["grass"], PALETTE["grass_shadow"])
    for y in range(BASE):
        edge = int(3 * math.sin(y * 0.6)) + 8
        for x in range(edge, BASE):
            c = PALETTE["dirt_shadow"] if (x + y) % 5 == 0 else PALETTE["dirt"]
            d.point((x, y), fill=c)
    return upscale(img)


def tile_stone_floor():
    img = canvas(); d = ImageDraw.Draw(img)
    dither_fill(d, PALETTE["stone"], PALETTE["stone_shadow"], seed_offset=1)
    d.line([(0, 8), (15, 8)], fill=PALETTE["stone_shadow"])
    d.line([(8, 0), (8, 15)], fill=PALETTE["stone_shadow"])
    return upscale(img)


def tile_stone_wall():
    img = canvas(); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 15, 15], fill=PALETTE["stone_shadow"])
    for row, offset in enumerate([0, 4, 0, 4]):
        y = row * 4
        for x in range(-4 + offset, BASE, 8):
            d.rectangle([max(0, x), y, min(15, x + 6), min(15, y + 3)], fill=PALETTE["stone"])
    for x, y in [(2, 1), (10, 5), (5, 9), (13, 13)]:
        d.point((x, y), fill=PALETTE["stone_hi"])
    return upscale(img)


def tile_water():
    img = canvas(); d = ImageDraw.Draw(img)
    dither_fill(d, PALETTE["water"], PALETTE["water_shadow"], seed_offset=3)
    for y in (3, 8, 12):
        for x in range(0, BASE, 4):
            d.point(((x + y) % BASE, y), fill=PALETTE["water_hi"])
    return upscale(img)


def tile_sand():
    img = canvas(); d = ImageDraw.Draw(img)
    dither_fill(d, PALETTE["sand"], PALETTE["sand_shadow"], seed_offset=4)
    return upscale(img)


def tile_path():
    img = canvas(); d = ImageDraw.Draw(img)
    dither_fill(d, PALETTE["path"], PALETTE["path_shadow"], seed_offset=5)
    return upscale(img)


def build_tileset():
    frames = [tile_grass(), tile_dirt(), tile_grass_dirt_edge(), tile_stone_floor(),
              tile_stone_wall(), tile_water(), tile_sand(), tile_path()]
    save_row_strip(frames, os.path.join(SPRITES, "tiles", "tileset.png"))
    print("tileset.png -> 8 tiles (grass,dirt,grass_dirt_edge,stone_floor,stone_wall,water,sand,path)")


# ---------------------------------------------------------------------------
# HUMANOID (dùng chung cho Player & 15 NPC, đổi màu da/tóc/áo/quần)
# ---------------------------------------------------------------------------
def draw_humanoid(direction: str, pose: str, frame_i: int,
                   skin, hair, outfit, pants, weapon=None) -> Image.Image:
    """
    direction: down/up/left/right | pose: idle/walk/attack/hurt/die
    Vẽ 1 nhân vật chibi đơn giản, đồng bộ tỷ lệ 16x16.
    """
    img = canvas(); d = ImageDraw.Draw(img)

    bob = 0
    leg_offset = 0
    arm_swing = 0
    squash = 0
    tint = None

    if pose == "idle":
        bob = 1 if frame_i % 2 == 1 else 0
    elif pose == "walk":
        leg_offset = [(-1, 1), (0, 0), (1, 1), (0, 0)][frame_i % 4]
        bob = 1 if frame_i % 2 == 0 else 0
        arm_swing = leg_offset[0] if isinstance(leg_offset, tuple) else 0
    elif pose == "attack":
        arm_swing = min(frame_i, 3)
    elif pose == "hurt":
        tint = (214, 70, 70)
    elif pose == "die":
        squash = frame_i  # càng lớn càng "gục xuống"

    y0 = bob - squash // 2
    left_leg_dy = leg_offset[0] if pose == "walk" and isinstance(leg_offset, tuple) else 0
    right_leg_dy = leg_offset[1] if pose == "walk" and isinstance(leg_offset, tuple) else 0

    body_h = max(2, 6 - squash)

    # chân
    d.rectangle([5, 12 - y0 + left_leg_dy, 7, 15 - y0 + left_leg_dy], fill=pants)
    d.rectangle([9, 12 - y0 + right_leg_dy, 11, 15 - y0 + right_leg_dy], fill=pants)

    # thân (outfit)
    d.rectangle([4, 6 - y0, 12, 6 - y0 + body_h], fill=outfit)

    # tay (trái luôn cố định, phải là tay cầm vũ khí -> vươn ra khi attack)
    d.rectangle([2, 7 - y0, 4, 10 - y0], fill=skin)
    right_arm_x0 = 12 + min(arm_swing, 2)
    d.rectangle([right_arm_x0, 7 - y0, right_arm_x0 + 2, 10 - y0], fill=skin)

    # vũ khí (chỉ khi attack) — vươn xa dần theo arm_swing, giới hạn trong canvas
    if pose == "attack" and weapon:
        wx0 = min(13 + arm_swing, BASE - 2)
        d.rectangle([wx0, 5 - y0, wx0 + 1, 11 - y0], fill=weapon)

    # đầu + tóc
    d.rectangle([5, 2 - y0, 10, 6 - y0], fill=skin)
    if direction == "up":
        d.rectangle([5, 1 - y0, 10, 4 - y0], fill=hair)
    else:
        d.rectangle([4, 1 - y0, 10, 3 - y0], fill=hair)
        if direction == "down":
            d.point((6, 4 - y0), fill=PALETTE["outline"])
            d.point((9, 4 - y0), fill=PALETTE["outline"])
        elif direction == "left":
            d.point((5, 4 - y0), fill=PALETTE["outline"])
        elif direction == "right":
            d.point((9, 4 - y0), fill=PALETTE["outline"])

    if tint:
        # chỉ tô đỏ lên các pixel đã có nhân vật (alpha>0), không phủ toàn khung
        px = img.load()
        for yy in range(img.height):
            for xx in range(img.width):
                r, g, b, a = px[xx, yy]
                if a > 0:
                    px[xx, yy] = (
                        min(255, r + (tint[0] - r) // 2),
                        min(255, g + (tint[1] - g) // 2),
                        min(255, b + (tint[2] - b) // 2),
                        a,
                    )

    if direction == "left":
        img = img.transpose(Image.FLIP_LEFT_RIGHT)

    return upscale(img)


def build_character_sheet(path: str, skin, hair, outfit, pants, weapon=None,
                           states=("idle", "walk", "attack", "hurt")):
    """
    Sinh sheet nhân vật đầy đủ theo đúng row_map dùng trong game/core/sprite_animation.py:
    16 hàng (4 hướng x 4 state) + 1 hàng DIE chung.
    """
    from game.data.animations import DEFAULT_FRAME_COUNT, AnimState

    frame_counts = {
        "idle": DEFAULT_FRAME_COUNT[AnimState.IDLE],
        "walk": DEFAULT_FRAME_COUNT[AnimState.WALK],
        "attack": DEFAULT_FRAME_COUNT[AnimState.ATTACK],
        "hurt": DEFAULT_FRAME_COUNT[AnimState.HURT],
    }
    die_count = DEFAULT_FRAME_COUNT[AnimState.DIE]

    rows = []
    for direction in ("down", "up", "left", "right"):
        for state in states:
            n = frame_counts[state]
            row = [draw_humanoid(direction, state, i, skin, hair, outfit, pants, weapon)
                   for i in range(n)]
            rows.append(row)
    die_row = [draw_humanoid("down", "die", i, skin, hair, outfit, pants, weapon)
               for i in range(die_count)]
    rows.append(die_row)

    save_grid_sheet(rows, path)


# row_map chuẩn tương ứng với thứ tự sinh ở trên (dùng trong game code)
CHARACTER_ROW_MAP_COMMENT = """
row_map chuẩn cho mọi sheet nhân vật sinh bởi generate_assets.py:
(IDLE,DOWN)=0 (WALK,DOWN)=1 (ATTACK,DOWN)=2 (HURT,DOWN)=3
(IDLE,UP)=4   (WALK,UP)=5   (ATTACK,UP)=6   (HURT,UP)=7
(IDLE,LEFT)=8 (WALK,LEFT)=9 (ATTACK,LEFT)=10 (HURT,LEFT)=11
(IDLE,RIGHT)=12 (WALK,RIGHT)=13 (ATTACK,RIGHT)=14 (HURT,RIGHT)=15
(DIE,None)=16
"""


PLAYER_PALETTES = {
    "hair_01": (70, 45, 35), "hair_02": (200, 170, 90), "hair_03": (40, 40, 45),
    "hair_04": (150, 90, 60), "hair_05": (120, 60, 140), "hair_06": (210, 60, 60),
    "hair_07": (30, 30, 30), "hair_08": (230, 230, 235), "hair_09": (90, 130, 200),
    "hair_10": (60, 150, 110),
}
OUTFIT_COLORS = {
    "outfit_01": (150, 120, 90), "outfit_02": (110, 80, 55), "outfit_03": (90, 60, 150),
    "outfit_04": (90, 100, 110), "outfit_05": (70, 110, 70), "outfit_06": (140, 140, 150),
    "outfit_07": (35, 35, 40), "outfit_08": (170, 140, 90), "outfit_09": (200, 200, 210),
    "outfit_10": (190, 160, 60),
}
SKIN_TONES = [(247, 202, 159), (224, 172, 122), (198, 134, 90), (140, 95, 65)]


def build_player_assets():
    out_dir = os.path.join(SPRITES, "player")
    for i, (hair_id, hair_color) in enumerate(PLAYER_PALETTES.items()):
        skin = SKIN_TONES[i % len(SKIN_TONES)]
        pants = (70, 55, 45)
        build_character_sheet(
            os.path.join(out_dir, f"{hair_id}_base.png"),
            skin=skin, hair=hair_color, outfit=OUTFIT_COLORS["outfit_01"], pants=pants,
            weapon=(210, 210, 220),
        )
    # 1 sheet mặc định "player.png" dùng trực tiếp trong main.py
    build_character_sheet(
        os.path.join(out_dir, "player.png"),
        skin=SKIN_TONES[0], hair=PLAYER_PALETTES["hair_01"],
        outfit=OUTFIT_COLORS["outfit_01"], pants=(70, 55, 45), weapon=(210, 210, 220),
    )
    print(f"player/ -> {len(PLAYER_PALETTES) + 1} character sheets (32x32/frame, 17 rows)")


NPC_PALETTE_SEEDS = [
    ((247, 202, 159), (70, 45, 35), (150, 60, 60)),
    ((224, 172, 122), (30, 30, 30), (90, 60, 150)),
    ((198, 134, 90), (200, 170, 90), (70, 110, 70)),
    ((247, 202, 159), (210, 60, 60), (140, 140, 150)),
    ((140, 95, 65), (150, 90, 60), (170, 140, 90)),
    ((224, 172, 122), (90, 130, 200), (35, 35, 40)),
    ((198, 134, 90), (60, 150, 110), (110, 80, 55)),
    ((247, 202, 159), (230, 230, 235), (190, 160, 60)),
    ((224, 172, 122), (40, 40, 45), (90, 100, 110)),
    ((140, 95, 65), (120, 60, 140), (200, 200, 210)),
    ((198, 134, 90), (70, 45, 35), (90, 60, 150)),
    ((247, 202, 159), (200, 170, 90), (35, 35, 40)),
    ((224, 172, 122), (210, 60, 60), (190, 160, 60)),
    ((140, 95, 65), (30, 30, 30), (70, 100, 90)),
    ((198, 134, 90), (150, 90, 60), (140, 140, 150)),
]


def build_npc_assets():
    from game.data.npcs import NPC_DATA
    out_dir = os.path.join(SPRITES, "npc")
    for npc, (skin, hair, outfit) in zip(NPC_DATA, NPC_PALETTE_SEEDS):
        build_character_sheet(
            os.path.join(out_dir, f"{npc['id']}.png"),
            skin=skin, hair=hair, outfit=outfit, pants=(70, 55, 45),
            states=("idle", "walk"),  # NPC thường không cần attack/hurt đầy đủ
        )
    print(f"npc/ -> {len(NPC_DATA)} character sheets (idle+walk x4 hướng)")


# ---------------------------------------------------------------------------
# MOB: hình dạng blob/creature đơn giản, màu theo tier, kích thước tăng dần
# ---------------------------------------------------------------------------
TIER_COLORS = {
    1: (110, 200, 110),
    2: (90, 150, 210),
    3: (170, 110, 200),
    4: (220, 140, 60),
    5: (210, 60, 60),
}


def draw_mob_frame(tier: int, seed: int, pose: str, frame_i: int) -> Image.Image:
    img = canvas(); d = ImageDraw.Draw(img)
    base_color = TIER_COLORS.get(tier, (150, 150, 150))
    shade = tuple(max(0, c - 40) for c in base_color)
    size = 6 + tier  # blob lớn dần theo tier

    bob = 0
    if pose == "idle":
        bob = frame_i % 2
    elif pose == "walk":
        bob = [0, 1, 0, 1][frame_i % 4]

    cx, cy = 8, 9 - bob
    # thân blob (hình oval xấp xỉ bằng rectangle bo góc thủ công)
    r = size // 2
    for y in range(-r, r + 1):
        span = int((r * r - y * y) ** 0.5) if r > 0 else 0
        for x in range(-span, span + 1):
            shade_pixel = shade if (x + y + seed) % 5 == 0 else base_color
            px_pos = (cx + x, cy + y)
            if 0 <= px_pos[0] < BASE and 0 <= px_pos[1] < BASE:
                d.point(px_pos, fill=shade_pixel)
    # mắt
    eye_y = cy - 1
    for ex in (cx - 2, cx + 1):
        if 0 <= ex < BASE and 0 <= eye_y < BASE:
            d.rectangle([ex, eye_y, ex + 1, eye_y + 1], fill=(20, 20, 25))
    return upscale(img)


def build_mob_assets():
    from game.data.mobs import MOB_DATA
    out_dir = os.path.join(SPRITES, "mobs")
    for idx, mob in enumerate(MOB_DATA):
        idle = [draw_mob_frame(mob["tier"], idx, "idle", i) for i in range(2)]
        walk = [draw_mob_frame(mob["tier"], idx, "walk", i) for i in range(4)]
        save_grid_sheet([idle, walk], os.path.join(out_dir, f"{mob['id']}.png"))
    print(f"mobs/ -> {len(MOB_DATA)} sheets (row0=idle 2f, row1=walk 4f)")


# ---------------------------------------------------------------------------
# FOLIAGE: bụi cỏ (đung đưa + bị dẫm)
# ---------------------------------------------------------------------------
def draw_foliage_frame(mode: str, frame_i: int) -> Image.Image:
    img = canvas(); d = ImageDraw.Draw(img)
    sway = 0
    height = 10
    if mode == "sway":
        sway = [-1, 0, 1, 0][frame_i % 4]
    elif mode == "trampled":
        height = [10, 5, 2][min(frame_i, 2)]

    base_y = 15
    for i, bx in enumerate((5, 8, 11)):
        blade_h = height - (2 if i == 1 else 0)
        tip_x = bx + sway
        d.line([(bx, base_y), (tip_x, base_y - blade_h)], fill=PALETTE["grass_shadow"])
        d.line([(bx + 1, base_y), (tip_x + 1, base_y - blade_h)], fill=PALETTE["grass_hi"])
    return upscale(img)


def build_foliage_assets():
    sway = [draw_foliage_frame("sway", i) for i in range(4)]
    trampled = [draw_foliage_frame("trampled", i) for i in range(3)]
    save_grid_sheet([sway, trampled], os.path.join(SPRITES, "tiles", "foliage.png"))
    print("tiles/foliage.png -> row0=sway 4f, row1=trampled 3f")


# ---------------------------------------------------------------------------
# APP ICON: khiên pixel art đơn giản dùng làm icon.png cho buildozer.spec
# ---------------------------------------------------------------------------
def build_icon():
    size = 64  # canvas art-pixel, upscale x8 -> 512x512
    img = Image.new("RGBA", (size, size), TRANSPARENT)
    d = ImageDraw.Draw(img)
    cx = size // 2
    # nền tròn bo (giả lập bằng oval)
    d.ellipse([2, 2, size - 3, size - 3], fill=(150, 120, 90))
    d.ellipse([6, 6, size - 7, size - 7], fill=(126, 200, 80))
    # khiên
    shield_pts = [(cx, 12), (size - 16, 22), (size - 16, 38), (cx, size - 10),
                  (16, 38), (16, 22)]
    d.polygon(shield_pts, fill=(210, 60, 60), outline=(80, 30, 30))
    d.polygon([(cx, 18), (size - 22, 26), (size - 22, 36), (cx, size - 18),
               (22, 36), (22, 26)], fill=(230, 90, 90))
    # kiếm chéo giữa khiên
    d.line([(cx - 10, cx - 6), (cx + 10, cx + 10)], fill=(230, 230, 235), width=3)
    d.line([(cx - 12, cx + 8), (cx + 4, cx - 8)], fill=(200, 170, 60), width=3)

    icon_path = os.path.join(SPRITES, "icon.png")
    os.makedirs(os.path.dirname(icon_path), exist_ok=True)
    img.resize((512, 512), Image.NEAREST).save(icon_path)
    print("assets/sprites/icon.png -> 512x512 app icon")


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    build_tileset()
    build_player_assets()
    build_npc_assets()
    build_mob_assets()
    build_foliage_assets()
    build_icon()
    print(CHARACTER_ROW_MAP_COMMENT)
    print("\nHoàn tất sinh asset gốc vào assets/sprites/")
