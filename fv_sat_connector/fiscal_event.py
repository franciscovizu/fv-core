from __future__ import annotations

from .config import ConnectorConfig
from .models import FiscalEvent
from .traceability import build_audit_record, new_operation_id, sha256_bytes, utc_now


class FiscalEventFactory:
    def __init__(self, config: ConnectorConfig) -> None:
        self.config = config

    def create(
        self,
        *,
        source: str,
        actor: str,
        original_document: bytes,
        metadata,
        normalized_data: dict[str, object],
        processing_result: dict[str, object],
    ) -> FiscalEvent:
        operation_id = new_operation_id(self.config.fv_id)
        document_sha = sha256_bytes(original_document)
        event_id = f"fiscal-event-{metadata.uuid}-{operation_id}"
        audit = build_audit_record(
            operation_id=operation_id,
            origin=source,
            actor=actor,
            action="cfdi_ingested",
            related_uuid=metadata.uuid,
            result="success",
            document_sha256=document_sha,
            connector_version=self.config.connector_version,
        )
        return FiscalEvent(
            event_id=event_id,
            fv_id=self.config.fv_id,
            operation_id=operation_id,
            connector_version=self.config.connector_version,
            source=source,
            actor=actor,
            created_at=utc_now(),
            document_sha256=document_sha,
            metadata=metadata,
            normalized_data=normalized_data,
            processing_result=processing_result,
            audit_trail=(audit,),
        )
