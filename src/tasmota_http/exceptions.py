"""Exception hierarchy for Tasmota HTTP client."""

from __future__ import annotations


class TasmotaError(Exception):
    """Base class for all library errors."""


class TasmotaTransportError(TasmotaError):
    """Raised when HTTP transport fails."""


class TasmotaCommandError(TasmotaError):
    """Raised when command input is invalid before network call."""
