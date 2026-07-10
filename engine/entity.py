import pygame

from engine.settings import TILE_SIZE, COLORS
from engine.assets import load_image
from data.items import get_item


class NPC:
    def __init__(self, id, name, pos, dialog=""):
        self.id = id
        self.name = name
        self.pos = tuple(pos)
        self.dialog = dialog

    def draw(self, surface, camera_offset=(0, 0)):
        ox, oy = camera_offset
        tx, ty = self.pos
        img = load_image(f"npc_{self.id}.png", fallback_color=COLORS["npc"])
        surface.blit(img, (tx * TILE_SIZE - ox, ty * TILE_SIZE - oy))


class ItemDrop:
    def __init__(self, item_id, pos):
        self.item_id = item_id
        self.pos = tuple(pos)
        self.collected = False

    def draw(self, surface, camera_offset=(0, 0)):
        ox, oy = camera_offset
        tx, ty = self.pos
        data = get_item(self.item_id) or {}
        img = load_image(data.get("image", ""), fallback_color=data.get("color", COLORS["item"]))
        surface.blit(img, (tx * TILE_SIZE - ox, ty * TILE_SIZE - oy))
