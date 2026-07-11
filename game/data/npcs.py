"""
Định nghĩa 15 NPC tương tác được, mỗi NPC có vai trò (role), vị trí gợi ý
trong world, và cây hội thoại cơ bản (có thể mở rộng thêm option/quest).
"""

from game.core.entity import DialogueNode, DialogueOption

NPC_DATA = [
    {
        "id": "npc_001", "name": "Trưởng Làng Aldric", "role": "village_elder",
        "location": "village_square",
        "dialogue": DialogueNode(
            "Chào mừng, lữ khách. Ngôi làng này đang bị quái vật quấy phá ở phía tây.",
            [DialogueOption("Tôi sẽ giúp làng.", quest_trigger="quest_clear_west_field")]
        ),
    },
    {
        "id": "npc_002", "name": "Thợ Rèn Bran", "role": "blacksmith",
        "location": "village_forge",
        "dialogue": DialogueNode("Cần vũ khí tốt hơn không? Ta có thể rèn cho ngươi."),
    },
    {
        "id": "npc_003", "name": "Thương Nhân Elowen", "role": "merchant",
        "location": "village_market",
        "dialogue": DialogueNode("Hàng hóa tươi mới mỗi ngày, xem thử nhé!"),
    },
    {
        "id": "npc_004", "name": "Y Sĩ Maren", "role": "healer",
        "location": "village_clinic",
        "dialogue": DialogueNode("Ngươi bị thương à? Để ta chữa trị cho."),
    },
    {
        "id": "npc_005", "name": "Nông Dân Toby", "role": "farmer",
        "location": "village_farm",
        "dialogue": DialogueNode(
            "Đám chuột đồng phá hết ruộng lúa của ta rồi!",
            [DialogueOption("Để tôi xử lý đám chuột.", quest_trigger="quest_kill_field_mice")]
        ),
    },
    {
        "id": "npc_006", "name": "Thủ Thư Ilyana", "role": "librarian",
        "location": "village_library",
        "dialogue": DialogueNode("Trong sách cổ có ghi về một hầm ngục bị lãng quên..."),
    },
    {
        "id": "npc_007", "name": "Lính Gác Cổng Đông", "role": "guard",
        "location": "village_gate_east",
        "dialogue": DialogueNode("Đường phía đông khá an toàn, cứ đi thoải mái."),
    },
    {
        "id": "npc_008", "name": "Lính Gác Cổng Tây", "role": "guard",
        "location": "village_gate_west",
        "dialogue": DialogueNode("Cẩn thận, phía tây có sói xuất hiện gần đây."),
    },
    {
        "id": "npc_009", "name": "Chủ Quán Trọ Gareth", "role": "innkeeper",
        "location": "village_inn",
        "dialogue": DialogueNode("Nghỉ ngơi một đêm để hồi phục HP/MP đầy đủ chứ?"),
    },
    {
        "id": "npc_010", "name": "Thợ Săn Rowan", "role": "hunter",
        "location": "wild_forest_edge",
        "dialogue": DialogueNode(
            "Ta cần da sói để làm áo giáp. Giúp ta được không?",
            [DialogueOption("Đồng ý săn sói.", quest_trigger="quest_wolf_pelts")]
        ),
    },
    {
        "id": "npc_011", "name": "Pháp Sư Lão Thành Orin", "role": "mage_trainer",
        "location": "village_tower",
        "dialogue": DialogueNode("Ngươi có tố chất phép thuật đấy. Muốn học không?"),
    },
    {
        "id": "npc_012", "name": "Chỉ Huy Thành Trì Bertrand", "role": "castle_commander",
        "location": "castle_hall",
        "dialogue": DialogueNode(
            "Thành trì đang cần chiến binh dũng cảm để dẹp loạn Goblin.",
            [DialogueOption("Tôi tình nguyện.", quest_trigger="quest_goblin_uprising")]
        ),
    },
    {
        "id": "npc_013", "name": "Công Chúa Seraphine", "role": "royal_npc",
        "location": "castle_garden",
        "dialogue": DialogueNode("Ta chỉ mong hòa bình trở lại vương quốc này..."),
    },
    {
        "id": "npc_014", "name": "Ngục Tốt Gideon", "role": "dungeon_keeper",
        "location": "castle_dungeon_entrance",
        "dialogue": DialogueNode("Bên dưới có thứ gì đó rất nguy hiểm đang chờ."),
    },
    {
        "id": "npc_015", "name": "Lữ Khách Bí Ẩn", "role": "wandering_trader",
        "location": "random_roadside",
        "dialogue": DialogueNode("Ta có vài món hàng hiếm, không phải ai cũng thấy được ta đâu."),
    },
]


def get_npc_by_id(npc_id: str):
    return next((n for n in NPC_DATA if n["id"] == npc_id), None)
