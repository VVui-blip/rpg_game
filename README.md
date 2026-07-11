# Pixel Realm RPG

RPG 2D pixel art kết hợp yếu tố MMO (chat, nhiều người chơi cùng zone) và
Offline (chơi solo, PvE với NPC/quest offline vẫn hoạt động không cần server).

## Tech Stack
- **Python 3.11 + Pygame-CE**: engine 2D, xử lý toàn bộ game logic, render, animation.
- **Buildozer (python-for-android)**: đóng gói Python + Pygame thành APK.
- **GitHub Actions**: tự động build APK mỗi lần push/PR, upload artifact + tạo Release khi gắn tag.

## Chạy thử trên máy dev (Windows/macOS/Linux)
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
Điều khiển: `WASD`/mũi tên để di chuyển, `C` mở bảng trạng thái, `I` mở hòm đồ, `ESC` thoát.

## Build APK
### Cách 1 — Tự động qua GitHub Actions (khuyến nghị)
Chỉ cần `git push` lên nhánh `main`/`develop`, workflow `.github/workflows/build-apk.yml`
sẽ tự chạy và sinh file APK trong tab **Actions > Artifacts**. Gắn tag (`git tag v0.1.0 && git push --tags`)
để tự tạo GitHub Release kèm APK.

### Cách 2 — Build thủ công (Linux/WSL)
```bash
pip install buildozer cython
buildozer android debug
```
File APK debug xuất ra ở `bin/*.apk`.

## Cấu trúc dự án
```
rpg_project/
├── .github/workflows/build-apk.yml   # CI/CD build APK
├── buildozer.spec                    # Cấu hình đóng gói Android
├── main.py                           # Entry point, game loop
├── game/
│   ├── core/
│   │   ├── sprite_animation.py       # Quản lý sprite sheet + animation controller
│   │   ├── entity.py                 # Entity/Player/NPC/Mob + hệ thống chỉ số
│   │   └── map_renderer.py           # Tilemap, tile types, foliage animation
│   ├── data/
│   │   ├── animations.py             # 19 animation states + foliage anim
│   │   ├── mobs.py                   # 50 mob (5 tier x 10)
│   │   ├── npcs.py                   # 15 NPC với hội thoại/quest
│   │   └── player_customization.py   # 10 tóc / 10 trang phục / 10 vũ khí
│   ├── ui/hud.py                     # HP-MP bar, Chat, Minimap, Status, Inventory
│   └── maps/world_map.py             # Village / Wild Field / Forest / Cave / Castle / Dungeon
└── assets/                           # <-- CẦN BỔ SUNG (xem checklist bên dưới)
```

## ⚠️ Checklist trước khi build bản chính thức
Code hiện tại là **bộ khung logic đầy đủ** (data, entity, animation controller, map, UI) —
đã test pass toàn bộ (50 mob / 15 NPC / 10-10-10 customization / combat / map generation).
Player hiện đang render bằng hình chữ nhật placeholder vì **chưa có file ảnh sprite thật**.
Trước khi build APK phát hành, cần:

1. Tải asset pixel art 32x32 từ nguồn miễn phí (khuyến nghị: **Kenney.nl** — bộ *RPG Urban/Fantasy Pack*,
   hoặc **itch.io** tác giả *0x72*, *Sanctumpixel* — chọn bộ có tông màu tương đồng để không bị lệch style).
2. Đặt sprite sheet Player/NPC vào `assets/sprites/player/` và `assets/sprites/npc/`, đặt tile vào
   `assets/sprites/tiles/`, đặt mob vào `assets/sprites/mobs/`.
3. Khai báo `row_map` cho từng `SpriteSheetConfig` (xem `game/core/sprite_animation.py`) khớp với
   thứ tự hàng thật trong sheet đã tải — vì mỗi bộ asset có thứ tự animation khác nhau.
4. Thay `build_placeholder_tileset()` trong `main.py` bằng texture đá/cỏ/đất thật đã tải.
5. Cập nhật `icon.filename` trong `buildozer.spec` trỏ tới icon game thật.

## Ghi chú thiết kế
- 50 mob chia 5 tier độ khó (tier 1 = ngoại vi làng, tier 5 = boss hầm ngục thành trì),
  chỉ số scale dần để cân bằng progression.
- 15 NPC có vai trò riêng (thợ rèn, thương nhân, y sĩ, chỉ huy...) + 4 NPC có `quest_trigger` sẵn.
- Foliage (bụi cỏ) tách riêng khỏi tilemap chính, có state `sway`/`trampled` độc lập cho từng cụm.
