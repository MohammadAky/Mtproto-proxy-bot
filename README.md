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

## � Full Deployment Tutorial with PM2

### **Step 1: Connect to Your Server**

```bash
ssh root@your_server_ip
```

### **Step 2: Update System & Install Dependencies**

```bash
apt-get update && apt-get upgrade -y
apt-get install -y python3 python3-pip python3-venv git curl wget
```

### **Step 3: Install Node.js & PM2**

```bash
# Install Node.js LTS
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# Install PM2 globally
npm install -g pm2

# Verify installations
node --version
npm --version
pm2 --version
```

### **Step 4: Clone Your Project**

```bash
cd /root
git clone https://github.com/MohammadAky/Mtproto-proxy-bot.git
cd mtproto-proxy-bot
```

### **Step 5: Run the Installer**

```bash
chmod +x installer.sh
sudo ./installer.sh
```

This script will automatically:

- Install Python dependencies
- Download and setup `mtg` proxy binary
- Create a Python virtual environment
- Configure all necessary tools

### **Step 6: Configure Environment Variables**

```bash
nano .env
```

Add your configuration:

```env
BOT_TOKEN=123456789:ABCDefGhIjKlMnOpQrStUvWxYz
ADMIN_IDS=123456789,987654321
PROXY_SECRET_PREFIX=dd
PORT_RANGE_START=8443
PORT_RANGE_END=8500
LOG_LEVEL=INFO
```

**Press `Ctrl+O` → Enter → `Ctrl+X` to save and exit**

### **Step 7: Start the Bot with PM2**

```bash
# Start using ecosystem config
pm2 start ecosystem.config.js

# Verify it's running
pm2 status
```

### **Step 8: Configure PM2 to Auto-Start on Reboot**

```bash
# Generate startup script
pm2 startup

# Create PM2 startup service
sudo env PATH=$PATH:/usr/bin pm2 startup systemd -u root --hp /root

# Save your PM2 process list
pm2 save

# Verify auto-startup is configured
pm2 show mtproto-proxy-bot
```

### **Step 9: Monitor Your Bot**

```bash
# View real-time logs
pm2 logs mtproto-proxy-bot

# View process status
pm2 status

# Show detailed process info
pm2 info mtproto-proxy-bot

# View system resource usage
pm2 monit
```

---

## 🔁 PM2 Common Commands

```bash
# Basic operations
pm2 start ecosystem.config.js           # Start from config file
pm2 stop mtproto-proxy-bot              # Stop the bot
pm2 restart mtproto-proxy-bot           # Restart the bot
pm2 delete mtproto-proxy-bot            # Remove from PM2
pm2 reload mtproto-proxy-bot            # Graceful reload (zero-downtime)

# Monitoring & Logs
pm2 logs mtproto-proxy-bot              # View logs (tail mode)
pm2 logs mtproto-proxy-bot --lines 100  # View last 100 lines
pm2 logs mtproto-proxy-bot --err        # View only errors
pm2 status                              # List all processes
pm2 monit                               # Real-time monitoring dashboard

# Process management
pm2 save                                # Save current process list
pm2 resurrect                           # Restore saved processes
pm2 kill                                # Kill PM2 daemon
pm2 update                              # Update PM2
```

---

## 🛠 Troubleshooting

### **Bot won't start**

```bash
pm2 logs mtproto-proxy-bot
# Check for Python errors and .env configuration
```

### **Permission denied errors**

```bash
# Run with proper permissions
sudo pm2 start ecosystem.config.js
sudo pm2 save
```

### **Bot crashes on reboot**

```bash
# Ensure startup script is configured
sudo pm2 startup
sudo pm2 save
# Reboot to verify
sudo reboot
```

### **View error logs**

```bash
tail -f logs/pm2-error.log
tail -f logs/pm2-out.log
```

### **Restart all processes**

```bash
pm2 kill
pm2 start ecosystem.config.js
pm2 save
```

---

## 📊 Advanced PM2 Features

### **View CPU & Memory Usage**

```bash
pm2 monit              # Interactive dashboard
pm2 status             # Simple table view
```

### **Connect to PM2+ (Optional Cloud Monitoring)**

```bash
pm2 link <secret> <public_key>
# Visit https://app.pm2.io to monitor your bot remotely
```

### **Backup Process List**

```bash
pm2 save
# Your process list is saved in ~/.pm2/dump.pm2
```

### **Update Bot Code**

```bash
cd /root/mtproto-proxy-bot
git pull origin master
pm2 restart mtproto-proxy-bot
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
