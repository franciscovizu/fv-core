from __future__ import annotations

from collections.abc import Iterable
import threading

from .models import CfdiMetadata


class ValidationError(ValueError):
    pass


class DuplicateCFDIError(ValidationError):
    pass


class DuplicateDetector:
    def __init__(self, existing_uuids: Iterable[str] = ()) -> None:
        self._lock = threading.Lock()
        self._seen = set(existing_uuids)
        self._reserved: set[str] = set()

    def reserve(self, uuid: str) -> None:
        with self._lock:
            if uuid in self._seen or uuid in self._reserved:
                raise DuplicateCFDIError(f"CFDI with UUID {uuid} is already registered")
            self._reserved.add(uuid)

    def commit(self, uuid: str) -> None:
        with self._lock:
            self._reserved.discard(uuid)
            self._seen.add(uuid)

    def release(self, uuid: str) -> None:
        with self._lock:
            self._reserved.discard(uuid)

    def ensure_unique(self, uuid: str) -> None:
        self.reserve(uuid)
        self.commit(uuid)


def validate_metadata(metadata: CfdiMetadata) -> None:
    if not metadata.uuid:
        raise ValidationError("CFDI UUID is required")
    if not metadata.rfc_emisor or not metadata.rfc_receptor:
        raise ValidationError("CFDI emitter and receiver RFCs are required")
    if metadata.total <= 0:
        raise ValidationError("CFDI total must be greater than zero")
