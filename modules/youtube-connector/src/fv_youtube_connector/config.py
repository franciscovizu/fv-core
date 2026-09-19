from dataclasses import dataclass
import os


@dataclass(frozen=True)
class ConnectorConfig:
    access_token: str
    data_api_base: str = "https://www.googleapis.com/youtube/v3"
    analytics_api_base: str = "https://youtubeanalytics.googleapis.com/v2"

    @classmethod
    def from_environment(cls) -> "ConnectorConfig":
        token = os.getenv("FV_YOUTUBE_ACCESS_TOKEN", "").strip()
        if not token:
            raise RuntimeError(
                "Falta FV_YOUTUBE_ACCESS_TOKEN. Autoriza Google OAuth y guarda el token como secreto."
            )
        return cls(access_token=token)
