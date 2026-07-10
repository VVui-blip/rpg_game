# Assets ảnh

Bỏ file PNG vào đây với đúng tên, game sẽ tự dùng thay cho ô màu fallback:

| File cần | Dùng cho |
|---|---|
| `player.png` | Nhân vật chính |
| `tile_grass.png` | Ô cỏ (`.` trong map) |
| `tile_wall.png` | Ô tường (`#`) |
| `tile_water.png` | Ô nước (`~`) |
| `npc_elder.png` | NPC "Trưởng làng" |
| `npc_merchant.png` | NPC "Thương nhân" |
| `potion.png`, `sword.png`, `key_gold.png` | Item (khớp id trong `data/items.py`) |

Kích thước khuyên dùng: **32x32px** (đổi `TILE_SIZE` trong `engine/settings.py` nếu muốn size khác).
Không có file thì game vẫn chạy bình thường — chỉ hiện ô màu thay ảnh (xem `engine/assets.py`).
