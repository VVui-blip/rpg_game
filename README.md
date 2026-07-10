# Terminal Quest

Game 2D top-down RPG viết bằng **Python (Pygame)**, đóng gói APK Android qua
**python-for-android/Buildozer** (tự sinh lớp vỏ **Java** + build native **C++/NDK** bên dưới).
Có **terminal trong game** — vừa dùng để chơi (dùng item, nói chuyện NPC) vừa dùng để debug (dev mode).

## Chạy thử trên PC/Termux

```bash
pip install -r requirements.txt   # hoặc: pip install pygame --break-system-packages (trên Termux)
python main.py
```

**Điều khiển:**
- `WASD` / mũi tên: di chuyển
- `` ` `` (backtick): bật/tắt terminal
- `ESC`: thoát

**Lệnh terminal (người chơi):** `help`, `inventory` (`inv`), `use <item_id>`, `talk`, `stats`, `items`

**Lệnh terminal (dev, cần `DEV_MODE = True` trong `engine/settings.py`):**
`give <item_id> [số lượng]`, `tp <x> <y>`, `heal [số]`, `god`, `map_reload`, `eval <biểu thức python>`

## Cấu trúc dữ liệu game (Python thuần)

- `data/maps/map01.py` — lưới bản đồ, NPC, vị trí item spawn. Copy file này để tạo map mới.
- `data/items.py` — định nghĩa item (máu hồi, sát thương, loại...).
- Đổi map đang dùng: sửa `World("data.maps.map01")` trong `main.py`, hoặc gõ `map_reload` trong console sau khi sửa file để load lại không cần khởi động lại game.

## Asset ảnh

Đã có sẵn 1 bộ pixel-art 32x32 tự vẽ bằng code (`tools/generate_assets.py`, dùng Pillow) —
chạy `python tools/generate_assets.py` để tạo lại/chỉnh sửa. Xem `assets/images/README.md`
để biết tên file cần khớp.

**Nâng cấp lên asset chất lượng cao (free, CC0 — dùng thoải mái kể cả thương mại):**
- [Kenney – Roguelike/RPG Pack](https://kenney.nl/assets/roguelike-rpg-pack) — 1700 asset, rất hợp map top-down kiểu này
- [Kenney – RPG Urban Pack](https://kenney.nl/assets/rpg-urban-pack)
- [Kenney – RPG Base](https://kenney.nl/assets/rpg-base)
- [Kenney – 1-Bit Pack](https://kenney-assets.itch.io/1-bit-pack) — 1000+ tile phong cách roguelike
- [Kenney All-in-1 bundle](https://kenney-assets.itch.io/) — tải trọn bộ 1 lần

Tải về, resize ảnh về 32x32 (hoặc đổi `TILE_SIZE` trong `engine/settings.py` cho khớp),
đặt đúng tên file như bảng trong `assets/images/README.md` là engine tự nhận, không cần sửa code.

## Build ra APK

### Cách khuyên dùng: GitHub Actions (tự động, không cần build trên máy/Termux)
1. Push code lên GitHub (repo đã có sẵn `.github/workflows/build.yml`).
2. Vào tab **Actions** trên GitHub → chờ workflow "Build APK" chạy xong.
3. Tải APK ở phần **Artifacts** của lần chạy đó.

### Build local (Linux/WSL, không khuyến khích chạy thẳng trên Termux vì hay lỗi NDK)
```bash
pip install buildozer cython==0.29.36
buildozer android debug
```
File APK sẽ nằm trong `bin/`.

## Kiến trúc

```
main.py              # game loop, input, camera
engine/
  settings.py         # hằng số cấu hình
  assets.py            # load ảnh, fallback màu nếu thiếu asset
  world.py            # nạp/vẽ map từ file python trong data/maps/
  entity.py           # NPC, item rơi trên map
  player.py           # di chuyển, máu, túi đồ
  console.py          # UI terminal trong game
  commands.py         # bảng lệnh terminal (dev + player)
data/
  items.py            # định nghĩa item
  maps/map01.py       # dữ liệu bản đồ
```

## TODO gợi ý để làm "thật sự hay"
- Thêm animation (spritesheet) thay vì ảnh tĩnh trong `assets.py`
- Hệ thống combat (NPC quái, sát thương theo `sword` damage)
- Âm thanh (`pygame.mixer`)
- Save/load game (dump `player.inventory` + vị trí ra file json)
- Cutscene/dialog nhiều dòng thay vì 1 câu thoại
