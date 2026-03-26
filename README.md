# tasmota-http

A Python library for the local Tasmota HTTP command API.

The library provides:
- a single HTTP client for `http://<device>/cm?cmnd=...`;
- optional credential support via URL query (`user`, `password`);
- convenience methods for common operations (`Status`, `Power`, `Backlog`);
- a unified transport and command error layer.

## Contents

- Quick Start
- Authentication
- Supported Methods
- Error Handling
- API Documentation
- Usage Examples
- Build and Release
- Development and Tests

## Quick Start

### 1) Install

```bash
cd /mnt/NetworkBackupShare/api_doc/tasmota-http
python3 -m pip install -e .
```

### 2) Basic usage

```python
from tasmota_http import TasmotaClient, TasmotaCommandError, TasmotaTransportError

client = TasmotaClient("192.168.33.50")

try:
    status = client.status(0)
    before = client.power_get()
    client.power_set(True)
    after = client.power_get()

    print("status keys:", list(status.keys()) if isinstance(status, dict) else status)
    print("before:", before)
    print("after:", after)
except TasmotaCommandError as e:
    print(f"Command error: {e}")
except TasmotaTransportError as e:
    print(f"Transport error: {e}")
```

## Authentication

If your web commands require credentials:

```python
from tasmota_http import TasmotaClient

client = TasmotaClient(
    "192.168.33.50",
    username="admin",
    password="secret",
)
```

## Supported Methods (v1)

### Generic methods
- `send_command(command)`

### Convenience methods
- `backlog(commands)` -> `Backlog ...`
- `status(code=0)` -> `Status <code>`
- `power_get(channel=1)` -> `Power`/`Power<x>`
- `power_set(on, channel=1)` -> `Power ON|OFF`
- `power_toggle(channel=1)` -> `Power TOGGLE`

## Error Handling

- `TasmotaTransportError`
  - network errors;
  - HTTP errors.
- `TasmotaCommandError`
  - invalid command inputs before request (empty command, bad channel, etc.).

## API Documentation

- Detailed class and method reference: [docs/API.md](docs/API.md)
- Ready-to-run usage scenarios: [docs/EXAMPLES.md](docs/EXAMPLES.md)
- Build and release instructions (uv): [docs/BUILD.md](docs/BUILD.md)

## Development and Tests

Run tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Sources (local docs snapshot)

- `tasmota.github.io/docs/Commands/index.html`
- `tasmota.github.io/docs/MQTT/index.html`
