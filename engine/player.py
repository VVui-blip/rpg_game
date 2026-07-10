import pygame

from engine.settings import TILE_SIZE, COLORS
from engine.assets import load_image
from data.items import get_item


class Player:
    def __init__(self, tile_pos):
        self.tx, self.ty = tile_pos
        self.max_hp = 100
        self.hp = 100
        self.inventory = {}  # item_id -> số lượng
        self.move_cooldown = 0
        self.god_mode = False  # bật qua console dev: god

    @property
    def pos(self):
        return (self.tx, self.ty)

    def move(self, dx, dy, world):
        nx, ny = self.tx + dx, self.ty + dy
        if world.is_walkable(nx, ny) or self.god_mode:
            self.tx, self.ty = nx, ny
            picked = world.try_pickup(nx, ny)
            if picked:
                self.give_item(picked, 1)
            return True
        return False

    def give_item(self, item_id, qty=1):
        if not get_item(item_id):
            return False
        self.inventory[item_id] = self.inventory.get(item_id, 0) + qty
        return True

    def use_item(self, item_id):
        if self.inventory.get(item_id, 0) <= 0:
            return None
        data = get_item(item_id)
        if data and data["type"] == "consumable":
            self.hp = min(self.max_hp, self.hp + data.get("heal", 0))
        self.inventory[item_id] -= 1
        if self.inventory[item_id] <= 0:
            del self.inventory[item_id]
        return data

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def take_damage(self, amount):
        if self.god_mode:
            return
        self.hp = max(0, self.hp - amount)

    def teleport(self, tx, ty):
        self.tx, self.ty = tx, ty

    def draw(self, surface, camera_offset=(0, 0)):
        ox, oy = camera_offset
        img = load_image("player.png", fallback_color=COLORS["player"])
        surface.blit(img, (self.tx * TILE_SIZE - ox, self.ty * TILE_SIZE - oy))
