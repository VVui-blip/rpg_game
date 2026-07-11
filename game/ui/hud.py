"""
Hệ thống HUD/UI chính:
- HealthManaBar: thanh HP/MP góc trên trái
- ChatBox: khung chat cho MMO (tin nhắn hệ thống + người chơi khác)
- Minimap: bản đồ nhỏ góc trên phải
- StatusPanel: bảng chỉ số nhân vật (mở bằng phím C)
- InventoryPanel: hòm đồ dạng lưới (mở bằng phím I)

Toàn bộ panel dùng chung 1 bảng màu pastel/rực rỡ hài hòa kiểu
Stardew Valley: nền be nhạt (#F4E9D8), viền nâu gỗ (#8B5E3C),
điểm nhấn đỏ/vàng cho HP/MP.
"""

from __future__ import annotations
import pygame
from collections import deque
from typing import List, Tuple

COLOR_PANEL_BG = (244, 233, 216, 235)
COLOR_PANEL_BORDER = (139, 94, 60)
COLOR_HP = (214, 64, 64)
COLOR_HP_BG = (90, 30, 30)
COLOR_MP = (64, 120, 214)
COLOR_MP_BG = (25, 40, 90)
COLOR_TEXT = (60, 42, 30)
COLOR_TEXT_LIGHT = (250, 245, 235)


def draw_panel(surface: pygame.Surface, rect: pygame.Rect, radius: int = 8):
    panel = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(panel, COLOR_PANEL_BG, panel.get_rect(), border_radius=radius)
    pygame.draw.rect(panel, COLOR_PANEL_BORDER, panel.get_rect(), width=3, border_radius=radius)
    surface.blit(panel, rect.topleft)


class HealthManaBar:
    """Thanh HP/MP với hiệu ứng easing khi giá trị thay đổi (mượt hơn giật cục)."""

    def __init__(self, pos: Tuple[int, int] = (16, 16), width: int = 220):
        self.pos = pos
        self.width = width
        self.bar_height = 16
        self.display_hp_ratio = 1.0
        self.display_mp_ratio = 1.0

    def update(self, hp: int, max_hp: int, mp: int, max_mp: int, dt: float):
        target_hp = hp / max_hp if max_hp else 0
        target_mp = mp / max_mp if max_mp else 0
        ease = min(1.0, dt * 6)
        self.display_hp_ratio += (target_hp - self.display_hp_ratio) * ease
        self.display_mp_ratio += (target_mp - self.display_mp_ratio) * ease

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, name: str,
              hp: int, max_hp: int, mp: int, max_mp: int):
        x, y = self.pos
        draw_panel(surface, pygame.Rect(x - 8, y - 8, self.width + 16, 70))

        name_surf = font.render(name, True, COLOR_TEXT)
        surface.blit(name_surf, (x, y))

        bar_y = y + 20
        pygame.draw.rect(surface, COLOR_HP_BG, (x, bar_y, self.width, self.bar_height), border_radius=4)
        pygame.draw.rect(surface, COLOR_HP, (x, bar_y, int(self.width * self.display_hp_ratio), self.bar_height), border_radius=4)
        hp_text = font.render(f"HP {hp}/{max_hp}", True, COLOR_TEXT_LIGHT)
        surface.blit(hp_text, (x + 6, bar_y - 1))

        bar_y2 = bar_y + self.bar_height + 4
        pygame.draw.rect(surface, COLOR_MP_BG, (x, bar_y2, self.width, self.bar_height), border_radius=4)
        pygame.draw.rect(surface, COLOR_MP, (x, bar_y2, int(self.width * self.display_mp_ratio), self.bar_height), border_radius=4)
        mp_text = font.render(f"MP {mp}/{max_mp}", True, COLOR_TEXT_LIGHT)
        surface.blit(mp_text, (x + 6, bar_y2 - 1))


class ChatBox:
    """Khung chat MMO: hiển thị N tin nhắn gần nhất, hỗ trợ input gõ chat."""

    def __init__(self, pos: Tuple[int, int], size: Tuple[int, int], max_lines: int = 8):
        self.rect = pygame.Rect(pos, size)
        self.messages: deque[str] = deque(maxlen=max_lines)
        self.input_active = False
        self.input_buffer = ""

    def add_message(self, author: str, text: str, system: bool = False):
        prefix = "[Hệ Thống] " if system else f"{author}: "
        self.messages.append(prefix + text)

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        draw_panel(surface, self.rect)
        line_h = 18
        base_y = self.rect.bottom - 30
        for i, msg in enumerate(reversed(self.messages)):
            y = base_y - i * line_h
            if y < self.rect.top + 6:
                break
            text_surf = font.render(msg, True, COLOR_TEXT)
            surface.blit(text_surf, (self.rect.x + 8, y))

        if self.input_active:
            input_rect = pygame.Rect(self.rect.x, self.rect.bottom - 24, self.rect.width, 24)
            pygame.draw.rect(surface, (255, 255, 255), input_rect, border_radius=4)
            input_surf = font.render(self.input_buffer + "|", True, COLOR_TEXT)
            surface.blit(input_surf, (input_rect.x + 4, input_rect.y + 3))


class Minimap:
    """Bản đồ nhỏ góc trên phải, chấm chấm đại diện entity xung quanh player."""

    def __init__(self, pos: Tuple[int, int], size: int = 150, world_scale: float = 0.05):
        self.rect = pygame.Rect(pos, (size, size))
        self.world_scale = world_scale

    def draw(self, surface: pygame.Surface, player_pos: Tuple[float, float],
              nearby_entities: List[Tuple[float, float, str]]):
        draw_panel(surface, self.rect, radius=size_radius(self.rect.width))
        center = self.rect.center
        pygame.draw.circle(surface, (60, 160, 90), center, 5)  # player = chấm xanh lá

        color_map = {"mob": (200, 50, 50), "npc": (230, 190, 60), "player_other": (60, 120, 220)}
        for ex, ey, kind in nearby_entities:
            dx = (ex - player_pos[0]) * self.world_scale
            dy = (ey - player_pos[1]) * self.world_scale
            point = (center[0] + dx, center[1] + dy)
            if self.rect.collidepoint(point):
                pygame.draw.circle(surface, color_map.get(kind, (255, 255, 255)), point, 3)


def size_radius(w: int) -> int:
    return min(16, w // 8)


class StatusPanel:
    """Bảng trạng thái nhân vật (Level, ATK, DEF, EXP...), toggle bằng phím C."""

    def __init__(self, pos: Tuple[int, int] = (200, 120), size: Tuple[int, int] = (260, 220)):
        self.rect = pygame.Rect(pos, size)
        self.visible = False

    def toggle(self):
        self.visible = not self.visible

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, stats):
        if not self.visible:
            return
        draw_panel(surface, self.rect)
        lines = [
            f"Cấp độ: {stats.level}",
            f"HP: {stats.hp}/{stats.max_hp}",
            f"MP: {stats.mp}/{stats.max_mp}",
            f"Tấn công (ATK): {stats.atk}",
            f"Phòng thủ (DEF): {stats.defense}",
        ]
        for i, line in enumerate(lines):
            surf = font.render(line, True, COLOR_TEXT)
            surface.blit(surf, (self.rect.x + 14, self.rect.y + 14 + i * 24))


class InventoryPanel:
    """Hòm đồ dạng lưới ô vuông, toggle bằng phím I."""

    def __init__(self, pos: Tuple[int, int] = (200, 120), cols: int = 6, rows: int = 4, slot_size: int = 44):
        self.cols, self.rows, self.slot_size = cols, rows, slot_size
        pad = 10
        w = cols * (slot_size + pad) + pad
        h = rows * (slot_size + pad) + pad
        self.rect = pygame.Rect(pos, (w, h))
        self.visible = False

    def toggle(self):
        self.visible = not self.visible

    def draw(self, surface: pygame.Surface, items: List[dict]):
        if not self.visible:
            return
        draw_panel(surface, self.rect)
        pad = 10
        for row in range(self.rows):
            for col in range(self.cols):
                slot_rect = pygame.Rect(
                    self.rect.x + pad + col * (self.slot_size + pad),
                    self.rect.y + pad + row * (self.slot_size + pad),
                    self.slot_size, self.slot_size,
                )
                pygame.draw.rect(surface, (255, 250, 240), slot_rect, border_radius=6)
                pygame.draw.rect(surface, COLOR_PANEL_BORDER, slot_rect, width=2, border_radius=6)
                idx = row * self.cols + col
                if idx < len(items):
                    icon = items[idx].get("icon_surface")
                    if icon:
                        surface.blit(icon, slot_rect.topleft)
