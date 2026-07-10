"""
Tự vẽ asset pixel-art 32x32 bằng Pillow, không cần tải gì từ mạng.
Chạy: python tools/generate_assets.py
Muốn asset đẹp hơn/đa dạng hơn, xem README.md phần "Asset free chất lượng cao".
"""

import os
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "images")
S = 32  # kích thước 1 tile


def new_canvas():
    return Image.new("RGBA", (S, S), (0, 0, 0, 0))


def save(img, name):
    os.makedirs(OUT, exist_ok=True)
    img.save(os.path.join(OUT, name))


def outline_rect(d, box, fill, outline=(0, 0, 0, 255), width=1):
    d.rectangle(box, fill=fill, outline=outline, width=width)


def tile_grass():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S, S], fill=(58, 145, 61, 255))
    for i in range(0, S, 4):
        d.rectangle([i, 0, i + 1, S], fill=(50, 130, 53, 120))
    for (x, y) in [(4, 6), (12, 20), (22, 10), (26, 24), (8, 26)]:
        d.line([x, y, x, y - 4], fill=(30, 100, 35, 255), width=1)
        d.line([x - 2, y - 2, x, y - 5], fill=(30, 100, 35, 255), width=1)
    save(img, "tile_grass.png")


def tile_wall():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S, S], fill=(90, 90, 96, 255))
    brick_h = 8
    for row, y in enumerate(range(0, S, brick_h)):
        offset = 0 if row % 2 == 0 else 8
        for x in range(-8 + offset, S, 16):
            d.rectangle([x, y, x + 15, y + brick_h - 1], outline=(50, 50, 55, 255), width=1)
    save(img, "tile_wall.png")


def tile_water():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S, S], fill=(35, 100, 175, 255))
    for y in range(4, S, 8):
        d.arc([2, y, 14, y + 6], start=200, end=340, fill=(120, 190, 230, 200), width=1)
        d.arc([16, y + 4, 28, y + 10], start=200, end=340, fill=(120, 190, 230, 200), width=1)
    save(img, "tile_water.png")


def player():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    # thân
    outline_rect(d, [9, 14, 22, 28], (60, 110, 220, 255))
    # đầu
    d.ellipse([9, 3, 22, 16], fill=(250, 210, 170, 255), outline=(0, 0, 0, 255))
    # tóc
    d.pieslice([8, 2, 23, 13], 180, 360, fill=(90, 60, 40, 255))
    # mắt
    d.point([13, 9], fill=(0, 0, 0, 255))
    d.point([18, 9], fill=(0, 0, 0, 255))
    # tay
    d.rectangle([6, 16, 9, 24], fill=(60, 110, 220, 255), outline=(0, 0, 0, 255))
    d.rectangle([22, 16, 25, 24], fill=(60, 110, 220, 255), outline=(0, 0, 0, 255))
    # chân
    d.rectangle([11, 27, 14, 31], fill=(40, 40, 60, 255))
    d.rectangle([17, 27, 20, 31], fill=(40, 40, 60, 255))
    save(img, "player.png")


def npc(name, shirt_color, hair_color):
    img = new_canvas()
    d = ImageDraw.Draw(img)
    outline_rect(d, [9, 14, 22, 28], shirt_color)
    d.ellipse([9, 3, 22, 16], fill=(240, 200, 160, 255), outline=(0, 0, 0, 255))
    d.pieslice([8, 2, 23, 13], 180, 360, fill=hair_color)
    d.point([13, 9], fill=(0, 0, 0, 255))
    d.point([18, 9], fill=(0, 0, 0, 255))
    d.rectangle([6, 16, 9, 24], fill=shirt_color, outline=(0, 0, 0, 255))
    d.rectangle([22, 16, 25, 24], fill=shirt_color, outline=(0, 0, 0, 255))
    d.rectangle([11, 27, 14, 31], fill=(70, 50, 40, 255))
    d.rectangle([17, 27, 20, 31], fill=(70, 50, 40, 255))
    save(img, f"npc_{name}.png")


def potion():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    d.rectangle([13, 6, 18, 10], fill=(140, 140, 150, 255), outline=(0, 0, 0, 255))
    d.polygon([(10, 12), (21, 12), (24, 26), (7, 26)], fill=(220, 40, 60, 255), outline=(0, 0, 0, 255))
    d.ellipse([12, 15, 18, 20], fill=(255, 130, 140, 200))
    save(img, "potion.png")


def sword():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    d.polygon([(16, 2), (19, 20), (13, 20)], fill=(200, 200, 210, 255), outline=(0, 0, 0, 255))
    d.rectangle([9, 19, 23, 23], fill=(120, 80, 40, 255), outline=(0, 0, 0, 255))
    d.rectangle([14, 22, 18, 30], fill=(90, 60, 30, 255), outline=(0, 0, 0, 255))
    save(img, "sword.png")


def key_gold():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    d.ellipse([6, 6, 16, 16], outline=(230, 190, 40, 255), width=3)
    d.rectangle([14, 12, 26, 16], fill=(240, 200, 50, 255), outline=(0, 0, 0, 255))
    d.rectangle([20, 16, 22, 20], fill=(240, 200, 50, 255))
    d.rectangle([24, 16, 26, 19], fill=(240, 200, 50, 255))
    save(img, "key_gold.png")


def icon():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S, S], fill=(30, 30, 40, 255))
    d.text((6, 10), ">_", fill=(0, 255, 100, 255))
    save(img, "icon.png")


if __name__ == "__main__":
    tile_grass()
    tile_wall()
    tile_water()
    player()
    npc("elder", (150, 70, 160, 255), (200, 200, 200, 255))
    npc("merchant", (60, 150, 90, 255), (40, 30, 20, 255))
    potion()
    sword()
    key_gold()
    icon()
    print(f"Đã tạo asset trong {OUT}")
