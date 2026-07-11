"""
Dữ liệu tùy biến khởi đầu cho Player: 10 kiểu tóc, 10 bộ trang phục,
10 loại vũ khí khởi đầu. Mỗi entry trỏ tới layer sprite riêng để
game ghép lớp (layered rendering) lên khung hình Player.
"""

HAIRSTYLES = [
    {"id": "hair_01", "name": "Tóc Ngắn Rối", "sprite_layer": "hair/short_messy.png"},
    {"id": "hair_02", "name": "Tóc Đuôi Ngựa", "sprite_layer": "hair/ponytail.png"},
    {"id": "hair_03", "name": "Tóc Xoăn Bồng", "sprite_layer": "hair/curly.png"},
    {"id": "hair_04", "name": "Đầu Trọc", "sprite_layer": "hair/bald.png"},
    {"id": "hair_05", "name": "Tóc Dài Thẳng", "sprite_layer": "hair/long_straight.png"},
    {"id": "hair_06", "name": "Tóc Undercut", "sprite_layer": "hair/undercut.png"},
    {"id": "hair_07", "name": "Tóc Búi Cao", "sprite_layer": "hair/topknot.png"},
    {"id": "hair_08", "name": "Tóc Xù Punk", "sprite_layer": "hair/spiky.png"},
    {"id": "hair_09", "name": "Tóc Tết Bím", "sprite_layer": "hair/braided.png"},
    {"id": "hair_10", "name": "Tóc Che Mắt", "sprite_layer": "hair/eye_cover.png"},
]

OUTFITS = [
    {"id": "outfit_01", "name": "Áo Dân Thường", "sprite_layer": "outfit/villager.png"},
    {"id": "outfit_02", "name": "Giáp Da Du Hành", "sprite_layer": "outfit/leather_traveler.png"},
    {"id": "outfit_03", "name": "Áo Choàng Pháp Sư", "sprite_layer": "outfit/mage_robe.png"},
    {"id": "outfit_04", "name": "Giáp Chiến Binh Nhẹ", "sprite_layer": "outfit/light_warrior.png"},
    {"id": "outfit_05", "name": "Trang Phục Cung Thủ", "sprite_layer": "outfit/archer.png"},
    {"id": "outfit_06", "name": "Giáp Hiệp Sĩ Nặng", "sprite_layer": "outfit/heavy_knight.png"},
    {"id": "outfit_07", "name": "Áo Sát Thủ Đen", "sprite_layer": "outfit/assassin.png"},
    {"id": "outfit_08", "name": "Trang Phục Nông Dân", "sprite_layer": "outfit/farmer.png"},
    {"id": "outfit_09", "name": "Áo Choàng Thầy Tu", "sprite_layer": "outfit/priest_robe.png"},
    {"id": "outfit_10", "name": "Giáp Hoàng Gia", "sprite_layer": "outfit/royal_armor.png"},
]

STARTING_WEAPONS = [
    {"id": "weapon_01", "name": "Kiếm Gỗ Tập Luyện", "type": "sword", "base_atk": 2, "sprite_layer": "weapon/wooden_sword.png"},
    {"id": "weapon_02", "name": "Kiếm Sắt", "type": "sword", "base_atk": 5, "sprite_layer": "weapon/iron_sword.png"},
    {"id": "weapon_03", "name": "Cung Ngắn", "type": "bow", "base_atk": 4, "sprite_layer": "weapon/short_bow.png"},
    {"id": "weapon_04", "name": "Trượng Phép", "type": "staff", "base_atk": 3, "sprite_layer": "weapon/mage_staff.png"},
    {"id": "weapon_05", "name": "Rìu Chiến", "type": "axe", "base_atk": 6, "sprite_layer": "weapon/battle_axe.png"},
    {"id": "weapon_06", "name": "Dao Găm Đôi", "type": "dagger", "base_atk": 3, "sprite_layer": "weapon/dual_dagger.png"},
    {"id": "weapon_07", "name": "Thương Dài", "type": "spear", "base_atk": 5, "sprite_layer": "weapon/spear.png"},
    {"id": "weapon_08", "name": "Búa Chiến", "type": "hammer", "base_atk": 7, "sprite_layer": "weapon/war_hammer.png"},
    {"id": "weapon_09", "name": "Nỏ Cơ Khí", "type": "crossbow", "base_atk": 5, "sprite_layer": "weapon/crossbow.png"},
    {"id": "weapon_10", "name": "Sách Phép Cổ", "type": "grimoire", "base_atk": 4, "sprite_layer": "weapon/spellbook.png"},
]


def get_by_id(catalog: list, item_id: str):
    return next((item for item in catalog if item["id"] == item_id), None)
