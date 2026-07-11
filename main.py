"""
Entry point của game. Khởi tạo cửa sổ Pygame, load zone làng mạc mặc định,
tạo Player, và chạy game loop chính (input -> update -> render).

Ghi chú: đây là bộ khung (skeleton) đã nối đủ các hệ thống core (Entity,
Animation, TileMap, HUD). Sprite sheet thật (PNG) cần được đặt vào
assets/sprites/ theo đúng path khai báo trong SpriteSheetConfig trước khi
build APK, nếu không AnimationController sẽ báo lỗi load file.
"""

import os
import sys
import pygame

from game.core.entity import Player, Stats
from game.core.map_renderer import TileMap, TILE_SIZE
from game.core.sprite_animation import AnimationController, SpriteSheetConfig, load_sheet
from game.data.sprite_config import FULL_ROW_MAP, TILE_INDEX
from game.maps.world_map import ZONES
from game.ui.hud import HealthManaBar, ChatBox, Minimap, StatusPanel, InventoryPanel

SCREEN_W, SCREEN_H = 960, 540
FPS = 60

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "sprites")
PLAYER_SHEET_PATH = os.path.join(ASSETS_DIR, "player", "player.png")
TILESET_PATH = os.path.join(ASSETS_DIR, "tiles", "tileset.png")

FALLBACK_TILE_COLORS = {
    1: (110, 190, 90), 2: (150, 111, 74), 3: (130, 160, 82), 4: (170, 170, 170),
    5: (90, 90, 95), 6: (70, 120, 200), 7: (225, 210, 150), 8: (200, 175, 130),
}


def build_tileset() -> dict:
    """
    Cắt tileset.png thật (sinh bởi tools/generate_assets.py) thành từng ô 32x32.
    Nếu chưa chạy generate_assets.py hoặc thiếu file, tự động rơi về màu phẳng
    tạm thời để game vẫn chạy được thay vì crash.
    """
    if not os.path.exists(TILESET_PATH):
        print(f"[Cảnh báo] Không tìm thấy {TILESET_PATH} — dùng tile màu phẳng tạm thời. "
              f"Chạy `python tools/generate_assets.py` để sinh asset thật.")
        tileset = {}
        for tile_id, color in FALLBACK_TILE_COLORS.items():
            surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            surf.fill(color)
            tileset[tile_id] = surf
        return tileset

    sheet = load_sheet(TILESET_PATH)
    tileset = {}
    tile_enum_order = ["GRASS", "DIRT", "GRASS_DIRT_EDGE", "STONE_FLOOR",
                        "STONE_WALL", "WATER", "SAND", "PATH"]
    for tile_id, name in enumerate(tile_enum_order, start=1):
        col = TILE_INDEX[name]
        rect = pygame.Rect(col * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
        tileset[tile_id] = sheet.subsurface(rect).copy()
    return tileset


def build_player_animation():
    """Tạo AnimationController thật từ player.png. Trả None nếu thiếu file (fallback vẽ rect)."""
    if not os.path.exists(PLAYER_SHEET_PATH):
        print(f"[Cảnh báo] Không tìm thấy {PLAYER_SHEET_PATH} — Player sẽ vẽ bằng hình chữ nhật tạm thời. "
              f"Chạy `python tools/generate_assets.py` để sinh asset thật.")
        return None
    config = SpriteSheetConfig(path=PLAYER_SHEET_PATH, frame_width=32, frame_height=32, row_map=FULL_ROW_MAP)
    return AnimationController(config, fps=8.0)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Pixel Realm RPG")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 14)

    zone = ZONES["village"]
    grid = zone.grid_generator()
    tilemap = TileMap(grid, build_tileset())

    player_stats = Stats(hp=100, max_hp=100, mp=50, max_mp=50, atk=8, defense=2, exp_reward=0, level=1)
    player = Player(
        entity_id="player_local", name="Lữ Khách", x=zone.spawn_point[0] * TILE_SIZE,
        y=zone.spawn_point[1] * TILE_SIZE, stats=player_stats,
        hairstyle_id="hair_01", outfit_id="outfit_01", weapon_id="weapon_01",
        anim=build_player_animation(),
    )

    hp_mp_bar = HealthManaBar()
    chat = ChatBox(pos=(16, SCREEN_H - 160), size=(320, 150))
    chat.add_message("", "Chào mừng đến Làng Bình Minh!", system=True)
    minimap = Minimap(pos=(SCREEN_W - 166, 16))
    status_panel = StatusPanel()
    inventory_panel = InventoryPanel()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    status_panel.toggle()
                elif event.key == pygame.K_i:
                    inventory_panel.toggle()
                elif event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        player.move(dx, dy, dt)
        player.update(dt)

        hp_mp_bar.update(player.stats.hp, player.stats.max_hp, player.stats.mp, player.stats.max_mp, dt)

        camera_offset = (player.x - SCREEN_W / 2, player.y - SCREEN_H / 2)

        screen.fill((20, 20, 25))
        tilemap.render(screen, camera_offset)

        player_screen_pos = (SCREEN_W / 2 - 16, SCREEN_H / 2 - 16)
        if player.anim is not None:
            screen.blit(player.anim.current_frame(), player_screen_pos)
        else:
            pygame.draw.rect(screen, (230, 190, 120), (*player_screen_pos, 32, 32), border_radius=4)

        hp_mp_bar.draw(screen, font, player.name, player.stats.hp, player.stats.max_hp,
                       player.stats.mp, player.stats.max_mp)
        chat.draw(screen, font)
        minimap.draw(screen, (player.x, player.y), nearby_entities=[])
        status_panel.draw(screen, font, player.stats)
        inventory_panel.draw(screen, player.inventory)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


def _write_crash_log(exc: Exception):
    """Ghi traceback ra file trên bộ nhớ máy, không cần adb/logcat.
    Trên Android: /sdcard/Android/data/<package>/files/crash.txt
    Trên desktop: ./crash.txt (thư mục hiện tại)."""
    import traceback
    log_path = "crash.txt"
    try:
        from jnius import autoclass
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        log_path = PythonActivity.mActivity.getExternalFilesDir(None).getAbsolutePath() + "/crash.txt"
    except Exception:
        pass  # không phải Android (chạy desktop) -> dùng path mặc định
    try:
        with open(log_path, "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
    except Exception:
        pass  # nếu ghi file cũng lỗi thì thôi, ít nhất traceback vẫn in ra stdout


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        _write_crash_log(e)
        raise
