from __future__ import annotations

from dataclasses import dataclass
import os

from .config import ConnectorConfig


@dataclass(frozen=True)
class SATCredentialsPresence:
    username: bool
    secret: bool
    certificate_path: bool
    private_key_path: bool
    private_key_secret: bool


def inspect_sat_credentials(config: ConnectorConfig) -> SATCredentialsPresence:
    return SATCredentialsPresence(
        username=bool(os.getenv(config.sat_username_env)),
        secret=bool(os.getenv(config.sat_password_env)),
        certificate_path=bool(os.getenv(config.sat_certificate_path_env)),
        private_key_path=bool(os.getenv(config.sat_private_key_path_env)),
        private_key_secret=bool(os.getenv(config.sat_private_key_password_env)),
    )
