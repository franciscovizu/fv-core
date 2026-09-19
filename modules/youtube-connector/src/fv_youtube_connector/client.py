import json
from typing import Any, Callable
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .config import ConnectorConfig

Transport = Callable[[str, dict[str, str]], dict[str, Any]]


def _default_transport(url: str, headers: dict[str, str]) -> dict[str, Any]:
    request = Request(url, headers=headers, method="GET")
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


class YouTubeConnector:
    """Cliente de solo lectura para el canal autorizado por OAuth."""

    def __init__(self, config: ConnectorConfig, transport: Transport | None = None):
        self.config = config
        self.transport = transport or _default_transport

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.config.access_token}",
            "Accept": "application/json",
            "User-Agent": "FV-YouTube-Connector/0.1",
        }

    def _get(self, base: str, path: str, params: dict[str, str]) -> dict[str, Any]:
        return self.transport(f"{base}/{path}?{urlencode(params)}", self._headers)

    def get_authorized_channel(self) -> dict[str, Any]:
        return self._get(
            self.config.data_api_base,
            "channels",
            {"part": "id,snippet,statistics,contentDetails", "mine": "true"},
        )

    def list_authorized_channel_videos(self, playlist_id: str, max_results: int = 25) -> dict[str, Any]:
        if not 1 <= max_results <= 50:
            raise ValueError("max_results debe estar entre 1 y 50")
        return self._get(
            self.config.data_api_base,
            "playlistItems",
            {
                "part": "id,snippet,contentDetails,status",
                "playlistId": playlist_id,
                "maxResults": str(max_results),
            },
        )

    def query_channel_analytics(
        self,
        start_date: str,
        end_date: str,
        metrics: str = "views,estimatedMinutesWatched,subscribersGained",
    ) -> dict[str, Any]:
        return self._get(
            self.config.analytics_api_base,
            "reports",
            {
                "ids": "channel==MINE",
                "startDate": start_date,
                "endDate": end_date,
                "metrics": metrics,
            },
        )
