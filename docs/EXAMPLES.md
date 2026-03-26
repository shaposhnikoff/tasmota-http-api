# Usage Examples

## 1) Basic health check

```python
from tasmota_http import TasmotaClient

client = TasmotaClient("192.168.33.50")

status = client.status(0)
print(status)
```

## 2) Relay on/off flow

```python
from tasmota_http import TasmotaClient

client = TasmotaClient("192.168.33.50")

before = client.power_get()
print("Before:", before)

client.power_set(True)
after_on = client.power_get()
print("After ON:", after_on)

client.power_set(False)
after_off = client.power_get()
print("After OFF:", after_off)
```

## 3) Toggle relay

```python
from tasmota_http import TasmotaClient

client = TasmotaClient("192.168.33.50")
print(client.power_toggle())
```

## 4) Multi-channel relay

```python
from tasmota_http import TasmotaClient

client = TasmotaClient("192.168.33.50")

# Channel 2
client.power_set(True, channel=2)
print(client.power_get(channel=2))
```

## 5) Backlog command sequence

```python
from tasmota_http import TasmotaClient

client = TasmotaClient("192.168.33.50")

result = client.backlog(["Power1 OFF", "Delay 10", "Power1 ON"])
print(result)
```

## 6) Auth-enabled web commands

```python
from tasmota_http import TasmotaClient

client = TasmotaClient(
    "192.168.33.50",
    username="admin",
    password="secret",
)

print(client.status(0))
```

## 7) Raw command for unsupported features

```python
from tasmota_http import TasmotaClient

client = TasmotaClient("192.168.33.50")

print(client.send_command("TelePeriod 60"))
print(client.send_command("Status 8"))
```
