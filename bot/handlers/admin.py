from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, Application
from bot.utils.decorators import admin_only
from bot.services.system import get_system_status
from bot.services.proxy_manager import ProxyManager

proxy_manager = ProxyManager()


@admin_only
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = get_system_status()
    proxies = proxy_manager.get_all_proxies()
    running = sum(1 for p in proxies if p.get("running"))

    msg = (
        f"🖥 <b>System Status</b>\n\n"
        f"🔧 CPU: <code>{info['cpu']}%</code>\n"
        f"💾 RAM: <code>{info['ram']}%</code>\n"
        f"💿 Disk: <code>{info['disk']}%</code>\n\n"
        f"📡 Total Proxies: <code>{len(proxies)}</code>\n"
        f"🟢 Running: <code>{running}</code>\n"
        f"🔴 Stopped: <code>{len(proxies) - running}</code>"
    )
    await update.message.reply_text(msg, parse_mode="HTML")


@admin_only
async def restart_proxy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /restart <proxy_id>")
        return
    proxy_id = context.args[0]
    result = proxy_manager.restart_proxy(proxy_id)
    if result["success"]:
        await update.message.reply_text(f"✅ Proxy <code>{proxy_id}</code> restarted.", parse_mode="HTML")
    else:
        await update.message.reply_text(f"❌ {result['error']}")


def register_admin_handlers(app: Application):
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("restart", restart_proxy))