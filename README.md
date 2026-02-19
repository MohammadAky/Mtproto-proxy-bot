# 🔧 MTProto Proxy Manager Bot

A Telegram bot to manage MTProto proxies on your VPS, powered by Python, `mtg`, and PM2.

---

## 📋 Requirements

- Ubuntu 20.04+ / Debian VPS
- Root access
- A Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- Your Telegram User ID (get from [@userinfobot](https://t.me/userinfobot))

---

## 🚀 Quick Deploy

```bash
git clone https://github.com/yourname/mtproto-proxy-bot.git
cd mtproto-proxy-bot
chmod +x installer.sh
sudo ./installer.sh
```

After install:

```bash
nano .env          # Set BOT_TOKEN and ADMIN_IDS
pm2 start ecosystem.config.js
pm2 save
pm2 logs mtproto-proxy-bot
```

---

## ⚙️ Configuration

Edit `.env`:

| Variable              | Description                        | Example       |
| --------------------- | ---------------------------------- | ------------- |
| `BOT_TOKEN`           | Your bot token from BotFather      | `123:ABC...`  |
| `ADMIN_IDS`           | Comma-separated admin Telegram IDs | `12345,67890` |
| `PROXY_SECRET_PREFIX` | `dd` for fake-TLS, empty for plain | `dd`          |
| `PORT_RANGE_START`    | Auto-pick port range start         | `8443`        |
| `PORT_RANGE_END`      | Auto-pick port range end           | `8500`        |
| `LOG_LEVEL`           | Logging verbosity                  | `INFO`        |

---

## 🤖 Bot Commands

| Command         | Description                 |
| --------------- | --------------------------- |
| `/start`        | Show main menu              |
| `/create`       | Start proxy creation wizard |
| `/list`         | List all proxies            |
| `/delete <id>`  | Delete a proxy              |
| `/status`       | Show system stats           |
| `/restart <id>` | Restart a proxy             |
| `/cancel`       | Cancel current operation    |

---

## 📲 Creating a Proxy (Step-by-Step)

1. Send `/create`
2. Enter a domain (or `-` to skip for IP-only mode)
3. Enter a port (or `auto` to pick automatically)
4. Enter a sponsor channel ID (or `-` to skip)
5. Bot returns a proxy link + secret you can share directly in Telegram

---

## 🔗 Proxy Link Format

```
https://t.me/proxy?server=HOST&port=PORT&secret=SECRET
```

Users can click this link to add the proxy directly in Telegram.

---

## 🔁 PM2 Management

```bash
pm2 start ecosystem.config.js     # Start the bot
pm2 stop mtproto-proxy-bot        # Stop the bot
pm2 restart mtproto-proxy-bot     # Restart the bot
pm2 logs mtproto-proxy-bot        # View logs
pm2 status                        # Check status
pm2 save                          # Save process list (survives reboot)
```

---

## 📁 Project Structure

```
mtproto-proxy-bot/
├── bot/
│   ├── handlers/       # Telegram command handlers
│   ├── services/       # Proxy management & system info
│   ├── utils/          # Decorators, helpers
│   └── keyboards/      # Inline keyboards
├── data/proxies.json   # Stored proxy configs
├── logs/               # Log files
├── config.py           # Loads .env settings
├── main.py             # Entry point
├── ecosystem.config.js # PM2 config
├── installer.sh        # One-click installer
└── README.md
```

---

## 🛡 Security Notes

- The bot only responds to users listed in `ADMIN_IDS`
- Keep your `.env` file private — never commit it
- The bot must run as root (or with sudo) to manage systemd services

---

## 📦 Under the Hood

- **Bot framework**: `python-telegram-bot` v21
- **MTProto binary**: [`mtg`](https://github.com/9seconds/mtg) v2
- **Process manager**: PM2 (Node.js)
- **Proxy management**: systemd services per proxy
