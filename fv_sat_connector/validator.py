from __future__ import annotations

from collections.abc import Iterable

from .models import CfdiMetadata


class ValidationError(ValueError):
    pass


class DuplicateCFDIError(ValidationError):
    pass


class DuplicateDetector:
    def __init__(self, existing_uuids: Iterable[str] = ()) -> None:
        self._seen = set(existing_uuids)

    def ensure_unique(self, uuid: str) -> None:
        if uuid in self._seen:
            raise DuplicateCFDIError(f"CFDI with UUID {uuid} is already registered")
        self._seen.add(uuid)


def validate_metadata(metadata: CfdiMetadata) -> None:
    if not metadata.uuid:
        raise ValidationError("CFDI UUID is required")
    if not metadata.rfc_emisor or not metadata.rfc_receptor:
        raise ValidationError("CFDI emitter and receiver RFCs are required")
    if metadata.total <= 0:
        raise ValidationError("CFDI total must be greater than zero")
