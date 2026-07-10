import importlib
import pygame

from engine.settings import TILE_SIZE, COLORS
from engine.assets import load_image
from engine.entity import NPC, ItemDrop


class World:
    def __init__(self, map_module_name="data.maps.map01"):
        self.map_module_name = map_module_name
        self.npcs = []
        self.items = []
        self.load(map_module_name)

    def load(self, map_module_name):
        """Nạp map bằng cách import module python — đổi map = đổi tên module này."""
        mod = importlib.import_module(map_module_name)
        importlib.reload(mod)  # cho phép reload map lúc runtime qua console (map_reload)
        data = mod.generate()

        self.grid = data["grid"]
        self.legend = data["legend"]
        self.player_spawn = data["player_spawn"]
        self.width = len(self.grid[0])
        self.height = len(self.grid)

        self.npcs = [NPC(**n) for n in data["npcs"]]
        self.items = [ItemDrop(i["item_id"], i["pos"]) for i in data["item_spawns"]]

    def tile_at(self, tx, ty):
        if 0 <= ty < self.height and 0 <= tx < self.width:
            ch = self.grid[ty][tx]
            return self.legend.get(ch, self.legend["."])
        return {"walkable": False, "color_key": "wall", "image": "tile_wall.png"}

    def is_walkable(self, tx, ty):
        return self.tile_at(tx, ty)["walkable"]

    def draw(self, surface, camera_offset=(0, 0)):
        ox, oy = camera_offset
        for ty, row in enumerate(self.grid):
            for tx, ch in enumerate(row):
                tile = self.legend.get(ch, self.legend["."])
                img = load_image(tile["image"], fallback_color=COLORS[tile["color_key"]])
                surface.blit(img, (tx * TILE_SIZE - ox, ty * TILE_SIZE - oy))

        for item in self.items:
            if not item.collected:
                item.draw(surface, camera_offset)
        for npc in self.npcs:
            npc.draw(surface, camera_offset)

    def npc_near(self, tx, ty, radius=1):
        for npc in self.npcs:
            nx, ny = npc.pos
            if abs(nx - tx) <= radius and abs(ny - ty) <= radius:
                return npc
        return None

    def try_pickup(self, tx, ty):
        for item in self.items:
            if not item.collected and item.pos == (tx, ty):
                item.collected = True
                return item.item_id
        return None
