from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import uuid

from .config import CONNECTOR_VERSION
from .models import AuditRecord


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def new_operation_id(fv_id: str) -> str:
    return f"{fv_id}-{uuid.uuid4()}"


def build_audit_record(
    *,
    operation_id: str,
    origin: str,
    actor: str,
    action: str,
    related_uuid: str,
    result: str,
    document_sha256: str,
    error: str | None = None,
    connector_version: str = CONNECTOR_VERSION,
) -> AuditRecord:
    return AuditRecord(
        timestamp=utc_now(),
        operation_id=operation_id,
        origin=origin,
        actor=actor,
        action=action,
        related_uuid=related_uuid,
        result=result,
        document_sha256=document_sha256,
        connector_version=connector_version,
        error=error,
    )


def audit_record_as_dict(record: AuditRecord) -> dict[str, object]:
    return asdict(record)
