from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Create Proxy", callback_data="create")],
        [InlineKeyboardButton("📋 List Proxies", callback_data="list"),
         InlineKeyboardButton("🖥 Status", callback_data="status")],
    ])


def confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Confirm", callback_data="confirm"),
         InlineKeyboardButton("❌ Cancel", callback_data="cancel")],
    ])


def proxy_list_keyboard(proxies: list) -> InlineKeyboardMarkup:
    buttons = []
    for p in proxies:
        status = "🟢" if p.get("running") else "🔴"
        buttons.append([InlineKeyboardButton(
            f"{status} Port {p['port']} (ID: {p['id']})",
            callback_data=f"proxy_{p['id']}"
        )])
    return InlineKeyboardMarkup(buttons)
