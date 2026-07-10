"""
Load ảnh từ assets/images/. Nếu file ảnh chưa tồn tại (bạn chưa bỏ asset vào),
tự động vẽ 1 ô màu để game vẫn chạy được, không bị crash.
"""

import os
import pygame

from engine.settings import TILE_SIZE, COLORS

ASSET_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "images")

_cache = {}


def load_image(name, size=(TILE_SIZE, TILE_SIZE), fallback_color=None):
    """
    name: tên file trong assets/images/, vd "player.png"
    fallback_color: RGB dùng nếu không tìm thấy ảnh
    """
    key = (name, size)
    if key in _cache:
        return _cache[key]

    path = os.path.join(ASSET_DIR, name)
    surf = None
    if os.path.isfile(path):
        try:
            surf = pygame.image.load(path).convert_alpha()
            surf = pygame.transform.scale(surf, size)
        except pygame.error:
            surf = None

    if surf is None:
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill(fallback_color or COLORS["wall"])

    _cache[key] = surf
    return surf


def load_font(size=18, name=None):
    """Font pixel-style nếu có file trong assets/fonts/, không thì dùng font hệ thống."""
    font_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "fonts")
    if name:
        path = os.path.join(font_dir, name)
        if os.path.isfile(path):
            return pygame.font.Font(path, size)
    return pygame.font.SysFont("consolas", size)
