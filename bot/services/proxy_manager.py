import json
import os
import secrets
import subprocess
import logging
from typing import Optional
from pathlib import Path

import config

logger = logging.getLogger(__name__)


class ProxyManager:
    def __init__(self):
        self.data_file = Path(config.DATA_FILE)
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            self._save([])

    def _load(self) -> list:
        try:
            with open(self.data_file) as f:
                return json.load(f)
        except Exception:
            return []

    def _save(self, data: list):
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=2)

    def _generate_secret(self, domain: Optional[str]) -> str:
        raw = secrets.token_hex(16)
        if domain:
            # fake-TLS secret: dd + hex(domain)
            hex_domain = domain.encode().hex()
            return f"dd{raw}{hex_domain}"
        return f"{config.PROXY_SECRET_PREFIX}{raw}" if config.PROXY_SECRET_PREFIX else raw

    def _pick_port(self) -> Optional[int]:
        used_ports = {p["port"] for p in self._load()}
        for port in range(config.PORT_RANGE_START, config.PORT_RANGE_END + 1):
            if port not in used_ports:
                return port
        return None

    def _build_link(self, server: str, port: int, secret: str) -> str:
        return f"https://t.me/proxy?server={server}&port={port}&secret={secret}"

    def _get_server_ip(self) -> str:
        try:
            result = subprocess.run(
                ["curl", "-s", "https://api.ipify.org"],
                capture_output=True, text=True, timeout=5
            )
            return result.stdout.strip() or "your-server-ip"
        except Exception:
            return "your-server-ip"

    def _start_mtproto(self, port: int, secret: str, sponsor: Optional[str]) -> dict:
        """Start mtg (MTProto proxy) process via systemd service or direct."""
        try:
            cmd = ["mtg", "simple-run", "-n", "0.0.0.0", str(port), secret]
            if sponsor:
                cmd += ["--ads-listen-addr", f"0.0.0.0:{port+1000}"]

            service_name = f"mtg-proxy-{port}"
            # Write a systemd service file
            service_content = f"""[Unit]
Description=MTProto Proxy on port {port}
After=network.target

[Service]
ExecStart={" ".join(cmd)}
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
"""
            service_path = f"/etc/systemd/system/{service_name}.service"
            with open(service_path, "w") as f:
                f.write(service_content)

            subprocess.run(["systemctl", "daemon-reload"], check=True)
            subprocess.run(["systemctl", "enable", service_name], check=True)
            subprocess.run(["systemctl", "start", service_name], check=True)
            return {"success": True, "service": service_name}
        except PermissionError:
            return {"success": False, "error": "Permission denied. Run bot as root or with sudo."}
        except FileNotFoundError:
            return {"success": False, "error": "mtg binary not found. Please install mtg first."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _stop_mtproto(self, port: int) -> dict:
        try:
            service_name = f"mtg-proxy-{port}"
            subprocess.run(["systemctl", "stop", service_name], check=True)
            subprocess.run(["systemctl", "disable", service_name], check=True)
            service_path = f"/etc/systemd/system/{service_name}.service"
            if os.path.exists(service_path):
                os.remove(service_path)
            subprocess.run(["systemctl", "daemon-reload"])
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _is_running(self, port: int) -> bool:
        try:
            result = subprocess.run(
                ["systemctl", "is-active", f"mtg-proxy-{port}"],
                capture_output=True, text=True
            )
            return result.stdout.strip() == "active"
        except Exception:
            return False

    def create_proxy(self, domain: Optional[str] = None, port: Optional[int] = None, sponsor: Optional[str] = None) -> dict:
        if port is None:
            port = self._pick_port()
            if port is None:
                return {"success": False, "error": "No available ports in configured range."}

        proxies = self._load()
        if any(p["port"] == port for p in proxies):
            return {"success": False, "error": f"Port {port} is already in use."}

        secret = self._generate_secret(domain)
        server = domain if domain else self._get_server_ip()
        link = self._build_link(server, port, secret)

        start_result = self._start_mtproto(port, secret, sponsor)

        proxy_id = secrets.token_hex(4)
        proxy = {
            "id": proxy_id,
            "port": port,
            "secret": secret,
            "domain": domain,
            "sponsor": sponsor,
            "server": server,
            "link": link,
            "running": start_result["success"],
            "service": start_result.get("service"),
        }
        proxies.append(proxy)
        self._save(proxies)

        if not start_result["success"]:
            logger.warning(f"Proxy saved but failed to start: {start_result['error']}")

        return {"success": True, "proxy": proxy}

    def get_all_proxies(self) -> list:
        proxies = self._load()
        for p in proxies:
            p["running"] = self._is_running(p["port"])
        return proxies

    def delete_proxy(self, proxy_id: str) -> dict:
        proxies = self._load()
        proxy = next((p for p in proxies if p["id"] == proxy_id), None)
        if not proxy:
            return {"success": False, "error": "Proxy not found."}

        self._stop_mtproto(proxy["port"])
        proxies = [p for p in proxies if p["id"] != proxy_id]
        self._save(proxies)
        return {"success": True}

    def restart_proxy(self, proxy_id: str) -> dict:
        proxies = self._load()
        proxy = next((p for p in proxies if p["id"] == proxy_id), None)
        if not proxy:
            return {"success": False, "error": "Proxy not found."}

        self._stop_mtproto(proxy["port"])
        result = self._start_mtproto(proxy["port"], proxy["secret"], proxy.get("sponsor"))
        proxy["running"] = result["success"]
        self._save(proxies)
        return result