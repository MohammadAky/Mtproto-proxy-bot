import logging
import sys
from telegram.ext import ApplicationBuilder

import config
from bot.handlers.common import register_common_handlers
from bot.handlers.admin import register_admin_handlers
from bot.handlers.proxy import register_proxy_handlers

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/bot.log"),
    ],
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting MTProto Proxy Bot...")
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    register_common_handlers(app)
    register_admin_handlers(app)
    register_proxy_handlers(app)

    logger.info("Bot is polling...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()