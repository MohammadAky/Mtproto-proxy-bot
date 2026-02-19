module.exports = {
  apps: [
    {
      name: "mtproto-proxy-bot",
      script: "main.py",
      interpreter: "/root/Mtproto-proxy-bot/venv/bin/python3",
      watch: false,
      autorestart: true,
      max_restarts: 10,
      restart_delay: 5000,
      cwd: "/root/Mtproto-proxy-bot",
      log_date_format: "YYYY-MM-DD HH:mm:ss",
      out_file: "logs/pm2-out.log",
      error_file: "logs/pm2-error.log",
      merge_logs: true,
    },
  ],
};
