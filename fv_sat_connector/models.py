from __future__ import annotations

from dataclasses import asdict, dataclass, field
from decimal import Decimal


@dataclass(frozen=True)
class CfdiMetadata:
    uuid: str
    rfc_emisor: str
    rfc_receptor: str
    fecha: str
    tipo_comprobante: str
    subtotal: Decimal
    impuestos: Decimal
    total: Decimal
    moneda: str
    estado: str = "vigente"
    related_uuids: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, object]:
        data = asdict(self)
        for key in ("subtotal", "impuestos", "total"):
            data[key] = str(data[key])
        return data


@dataclass(frozen=True)
class AuditRecord:
    timestamp: str
    operation_id: str
    origin: str
    actor: str
    action: str
    related_uuid: str
    result: str
    document_sha256: str
    connector_version: str
    error: str | None = None


@dataclass(frozen=True)
class FiscalEvent:
    event_id: str
    fv_id: str
    operation_id: str
    connector_version: str
    source: str
    actor: str
    created_at: str
    document_sha256: str
    metadata: CfdiMetadata
    normalized_data: dict[str, object]
    processing_result: dict[str, object]
    audit_trail: tuple[AuditRecord, ...] = field(default_factory=tuple)
