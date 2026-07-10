import sys
import pygame

from engine.settings import SCREEN_W, SCREEN_H, FPS, TITLE, COLORS, DEV_MODE, TILE_SIZE
from engine.world import World
from engine.player import Player
from engine.console import Console


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dev_mode = DEV_MODE

        self.world = World("data.maps.map01")
        self.player = Player(self.world.player_spawn)
        self.console = Console(dev_mode=self.dev_mode)

        self.move_delay = 130  # ms giữa mỗi bước đi
        self._last_move = 0

    def camera_offset(self):
        cam_x = self.player.tx * TILE_SIZE - SCREEN_W // 2
        cam_y = self.player.ty * TILE_SIZE - SCREEN_H // 2
        return (cam_x, cam_y)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.unicode == "`":
                    self.console.toggle()
                    continue

                if self.console.active:
                    self.console.handle_key(event, self)
                    continue

                if event.key == pygame.K_ESCAPE:
                    self.running = False

        if not self.console.active:
            self._handle_movement()

    def _handle_movement(self):
        now = pygame.time.get_ticks()
        if now - self._last_move < self.move_delay:
            return
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1

        if dx or dy:
            if self.player.move(dx, dy, self.world):
                self._last_move = now

    def draw_hud(self):
        font = pygame.font.SysFont("consolas", 18)
        hud = font.render(
            f"HP: {self.player.hp}/{self.player.max_hp}   [`] Terminal   [ESC] Thoát", True, COLORS["ui_text"]
        )
        self.screen.blit(hud, (10, SCREEN_H - 26))

    def run(self):
        while self.running:
            self.handle_input()

            self.screen.fill(COLORS["bg"])
            self.world.draw(self.screen, self.camera_offset())
            self.player.draw(self.screen, self.camera_offset())
            self.draw_hud()
            self.console.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()
