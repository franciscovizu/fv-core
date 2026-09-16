from __future__ import annotations

from dataclasses import dataclass
import os


DEFAULT_FV_ID = "VIZF850813D46"
CONNECTOR_VERSION = "0.1.0"


@dataclass(frozen=True)
class ConnectorConfig:
    fv_id: str = DEFAULT_FV_ID
    sat_username_env: str = "SAT_USERNAME"
    sat_password_env: str = "SAT_PASSWORD"
    sat_certificate_path_env: str = "SAT_CERTIFICATE_PATH"
    sat_private_key_path_env: str = "SAT_PRIVATE_KEY_PATH"
    sat_private_key_password_env: str = "SAT_PRIVATE_KEY_PASSWORD"
    odoo_url_env: str = "ODOO_URL"
    odoo_database_env: str = "ODOO_DATABASE"
    odoo_username_env: str = "ODOO_USERNAME"
    odoo_password_env: str = "ODOO_PASSWORD"
    connector_version: str = CONNECTOR_VERSION

    @classmethod
    def from_env(cls) -> "ConnectorConfig":
        return cls(fv_id=os.getenv("FV_CONNECTOR_FV_ID", DEFAULT_FV_ID))
