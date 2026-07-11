"""
Hệ thống Tilemap & Render Map.
Map được lưu dưới dạng lưới 2D các mã tile (int), mỗi mã ánh xạ tới 1 loại
texture (đá, cỏ, đất, nước...). Hỗ trợ nhiều layer: nền (ground), vật cản
(collision), và trang trí (decoration, gồm bụi cỏ có animation riêng).
"""

from __future__ import annotations
import pygame
from enum import IntEnum
from typing import List, Dict, Tuple

TILE_SIZE = 32


class TileType(IntEnum):
    EMPTY = 0
    GRASS = 1
    DIRT = 2
    GRASS_DIRT_EDGE = 3   # tile chuyển tiếp cỏ-đất tự nhiên
    STONE_FLOOR = 4
    STONE_WALL = 5
    WATER = 6
    SAND = 7
    PATH = 8


# Tile nào chặn di chuyển (dùng cho collision check)
SOLID_TILES = {TileType.STONE_WALL, TileType.WATER}


class TileMap:
    def __init__(self, grid: List[List[int]], tileset: Dict[int, pygame.Surface]):
        self.grid = grid
        self.tileset = tileset
        self.height = len(grid)
        self.width = len(grid[0]) if grid else 0

    def is_solid(self, tile_x: int, tile_y: int) -> bool:
        if not (0 <= tile_y < self.height and 0 <= tile_x < self.width):
            return True
        return TileType(self.grid[tile_y][tile_x]) in SOLID_TILES

    def render(self, surface: pygame.Surface, camera_offset: Tuple[float, float]):
        cam_x, cam_y = camera_offset
        start_col = max(0, int(cam_x // TILE_SIZE))
        start_row = max(0, int(cam_y // TILE_SIZE))
        end_col = min(self.width, start_col + surface.get_width() // TILE_SIZE + 2)
        end_row = min(self.height, start_row + surface.get_height() // TILE_SIZE + 2)

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                tile_id = self.grid[row][col]
                texture = self.tileset.get(tile_id)
                if texture is None:
                    continue
                screen_x = col * TILE_SIZE - cam_x
                screen_y = row * TILE_SIZE - cam_y
                surface.blit(texture, (screen_x, screen_y))


class FoliagePatch:
    """Một cụm bụi cỏ trang trí có thể bị dẫm/chém, có animation riêng."""

    def __init__(self, tile_x: int, tile_y: int):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.state = "sway"  # "sway" | "trampled"
        self.trample_timer = 0.0

    def trigger_trample(self):
        self.state = "trampled"
        self.trample_timer = 0.4  # giây hồi lại trạng thái đung đưa

    def update(self, dt: float):
        if self.state == "trampled":
            self.trample_timer -= dt
            if self.trample_timer <= 0:
                self.state = "sway"


def generate_village_zone(width: int = 40, height: int = 30) -> List[List[int]]:
    """Sinh nhanh 1 map làng mẫu: nền cỏ + đường đất ở giữa + viền đá."""
    grid = [[TileType.GRASS for _ in range(width)] for _ in range(height)]
    for x in range(width):
        for y in range(height):
            if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                grid[y][x] = TileType.STONE_WALL
    # đường đất chạy ngang giữa làng
    mid_row = height // 2
    for x in range(1, width - 1):
        grid[mid_row][x] = TileType.PATH
        grid[mid_row - 1][x] = TileType.GRASS_DIRT_EDGE
        grid[mid_row + 1][x] = TileType.GRASS_DIRT_EDGE
    return [[int(t) for t in row] for row in grid]


def generate_castle_zone(width: int = 30, height: int = 30) -> List[List[int]]:
    """Sinh nhanh 1 map thành trì mẫu: sàn đá bên trong, tường đá bao quanh."""
    grid = [[TileType.STONE_FLOOR for _ in range(width)] for _ in range(height)]
    for x in range(width):
        for y in range(height):
            if x in (0, width - 1) or y in (0, height - 1):
                grid[y][x] = TileType.STONE_WALL
    return [[int(t) for t in row] for row in grid]


def generate_wild_zone(width: int = 50, height: int = 50) -> List[List[int]]:
    """Sinh nhanh 1 map khu vực quái vật hoang dã: cỏ + đất loang lổ tự nhiên."""
    import random
    grid = [[TileType.GRASS for _ in range(width)] for _ in range(height)]
    rng = random.Random(42)  # seed cố định để map ổn định giữa các lần build
    for _ in range(width * height // 12):
        x, y = rng.randint(1, width - 2), rng.randint(1, height - 2)
        grid[y][x] = TileType.DIRT
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 < nx < width - 1 and 0 < ny < height - 1 and rng.random() < 0.5:
                grid[ny][nx] = TileType.GRASS_DIRT_EDGE
    return [[int(t) for t in row] for row in grid]
