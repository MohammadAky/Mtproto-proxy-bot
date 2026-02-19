import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
ADMIN_IDS: list[int] = [
    int(i.strip()) for i in os.getenv("ADMIN_IDS", "").split(",") if i.strip()
]
PROXY_SECRET_PREFIX: str = os.getenv("PROXY_SECRET_PREFIX", "dd")
PORT_RANGE_START: int = int(os.getenv("PORT_RANGE_START", 8443))
PORT_RANGE_END: int = int(os.getenv("PORT_RANGE_END", 8500))
DATA_FILE: str = os.getenv("DATA_FILE", "data/proxies.json")
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in .env file!")