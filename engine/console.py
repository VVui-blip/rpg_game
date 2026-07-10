import pygame

from engine.settings import SCREEN_W, COLORS
from engine.assets import load_font
from engine.commands import COMMANDS, DEV_COMMANDS


class Console:
    """
    Terminal overlay trong game. Nhấn phím ` để bật/tắt.
    - Người chơi thường: chỉ chạy được COMMANDS (help, inventory, use, talk, stats...)
    - Dev mode (settings.DEV_MODE): thêm DEV_COMMANDS (give, tp, heal, god, eval...)
    """

    HEIGHT = 220
    MAX_LOG = 8

    def __init__(self, dev_mode=False):
        self.active = False
        self.dev_mode = dev_mode
        self.input_text = ""
        self.log = ["Terminal sẵn sàng. Gõ 'help' để xem lệnh."]
        self.font = load_font(18)
        self.history = []
        self.history_index = -1

    def toggle(self):
        self.active = not self.active
        self.input_text = ""

    def handle_key(self, event, game):
        if not self.active:
            return
        if event.key == pygame.K_RETURN:
            self.run(self.input_text.strip(), game)
            self.input_text = ""
            self.history_index = -1
        elif event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        elif event.key == pygame.K_UP:
            if self.history:
                self.history_index = max(0, self.history_index - 1) if self.history_index >= 0 else len(self.history) - 1
                self.input_text = self.history[self.history_index]
        elif event.key == pygame.K_DOWN:
            if self.history and self.history_index >= 0:
                self.history_index += 1
                if self.history_index >= len(self.history):
                    self.history_index = -1
                    self.input_text = ""
                else:
                    self.input_text = self.history[self.history_index]
        elif event.unicode and event.unicode.isprintable():
            self.input_text += event.unicode

    def run(self, line, game):
        if not line:
            return
        self.history.append(line)
        self._print(f"> {line}", color=COLORS["console_text"])

        parts = line.split()
        name, args = parts[0], parts[1:]

        handler = COMMANDS.get(name)
        is_dev_cmd = False
        if handler is None and self.dev_mode:
            handler = DEV_COMMANDS.get(name)
            is_dev_cmd = True

        if handler is None:
            self._print(f"Lệnh không tồn tại: '{name}' (gõ 'help')", color=(255, 90, 90))
            return

        try:
            result = handler(game, args)
        except Exception as e:
            result = f"Lỗi khi chạy lệnh: {e}"

        if result:
            color = COLORS["console_text_dev"] if is_dev_cmd else COLORS["console_text"]
            self._print(result, color=color)

    def _print(self, text, color=None):
        for line in str(text).split("\n"):
            self.log.append((line, color or COLORS["console_text"]))
        self.log = self.log[-self.MAX_LOG:]

    def draw(self, surface):
        if not self.active:
            return
        overlay = pygame.Surface((SCREEN_W, self.HEIGHT), pygame.SRCALPHA)
        overlay.fill(COLORS["console_bg"])
        surface.blit(overlay, (0, 0))

        y = 10
        for entry in self.log:
            text, color = entry if isinstance(entry, tuple) else (entry, COLORS["console_text"])
            surf = self.font.render(text, True, color)
            surface.blit(surf, (10, y))
            y += 22

        prompt = self.font.render("> " + self.input_text + "_", True, COLORS["ui_text"])
        surface.blit(prompt, (10, self.HEIGHT - 26))
