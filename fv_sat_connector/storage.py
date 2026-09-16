from __future__ import annotations

import json
from pathlib import Path

from .logs import JsonAuditLogger
from .models import FiscalEvent


class FilesystemStorage:
    def __init__(self, base_dir: str | Path, audit_logger: JsonAuditLogger | None = None) -> None:
        self.base_dir = Path(base_dir)
        self.audit_logger = audit_logger or JsonAuditLogger()

    def persist(self, event: FiscalEvent, original_document: bytes) -> Path:
        event_dir = self.base_dir / event.event_id
        (event_dir / "original").mkdir(parents=True, exist_ok=True)
        (event_dir / "metadata").mkdir(exist_ok=True)
        (event_dir / "normalized").mkdir(exist_ok=True)
        (event_dir / "processing").mkdir(exist_ok=True)

        (event_dir / "original" / "cfdi.xml").write_bytes(original_document)
        (event_dir / "metadata" / "cfdi.json").write_text(
            json.dumps(event.metadata.as_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        (event_dir / "normalized" / "cfdi.json").write_text(
            json.dumps(event.normalized_data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        (event_dir / "processing" / "result.json").write_text(
            json.dumps(event.processing_result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self.audit_logger.append(event_dir / "audit" / "log.jsonl", event.audit_trail)
        return event_dir
