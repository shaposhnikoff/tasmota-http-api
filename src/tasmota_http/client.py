"""Tasmota HTTP command client.

Implements command execution against Tasmota web endpoint `/cm?cmnd=...`.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, build_opener

from .exceptions import TasmotaCommandError, TasmotaTransportError
from .types import CommandResult


@dataclass(slots=True)
class TasmotaClientConfig:
    host: str
    username: str | None = None
    password: str | None = None
    use_https: bool = False
    timeout: float = 10.0


class TasmotaClient:
    """Client for Tasmota HTTP command API."""

    def __init__(
        self,
        host: str,
        *,
        username: str | None = None,
        password: str | None = None,
        use_https: bool = False,
        timeout: float = 10.0,
    ) -> None:
        self.config = TasmotaClientConfig(
            host=host,
            username=username,
            password=password,
            use_https=use_https,
            timeout=timeout,
        )
        self._base_url = self._build_base_url(host, use_https)
        self._opener = build_opener()

    @staticmethod
    def _build_base_url(host: str, use_https: bool) -> str:
        cleaned = host.strip().rstrip("/")
        if cleaned.startswith("http://") or cleaned.startswith("https://"):
            return cleaned
        scheme = "https" if use_https else "http"
        return f"{scheme}://{cleaned}"

    def _build_command_url(self, command: str) -> str:
        query: dict[str, str] = {"cmnd": command}
        if self.config.username is not None:
            query["user"] = self.config.username
        if self.config.password is not None:
            query["password"] = self.config.password

        encoded = urlencode(query)
        return f"{self._base_url}/cm?{encoded}"

    def _http_get(self, url: str) -> str:
        req = Request(url=url, method="GET")
        try:
            with self._opener.open(req, timeout=self.config.timeout) as resp:
                return resp.read().decode("utf-8")
        except HTTPError as exc:
            msg = exc.read().decode("utf-8", errors="replace") if exc.fp else str(exc)
            raise TasmotaTransportError(f"HTTP error {exc.code}: {msg}") from exc
        except URLError as exc:
            raise TasmotaTransportError(f"Connection error: {exc.reason}") from exc
        except OSError as exc:
            raise TasmotaTransportError(f"Transport error: {exc}") from exc

    def send_command(self, command: str) -> CommandResult:
        """Send a single Tasmota command using `/cm?cmnd=<command>`."""
        normalized = command.strip()
        if not normalized:
            raise TasmotaCommandError("command must be a non-empty string")

        url = self._build_command_url(normalized)
        raw = self._http_get(url)

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw

    def backlog(self, commands: str | list[str]) -> CommandResult:
        """Run multiple commands via `Backlog` command."""
        if isinstance(commands, str):
            body = commands.strip()
        else:
            cleaned = [cmd.strip() for cmd in commands if cmd.strip()]
            body = "; ".join(cleaned)

        if not body:
            raise TasmotaCommandError("backlog commands must not be empty")

        return self.send_command(f"Backlog {body}")

    def status(self, code: int = 0) -> CommandResult:
        """Request status block (`Status <code>`)."""
        if code < 0:
            raise TasmotaCommandError("status code must be >= 0")
        return self.send_command(f"Status {code}")

    def power_get(self, channel: int = 1) -> CommandResult:
        """Get power state for a relay channel."""
        cmd = self._power_command_name(channel)
        return self.send_command(cmd)

    def power_set(self, on: bool, channel: int = 1) -> CommandResult:
        """Set power state for a relay channel."""
        cmd = self._power_command_name(channel)
        state = "ON" if on else "OFF"
        return self.send_command(f"{cmd} {state}")

    def power_toggle(self, channel: int = 1) -> CommandResult:
        """Toggle power state for a relay channel."""
        cmd = self._power_command_name(channel)
        return self.send_command(f"{cmd} TOGGLE")

    @staticmethod
    def _power_command_name(channel: int) -> str:
        if channel < 1:
            raise TasmotaCommandError("channel must be >= 1")
        return "Power" if channel == 1 else f"Power{channel}"
