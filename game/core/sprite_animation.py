"""
Hệ thống quản lý Sprite Sheet & Animation.
Cắt sprite sheet thành từng frame theo lưới (grid), cache lại để tránh
load/crop lặp lại, và điều khiển playback (play/pause/loop) theo state.
"""

from __future__ import annotations
import pygame
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from game.data.animations import AnimState, Direction, DEFAULT_FRAME_COUNT, OMNIDIRECTIONAL_STATES

# Cache toàn cục để không load lại cùng 1 sheet nhiều lần
_SHEET_CACHE: Dict[str, pygame.Surface] = {}


def load_sheet(path: str) -> pygame.Surface:
    if path not in _SHEET_CACHE:
        _SHEET_CACHE[path] = pygame.image.load(path).convert_alpha()
    return _SHEET_CACHE[path]


def slice_row(sheet: pygame.Surface, row: int, frame_count: int,
              frame_w: int, frame_h: int) -> List[pygame.Surface]:
    """Cắt 1 hàng của sprite sheet thành danh sách frame."""
    frames = []
    for col in range(frame_count):
        rect = pygame.Rect(col * frame_w, row * frame_h, frame_w, frame_h)
        frames.append(sheet.subsurface(rect).copy())
    return frames


@dataclass
class SpriteSheetConfig:
    """Mô tả cách đọc 1 sprite sheet: kích thước frame và thứ tự hàng theo state."""
    path: str
    frame_width: int = 32
    frame_height: int = 32
    # map (AnimState, Direction) -> row index trong sheet
    row_map: Dict[Tuple[AnimState, Direction | None], int] = field(default_factory=dict)


class AnimationController:
    """
    Gắn vào 1 Entity (Player/NPC/Mob). Quản lý state hiện tại, hướng hiện tại,
    frame index, và tốc độ playback (fps).
    """

    def __init__(self, config: SpriteSheetConfig, fps: float = 8.0):
        self.config = config
        self.sheet = load_sheet(config.path)
        self.fps = fps
        self._frame_cache: Dict[Tuple[AnimState, Direction | None], List[pygame.Surface]] = {}

        self.state: AnimState = AnimState.IDLE
        self.direction: Direction = Direction.DOWN
        self.frame_index: float = 0.0
        self.loop: bool = True
        self.finished: bool = False

    def _frames_for(self, state: AnimState, direction: Direction) -> List[pygame.Surface]:
        key = (state, None if state in OMNIDIRECTIONAL_STATES else direction)
        if key not in self._frame_cache:
            row = self.config.row_map.get(key)
            if row is None:
                # fallback về IDLE nếu thiếu mapping, tránh crash game
                row = self.config.row_map.get((AnimState.IDLE, Direction.DOWN), 0)
            count = DEFAULT_FRAME_COUNT.get(state, 4)
            self._frame_cache[key] = slice_row(
                self.sheet, row, count, self.config.frame_width, self.config.frame_height
            )
        return self._frame_cache[key]

    def set_state(self, state: AnimState, direction: Direction | None = None, loop: bool = True):
        if direction is not None:
            self.direction = direction
        if state != self.state:
            self.state = state
            self.frame_index = 0.0
            self.finished = False
            self.loop = loop

    def update(self, dt: float):
        frames = self._frames_for(self.state, self.direction)
        if self.finished:
            return
        self.frame_index += self.fps * dt
        if self.frame_index >= len(frames):
            if self.loop:
                self.frame_index %= len(frames)
            else:
                self.frame_index = len(frames) - 1
                self.finished = True

    def current_frame(self) -> pygame.Surface:
        frames = self._frames_for(self.state, self.direction)
        return frames[int(self.frame_index) % len(frames)]
