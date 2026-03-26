"""Type aliases used by tasmota_http."""

from __future__ import annotations

from typing import Any

CommandResult = dict[str, Any] | list[Any] | str | int | float | bool | None
