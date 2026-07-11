"""
World map tổng: định nghĩa các zone (Village, Castle, Wild Zone) và
điểm spawn/kết nối (portal) giữa chúng.
"""

from dataclasses import dataclass
from typing import Dict, Tuple

from game.core.map_renderer import (
    generate_village_zone, generate_castle_zone, generate_wild_zone
)


@dataclass
class Zone:
    zone_id: str
    name: str
    grid_generator: callable
    spawn_point: Tuple[int, int]
    mob_tier_range: Tuple[int, int]  # tier mob xuất hiện trong zone này (0,0 = không có mob)


ZONES: Dict[str, Zone] = {
    "village": Zone(
        zone_id="village",
        name="Làng Bình Minh",
        grid_generator=generate_village_zone,
        spawn_point=(20, 15),
        mob_tier_range=(0, 0),
    ),
    "wild_field": Zone(
        zone_id="wild_field",
        name="Cánh Đồng Hoang",
        grid_generator=lambda: generate_wild_zone(50, 50),
        spawn_point=(5, 5),
        mob_tier_range=(1, 2),
    ),
    "wild_forest": Zone(
        zone_id="wild_forest",
        name="Khu Rừng Rậm",
        grid_generator=lambda: generate_wild_zone(60, 60),
        spawn_point=(10, 10),
        mob_tier_range=(2, 3),
    ),
    "mountain_cave": Zone(
        zone_id="mountain_cave",
        name="Hang Núi Đá",
        grid_generator=lambda: generate_wild_zone(45, 45),
        spawn_point=(4, 4),
        mob_tier_range=(3, 4),
    ),
    "castle": Zone(
        zone_id="castle",
        name="Thành Trì Hoàng Gia",
        grid_generator=generate_castle_zone,
        spawn_point=(15, 25),
        mob_tier_range=(0, 0),
    ),
    "castle_dungeon": Zone(
        zone_id="castle_dungeon",
        name="Hầm Ngục Thành Trì",
        grid_generator=lambda: generate_castle_zone(35, 35),
        spawn_point=(2, 2),
        mob_tier_range=(4, 5),
    ),
}

# Portal kết nối giữa các zone: (zone_from, tile_x, tile_y) -> zone_to
PORTALS = {
    ("village", 39, 15): "wild_field",
    ("wild_field", 0, 25): "village",
    ("wild_field", 49, 25): "wild_forest",
    ("wild_forest", 0, 30): "wild_field",
    ("village", 20, 0): "castle",
    ("castle", 15, 29): "village",
    ("castle", 29, 15): "castle_dungeon",
}
