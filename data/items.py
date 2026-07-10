"""
Định nghĩa item bằng Python thuần — muốn thêm item mới chỉ cần thêm 1 dict vào đây,
không cần đụng vào engine.
"""

ITEMS = {
    "potion": {
        "name": "Bình máu",
        "type": "consumable",
        "heal": 20,
        "image": "potion.png",
        "color": (220, 40, 60),
    },
    "sword": {
        "name": "Kiếm gỗ",
        "type": "weapon",
        "damage": 5,
        "image": "sword.png",
        "color": (180, 180, 190),
    },
    "key_gold": {
        "name": "Chìa khóa vàng",
        "type": "key",
        "image": "key_gold.png",
        "color": (240, 200, 40),
    },
}


def get_item(item_id):
    return ITEMS.get(item_id)
