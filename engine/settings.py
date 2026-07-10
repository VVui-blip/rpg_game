"""
Cấu hình chung của game. Đổi số ở đây để chỉnh toàn bộ game.
"""

TILE_SIZE = 32
SCREEN_W, SCREEN_H = 800, 600
FPS = 60

TITLE = "Terminal Quest"

# Bật DEV_MODE = True để mở thêm lệnh chỉ dành cho dev trong console
DEV_MODE = True

# Màu fallback dùng khi chưa có ảnh asset thật (đặt ảnh vào assets/images/)
COLORS = {
    "bg": (18, 18, 24),
    "grass": (46, 125, 50),
    "wall": (66, 66, 66),
    "water": (30, 90, 160),
    "player": (255, 210, 60),
    "npc": (200, 60, 60),
    "item": (240, 240, 100),
    "console_bg": (0, 0, 0, 200),
    "console_text": (0, 255, 100),
    "console_text_dev": (255, 180, 0),
    "ui_text": (255, 255, 255),
}

KEY_TOGGLE_CONSOLE = "`"  # phím mở/đóng terminal trong game
