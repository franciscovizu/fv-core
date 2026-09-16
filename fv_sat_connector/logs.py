from __future__ import annotations

import json
from pathlib import Path

from .models import AuditRecord
from .traceability import audit_record_as_dict


class JsonAuditLogger:
    def append(self, destination: Path, records: tuple[AuditRecord, ...]) -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("a", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(audit_record_as_dict(record), ensure_ascii=False) + "\n")
