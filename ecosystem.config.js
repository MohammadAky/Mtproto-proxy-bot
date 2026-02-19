module.exports = {
  apps: [
    {
      name: "mtproto-proxy-bot",
      script: "main.py",
      interpreter: "python3",
      watch: false,
      autorestart: true,
      max_restarts: 10,
      restart_delay: 5000,
      env: {
        NODE_ENV: "production",
      },
      log_date_format: "YYYY-MM-DD HH:mm:ss",
      out_file: "logs/pm2-out.log",
      error_file: "logs/pm2-error.log",
      merge_logs: true,
    },
  ],
};
