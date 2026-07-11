"""
Bảng dữ liệu 50 loại quái vật/mob. Mỗi entry là 1 dict template dùng để
spawn instance Mob (xem game/core/entity.py). Chia theo 5 tier độ khó
(Tier 1 = làng mạc ngoại ô, Tier 5 = hầm ngục/boss vùng), mỗi tier 10 mob.
"""

MOB_DATA = [
    # ---- Tier 1: Đồng cỏ ngoại ô (mob dễ, gần Village) ----
    {"id": "mob_001", "name": "Slime Xanh",        "tier": 1, "hp": 20,  "atk": 3,  "def": 1,  "exp": 5},
    {"id": "mob_002", "name": "Chuột Đồng",         "tier": 1, "hp": 15,  "atk": 2,  "def": 0,  "exp": 3},
    {"id": "mob_003", "name": "Ong Rừng",           "tier": 1, "hp": 12,  "atk": 4,  "def": 0,  "exp": 4},
    {"id": "mob_004", "name": "Thỏ Hoang",          "tier": 1, "hp": 10,  "atk": 1,  "def": 0,  "exp": 2},
    {"id": "mob_005", "name": "Gà Rừng",            "tier": 1, "hp": 14,  "atk": 2,  "def": 1,  "exp": 3},
    {"id": "mob_006", "name": "Nhện Cỏ",            "tier": 1, "hp": 18,  "atk": 3,  "def": 1,  "exp": 5},
    {"id": "mob_007", "name": "Slime Đỏ",           "tier": 1, "hp": 25,  "atk": 4,  "def": 1,  "exp": 6},
    {"id": "mob_008", "name": "Cây Nấm Độc",        "tier": 1, "hp": 22,  "atk": 3,  "def": 2,  "exp": 6},
    {"id": "mob_009", "name": "Dơi Hang Nhỏ",       "tier": 1, "hp": 16,  "atk": 3,  "def": 0,  "exp": 4},
    {"id": "mob_010", "name": "Sói Con",            "tier": 1, "hp": 24,  "atk": 5,  "def": 1,  "exp": 7},

    # ---- Tier 2: Rừng hoang / thảo nguyên ----
    {"id": "mob_011", "name": "Sói Xám",            "tier": 2, "hp": 40,  "atk": 7,  "def": 2,  "exp": 12},
    {"id": "mob_012", "name": "Gấu Rừng",           "tier": 2, "hp": 65,  "atk": 9,  "def": 4,  "exp": 20},
    {"id": "mob_013", "name": "Nhện Độc",           "tier": 2, "hp": 35,  "atk": 8,  "def": 1,  "exp": 14},
    {"id": "mob_014", "name": "Yêu Tinh Goblin",    "tier": 2, "hp": 38,  "atk": 6,  "def": 3,  "exp": 13},
    {"id": "mob_015", "name": "Cung Thủ Goblin",    "tier": 2, "hp": 30,  "atk": 9,  "def": 1,  "exp": 15},
    {"id": "mob_016", "name": "Rắn Độc",            "tier": 2, "hp": 28,  "atk": 8,  "def": 1,  "exp": 12},
    {"id": "mob_017", "name": "Cú Đêm Ma Thuật",    "tier": 2, "hp": 33,  "atk": 7,  "def": 2,  "exp": 14},
    {"id": "mob_018", "name": "Heo Rừng",           "tier": 2, "hp": 45,  "atk": 6,  "def": 3,  "exp": 13},
    {"id": "mob_019", "name": "Cây Ma",             "tier": 2, "hp": 50,  "atk": 5,  "def": 5,  "exp": 16},
    {"id": "mob_020", "name": "Golem Đất Nhỏ",      "tier": 2, "hp": 60,  "atk": 6,  "def": 6,  "exp": 18},

    # ---- Tier 3: Hang động / núi đá ----
    {"id": "mob_021", "name": "Golem Đá",           "tier": 3, "hp": 110, "atk": 12, "def": 10, "exp": 35},
    {"id": "mob_022", "name": "Dơi Chúa",           "tier": 3, "hp": 70,  "atk": 14, "def": 4,  "exp": 30},
    {"id": "mob_023", "name": "Người Sói",          "tier": 3, "hp": 95,  "atk": 15, "def": 6,  "exp": 34},
    {"id": "mob_024", "name": "Pháp Sư Hắc Ám",     "tier": 3, "hp": 60,  "atk": 18, "def": 3,  "exp": 32},
    {"id": "mob_025", "name": "Chiến Binh Orc",     "tier": 3, "hp": 100, "atk": 14, "def": 8,  "exp": 33},
    {"id": "mob_026", "name": "Cung Thủ Orc",       "tier": 3, "hp": 80,  "atk": 16, "def": 5,  "exp": 32},
    {"id": "mob_027", "name": "Bọ Cạp Khổng Lồ",    "tier": 3, "hp": 85,  "atk": 15, "def": 7,  "exp": 31},
    {"id": "mob_028", "name": "Xác Sống",           "tier": 3, "hp": 90,  "atk": 11, "def": 5,  "exp": 28},
    {"id": "mob_029", "name": "Hồn Ma Lang Thang",  "tier": 3, "hp": 55,  "atk": 17, "def": 2,  "exp": 30},
    {"id": "mob_030", "name": "Rồng Đất Nhỏ",       "tier": 3, "hp": 130, "atk": 16, "def": 9,  "exp": 40},

    # ---- Tier 4: Vùng nguy hiểm / gần thành trì địch ----
    {"id": "mob_031", "name": "Hiệp Sĩ Bóng Tối",   "tier": 4, "hp": 180, "atk": 22, "def": 14, "exp": 60},
    {"id": "mob_032", "name": "Pháp Sư Băng",       "tier": 4, "hp": 120, "atk": 26, "def": 8,  "exp": 58},
    {"id": "mob_033", "name": "Quái Nhân Lửa",      "tier": 4, "hp": 160, "atk": 24, "def": 10, "exp": 59},
    {"id": "mob_034", "name": "Griffin Hoang",      "tier": 4, "hp": 150, "atk": 23, "def": 9,  "exp": 57},
    {"id": "mob_035", "name": "Chằn Tinh",          "tier": 4, "hp": 220, "atk": 20, "def": 16, "exp": 62},
    {"id": "mob_036", "name": "Tướng Orc",          "tier": 4, "hp": 200, "atk": 25, "def": 13, "exp": 65},
    {"id": "mob_037", "name": "Thây Ma Giáp Sắt",   "tier": 4, "hp": 190, "atk": 19, "def": 18, "exp": 60},
    {"id": "mob_038", "name": "Rắn Hồ Nước",        "tier": 4, "hp": 140, "atk": 22, "def": 8,  "exp": 55},
    {"id": "mob_039", "name": "Cú Ma Khổng Lồ",     "tier": 4, "hp": 130, "atk": 27, "def": 7,  "exp": 58},
    {"id": "mob_040", "name": "Kỵ Sĩ Xương",        "tier": 4, "hp": 170, "atk": 24, "def": 12, "exp": 61},

    # ---- Tier 5: Boss / Hầm ngục thành trì ----
    {"id": "mob_041", "name": "Chúa Tể Goblin",     "tier": 5, "hp": 400, "atk": 30, "def": 20, "exp": 150},
    {"id": "mob_042", "name": "Rồng Lửa Cổ Đại",    "tier": 5, "hp": 800, "atk": 45, "def": 30, "exp": 400},
    {"id": "mob_043", "name": "Nữ Hoàng Nhện",      "tier": 5, "hp": 500, "atk": 35, "def": 22, "exp": 200},
    {"id": "mob_044", "name": "Tử Thần Kỵ Sĩ",      "tier": 5, "hp": 600, "atk": 40, "def": 25, "exp": 260},
    {"id": "mob_045", "name": "Pháp Sư Tối Cao",    "tier": 5, "hp": 350, "atk": 50, "def": 15, "exp": 240},
    {"id": "mob_046", "name": "Golem Cổ Đại",       "tier": 5, "hp": 900, "atk": 32, "def": 40, "exp": 300},
    {"id": "mob_047", "name": "Ác Quỷ Địa Ngục",    "tier": 5, "hp": 700, "atk": 42, "def": 28, "exp": 320},
    {"id": "mob_048", "name": "Vua Xác Sống",       "tier": 5, "hp": 650, "atk": 38, "def": 26, "exp": 290},
    {"id": "mob_049", "name": "Griffin Chúa",       "tier": 5, "hp": 550, "atk": 44, "def": 20, "exp": 270},
    {"id": "mob_050", "name": "Hắc Long Vương",     "tier": 5, "hp": 1200,"atk": 55, "def": 35, "exp": 600},
]


def get_mobs_by_tier(tier: int):
    return [m for m in MOB_DATA if m["tier"] == tier]


def get_mob_by_id(mob_id: str):
    return next((m for m in MOB_DATA if m["id"] == mob_id), None)
