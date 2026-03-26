# API Reference

## Module `tasmota_http`

### `TasmotaClient(host, *, username=None, password=None, use_https=False, timeout=10.0)`

Client for the local Tasmota HTTP command API.

Parameters:
- `host: str`
  - IP/hostname (`192.168.33.50`) or full URL (`http://192.168.33.50`).
- `username: str | None`
  - optional username to pass as `user` query parameter.
- `password: str | None`
  - optional password to pass as `password` query parameter.
- `use_https: bool`
  - use HTTPS when `host` is provided without a scheme.
- `timeout: float`
  - HTTP request timeout in seconds.

Host normalization behavior:
- `"192.168.1.10"` -> `http://192.168.1.10`
- `"https://example.local/"` -> `https://example.local`

### `send_command(command) -> CommandResult`

Runs a command via GET `/cm?cmnd=<command>`.

Return behavior:
- if response is valid JSON -> returns parsed JSON;
- otherwise returns raw text response.

Raises:
- `TasmotaCommandError` for empty command;
- `TasmotaTransportError` for HTTP/network errors.

### `backlog(commands) -> CommandResult`

Runs multiple commands through `Backlog`.

Input:
- `str`: used as-is after trim.
- `list[str]`: joined with `; `.

Example command sent:
- `Backlog Power1 OFF; Delay 10; Power1 ON`

### `status(code=0) -> CommandResult`

Runs `Status <code>`.

### `power_get(channel=1) -> CommandResult`

Runs `Power` for channel 1, or `Power<x>` for channel > 1.

### `power_set(on, channel=1) -> CommandResult`

Runs `Power ON|OFF` (or `Power<x> ON|OFF`).

### `power_toggle(channel=1) -> CommandResult`

Runs `Power TOGGLE` (or `Power<x> TOGGLE`).

## Exceptions

### `TasmotaError`
Base exception class for this library.

### `TasmotaTransportError(TasmotaError)`
Transport-level exception.

Typical cases:
- network/connectivity issues;
- HTTP status errors.

### `TasmotaCommandError(TasmotaError)`
Raised when command input is invalid before network call.

Handling example:

```python
from tasmota_http import TasmotaClient, TasmotaCommandError

client = TasmotaClient("192.168.33.50")

try:
    client.power_toggle(channel=0)
except TasmotaCommandError as e:
    print(e)
```
