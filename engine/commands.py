"""
Bảng lệnh cho terminal trong game. Mỗi lệnh là 1 hàm nhận (game, args) -> str (kết quả in ra console).
Thêm lệnh mới = thêm 1 hàm + đăng ký vào COMMANDS/DEV_COMMANDS ở cuối file.
"""

from data.items import get_item, ITEMS


def cmd_help(game, args):
    lines = ["Lệnh người chơi: " + ", ".join(sorted(COMMANDS.keys()))]
    if game.dev_mode:
        lines.append("Lệnh dev: " + ", ".join(sorted(DEV_COMMANDS.keys())))
    return "\n".join(lines)


def cmd_inventory(game, args):
    p = game.player
    if not p.inventory:
        return "Túi đồ trống."
    return ", ".join(f"{get_item(i)['name']} x{q}" for i, q in p.inventory.items())


def cmd_use(game, args):
    if not args:
        return "Dùng: use <item_id>"
    item = game.player.use_item(args[0])
    if item is None:
        return f"Không có '{args[0]}' trong túi."
    return f"Đã dùng {item['name']}."

def cmd_talk(game, args):
    npc = game.world.npc_near(*game.player.pos, radius=1)
    if not npc:
        return "Không có ai gần đây để nói chuyện."
    return f"{npc.name}: {npc.dialog}"


def cmd_stats(game, args):
    p = game.player
    return f"HP: {p.hp}/{p.max_hp}  Vị trí: ({p.tx},{p.ty})"


def cmd_items_list(game, args):
    return ", ".join(ITEMS.keys())


# ---- Lệnh chỉ dành cho dev (DEV_MODE = True trong settings.py) ----

def cmd_give(game, args):
    if not args:
        return "Dùng: give <item_id> [số lượng]"
    item_id = args[0]
    qty = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1
    if game.player.give_item(item_id, qty):
        return f"Đã thêm {qty}x {item_id}."
    return f"Không tìm thấy item '{item_id}'."


def cmd_tp(game, args):
    if len(args) < 2:
        return "Dùng: tp <x> <y>"
    try:
        x, y = int(args[0]), int(args[1])
    except ValueError:
        return "Tọa độ phải là số nguyên."
    game.player.teleport(x, y)
    return f"Đã dịch chuyển tới ({x},{y})."


def cmd_heal(game, args):
    amt = int(args[0]) if args and args[0].isdigit() else game.player.max_hp
    game.player.heal(amt)
    return f"Hồi {amt} máu."


def cmd_god(game, args):
    game.player.god_mode = not game.player.god_mode
    return f"God mode: {'BẬT' if game.player.god_mode else 'TẮT'}"


def cmd_map_reload(game, args):
    game.world.load(game.world.map_module_name)
    return "Đã reload lại map từ file python."


def cmd_eval(game, args):
    """Chạy trực tiếp 1 dòng Python trong context game — CHỈ dev mode, cẩn thận khi dùng."""
    if not args:
        return "Dùng: eval <biểu thức python>"
    expr = " ".join(args)
    try:
        result = eval(expr, {"game": game, "player": game.player, "world": game.world})
        return str(result)
    except Exception as e:
        return f"Lỗi: {e}"


COMMANDS = {
    "help": cmd_help,
    "inventory": cmd_inventory,
    "inv": cmd_inventory,
    "use": cmd_use,
    "talk": cmd_talk,
    "stats": cmd_stats,
    "items": cmd_items_list,
}

DEV_COMMANDS = {
    "give": cmd_give,
    "tp": cmd_tp,
    "heal": cmd_heal,
    "god": cmd_god,
    "map_reload": cmd_map_reload,
    "eval": cmd_eval,
}
