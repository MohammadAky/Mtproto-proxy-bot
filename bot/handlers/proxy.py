import logging
from telegram import Update
from telegram.ext import (
    ContextTypes, CommandHandler, Application,
    ConversationHandler, MessageHandler, filters, CallbackQueryHandler
)
from bot.utils.decorators import admin_only
from bot.services.proxy_manager import ProxyManager
from bot.keyboards.inline import proxy_list_keyboard, confirm_keyboard

logger = logging.getLogger(__name__)

# Conversation states
ASK_DOMAIN, ASK_PORT, ASK_SPONSOR = range(3)

proxy_manager = ProxyManager()


@admin_only
async def create_proxy_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 <b>Step 1/3 — Domain (optional)</b>\n\n"
        "Send me the <b>domain name</b> for fake-TLS (e.g. <code>cdn.example.com</code>)\n"
        "Or send <code>-</code> to skip and use IP only.",
        parse_mode="HTML",
    )
    return ASK_DOMAIN


async def ask_port(update: Update, context: ContextTypes.DEFAULT_TYPE):
    domain = update.message.text.strip()
    context.user_data["domain"] = None if domain == "-" else domain

    await update.message.reply_text(
        "🔌 <b>Step 2/3 — Port</b>\n\n"
        "Send me the <b>port number</b> to use (e.g. <code>8443</code>)\n"
        "Or send <code>auto</code> to pick automatically.",
        parse_mode="HTML",
    )
    return ASK_PORT


async def ask_sponsor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    port_text = update.message.text.strip()
    if port_text.lower() == "auto":
        context.user_data["port"] = None
    else:
        try:
            port = int(port_text)
            if not (1024 <= port <= 65535):
                raise ValueError
            context.user_data["port"] = port
        except ValueError:
            await update.message.reply_text("❌ Invalid port. Please send a number between 1024–65535 or <code>auto</code>.", parse_mode="HTML")
            return ASK_PORT

    await update.message.reply_text(
        "📢 <b>Step 3/3 — Sponsor Channel</b>\n\n"
        "Send the <b>Telegram channel ID</b> for sponsorship (e.g. <code>-1001234567890</code>)\n"
        "Or send <code>-</code> to skip.",
        parse_mode="HTML",
    )
    return ASK_SPONSOR


async def finalize_proxy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sponsor_text = update.message.text.strip()
    context.user_data["sponsor"] = None if sponsor_text == "-" else sponsor_text

    domain = context.user_data.get("domain")
    port = context.user_data.get("port")
    sponsor = context.user_data.get("sponsor")

    await update.message.reply_text("⏳ Creating proxy, please wait...")

    result = proxy_manager.create_proxy(domain=domain, port=port, sponsor=sponsor)

    if result["success"]:
        p = result["proxy"]
        msg = (
            f"✅ <b>Proxy Created!</b>\n\n"
            f"🆔 ID: <code>{p['id']}</code>\n"
            f"🌐 Domain: <code>{p.get('domain') or 'N/A (IP mode)'}</code>\n"
            f"🔌 Port: <code>{p['port']}</code>\n"
            f"🔑 Secret: <code>{p['secret']}</code>\n"
            f"📢 Sponsor: <code>{p.get('sponsor') or 'None'}</code>\n\n"
            f"🔗 <b>Proxy Link:</b>\n<code>{p['link']}</code>\n\n"
            f"📲 <a href=\"{p['link']}\">Click to add in Telegram</a>"
        )
        await update.message.reply_text(msg, parse_mode="HTML", disable_web_page_preview=True)
    else:
        await update.message.reply_text(f"❌ Failed: {result['error']}")

    context.user_data.clear()
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("❌ Cancelled.")
    return ConversationHandler.END


@admin_only
async def list_proxies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    proxies = proxy_manager.get_all_proxies()
    if not proxies:
        await update.message.reply_text("📭 No proxies found.")
        return

    msg = "📋 <b>Active Proxies:</b>\n\n"
    for p in proxies:
        status = "🟢" if p.get("running") else "🔴"
        msg += (
            f"{status} <b>ID:</b> <code>{p['id']}</code>\n"
            f"   🔌 Port: <code>{p['port']}</code>\n"
            f"   🌐 Domain: <code>{p.get('domain') or 'IP only'}</code>\n"
            f"   🔗 <a href=\"{p['link']}\">Open Link</a>\n\n"
        )
    await update.message.reply_text(msg, parse_mode="HTML", disable_web_page_preview=True)


@admin_only
async def delete_proxy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /delete <proxy_id>")
        return

    proxy_id = context.args[0]
    result = proxy_manager.delete_proxy(proxy_id)
    if result["success"]:
        await update.message.reply_text(f"✅ Proxy <code>{proxy_id}</code> deleted.", parse_mode="HTML")
    else:
        await update.message.reply_text(f"❌ {result['error']}")


def register_proxy_handlers(app: Application):
    conv = ConversationHandler(
        entry_points=[CommandHandler("create", create_proxy_start)],
        states={
            ASK_DOMAIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_port)],
            ASK_PORT:   [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_sponsor)],
            ASK_SPONSOR:[MessageHandler(filters.TEXT & ~filters.COMMAND, finalize_proxy)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)
    app.add_handler(CommandHandler("list", list_proxies))
    app.add_handler(CommandHandler("delete", delete_proxy))