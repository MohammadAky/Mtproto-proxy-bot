#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   MTProto Proxy Bot - Auto Installer   ${NC}"
echo -e "${BLUE}========================================${NC}"

# ── 1. System update
echo -e "\n${YELLOW}[1/7] Updating system...${NC}"
apt-get update -y && apt-get upgrade -y

# ── 2. Install dependencies
echo -e "\n${YELLOW}[2/7] Installing system dependencies...${NC}"
apt-get install -y python3 python3-pip python3-venv curl git wget systemd

# ── 3. Install Node.js + PM2
echo -e "\n${YELLOW}[3/7] Installing Node.js and PM2...${NC}"
if ! command -v node &>/dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt-get install -y nodejs
fi
npm install -g pm2

# ── 4. Install mtg (MTProto proxy binary)
echo -e "\n${YELLOW}[4/7] Installing mtg proxy binary...${NC}"
MTG_VERSION="2.1.7"
ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ]; then
    MTG_ARCH="amd64"
elif [ "$ARCH" = "aarch64" ]; then
    MTG_ARCH="arm64"
else
    MTG_ARCH="386"
fi

MTG_URL="https://github.com/9seconds/mtg/releases/download/v${MTG_VERSION}/mtg-${MTG_VERSION}-linux-${MTG_ARCH}.tar.gz"
wget -q "$MTG_URL" -O /tmp/mtg.tar.gz
tar -xzf /tmp/mtg.tar.gz -C /tmp/
mv /tmp/mtg-${MTG_VERSION}-linux-${MTG_ARCH}/mtg /usr/local/bin/mtg
chmod +x /usr/local/bin/mtg
echo -e "${GREEN}mtg installed: $(mtg --version 2>&1 | head -1)${NC}"

# ── 5. Python virtual environment & packages
echo -e "\n${YELLOW}[5/7] Setting up Python environment...${NC}"
cd "$(dirname "$0")"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# ── 6. Setup .env file
echo -e "\n${YELLOW}[6/7] Setting up environment...${NC}"
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${RED}⚠  Please edit .env and add your BOT_TOKEN and ADMIN_IDS${NC}"
    echo -e "${YELLOW}   Run: nano .env${NC}"
else
    echo -e "${GREEN}.env already exists, skipping.${NC}"
fi

# Create data and logs dirs
mkdir -p data logs

# ── 7. Setup PM2
echo -e "\n${YELLOW}[7/7] Setting up PM2...${NC}"
pm2 startup systemd -u root --hp /root 2>/dev/null || true

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  ✅ Installation Complete!              ${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Next steps:"
echo -e "  1. Edit your config:  ${YELLOW}nano .env${NC}"
echo -e "  2. Start the bot:     ${YELLOW}pm2 start ecosystem.config.js${NC}"
echo -e "  3. Save PM2 list:     ${YELLOW}pm2 save${NC}"
echo -e "  4. View logs:         ${YELLOW}pm2 logs mtproto-proxy-bot${NC}"
echo ""