from __future__ import annotations

import unittest
from urllib.error import URLError

from tasmota_http import TasmotaClient
from tasmota_http.exceptions import TasmotaCommandError, TasmotaTransportError


class _FailingOpener:
    def open(self, _req, timeout=0):
        raise URLError("network down")


class TasmotaClientTests(unittest.TestCase):
    def test_base_url_is_normalized(self):
        c1 = TasmotaClient("192.168.1.10")
        self.assertEqual(c1._base_url, "http://192.168.1.10")

        c2 = TasmotaClient("https://example.local/")
        self.assertEqual(c2._base_url, "https://example.local")

    def test_build_command_url_with_auth(self):
        client = TasmotaClient("192.168.1.10", username="admin", password="secret")
        url = client._build_command_url("Power ON")
        self.assertIn("/cm?", url)
        self.assertIn("cmnd=Power+ON", url)
        self.assertIn("user=admin", url)
        self.assertIn("password=secret", url)

    def test_send_command_returns_json_when_possible(self):
        client = TasmotaClient("192.168.1.10")
        client._http_get = lambda _url: '{"POWER":"ON"}'  # type: ignore[attr-defined]

        result = client.send_command("Power ON")
        self.assertEqual(result, {"POWER": "ON"})

    def test_send_command_returns_raw_text_when_non_json(self):
        client = TasmotaClient("192.168.1.10")
        client._http_get = lambda _url: "OK"  # type: ignore[attr-defined]

        result = client.send_command("Power ON")
        self.assertEqual(result, "OK")

    def test_send_command_rejects_empty_command(self):
        client = TasmotaClient("192.168.1.10")
        with self.assertRaises(TasmotaCommandError):
            client.send_command("   ")

    def test_backlog_from_list(self):
        client = TasmotaClient("192.168.1.10")
        captured = {}

        def fake_send(cmd):
            captured["cmd"] = cmd
            return {"ok": True}

        client.send_command = fake_send  # type: ignore[method-assign]
        client.backlog(["Power1 OFF", "Delay 10", "Power1 ON"])

        self.assertEqual(captured["cmd"], "Backlog Power1 OFF; Delay 10; Power1 ON")

    def test_status_uses_expected_command(self):
        client = TasmotaClient("192.168.1.10")
        captured = {}

        def fake_send(cmd):
            captured["cmd"] = cmd
            return {"Status": {}}

        client.send_command = fake_send  # type: ignore[method-assign]
        client.status(0)

        self.assertEqual(captured["cmd"], "Status 0")

    def test_power_set_for_multi_channel(self):
        client = TasmotaClient("192.168.1.10")
        captured = {}

        def fake_send(cmd):
            captured["cmd"] = cmd
            return {"POWER2": "ON"}

        client.send_command = fake_send  # type: ignore[method-assign]
        client.power_set(True, channel=2)

        self.assertEqual(captured["cmd"], "Power2 ON")

    def test_power_get_default_channel(self):
        client = TasmotaClient("192.168.1.10")
        captured = {}

        def fake_send(cmd):
            captured["cmd"] = cmd
            return {"POWER": "OFF"}

        client.send_command = fake_send  # type: ignore[method-assign]
        client.power_get()

        self.assertEqual(captured["cmd"], "Power")

    def test_invalid_channel_raises(self):
        client = TasmotaClient("192.168.1.10")
        with self.assertRaises(TasmotaCommandError):
            client.power_toggle(channel=0)

    def test_transport_errors_are_wrapped(self):
        client = TasmotaClient("192.168.1.10")
        client._opener = _FailingOpener()

        with self.assertRaises(TasmotaTransportError) as ctx:
            client.send_command("Status 0")

        self.assertIn("Connection error", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
