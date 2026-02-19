from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, Application
from bot.utils.decorators import admin_only
from bot.keyboards.inline import main_menu_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Hello <b>{user.first_name}</b>!\n\n"
        "🔧 <b>MTProto Proxy Manager Bot</b>\n\n"
        "Use the menu below to manage your proxies.",
        parse_mode="HTML",
        reply_markup=main_menu_keyboard(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 <b>Commands:</b>\n\n"
        "/start - Show main menu\n"
        "/help - Show this help\n"
        "/create - Create a new proxy\n"
        "/list - List all proxies\n"
        "/delete &lt;id&gt; - Delete a proxy\n"
        "/status - System status\n",
        parse_mode="HTML",
    )


def register_common_handlers(app: Application):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))