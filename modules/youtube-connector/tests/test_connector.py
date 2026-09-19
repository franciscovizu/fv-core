import unittest
from urllib.parse import parse_qs, urlparse

from fv_youtube_connector import ConnectorConfig, YouTubeConnector


class FakeTransport:
    def __init__(self):
        self.calls = []

    def __call__(self, url, headers):
        self.calls.append((url, headers))
        return {"ok": True}


class ConnectorTests(unittest.TestCase):
    def setUp(self):
        self.transport = FakeTransport()
        self.connector = YouTubeConnector(
            ConnectorConfig(access_token="token-de-prueba"),
            transport=self.transport,
        )

    def test_authorized_channel_uses_mine(self):
        self.assertEqual(self.connector.get_authorized_channel(), {"ok": True})
        url, headers = self.transport.calls[-1]
        query = parse_qs(urlparse(url).query)
        self.assertEqual(query["mine"], ["true"])
        self.assertEqual(headers["Authorization"], "Bearer token-de-prueba")

    def test_analytics_uses_channel_mine(self):
        self.connector.query_channel_analytics("2026-09-01", "2026-09-19")
        url, _ = self.transport.calls[-1]
        query = parse_qs(urlparse(url).query)
        self.assertEqual(query["ids"], ["channel==MINE"])
        self.assertIn("views", query["metrics"][0])

    def test_video_limit_is_validated(self):
        with self.assertRaises(ValueError):
            self.connector.list_authorized_channel_videos("uploads", 51)


if __name__ == "__main__":
    unittest.main()
