from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import tempfile

from .logs import JsonAuditLogger
from .models import FiscalEvent


class FilesystemStorage:
    def __init__(self, base_dir: str | Path, audit_logger: JsonAuditLogger | None = None) -> None:
        self.base_dir = Path(base_dir)
        self.audit_logger = audit_logger or JsonAuditLogger()

    def persist(self, event: FiscalEvent, original_document: bytes) -> Path:
        event_dir = self.base_dir / event.event_id
        lock_path = self.base_dir / f".{event.event_id}.lock"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        try:
            lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(lock_fd)
        except FileExistsError as exc:
            raise FileExistsError(f"Event directory is being persisted: {event_dir}") from exc
        staging_dir = Path(
            tempfile.mkdtemp(
                prefix=f".{event.event_id}.",
                suffix=".tmp",
                dir=self.base_dir,
            )
        )
        try:
            (staging_dir / "original").mkdir(parents=True, exist_ok=True)
            (staging_dir / "metadata").mkdir(exist_ok=True)
            (staging_dir / "normalized").mkdir(exist_ok=True)
            (staging_dir / "processing").mkdir(exist_ok=True)

            (staging_dir / "original" / "cfdi.xml").write_bytes(original_document)
            (staging_dir / "metadata" / "cfdi.json").write_text(
                json.dumps(event.metadata.as_dict(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            (staging_dir / "normalized" / "cfdi.json").write_text(
                json.dumps(event.normalized_data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            (staging_dir / "processing" / "result.json").write_text(
                json.dumps(event.processing_result, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            self.audit_logger.append(staging_dir / "audit" / "log.jsonl", event.audit_trail)
            staging_dir.rename(event_dir)
        except Exception:
            shutil.rmtree(event_dir, ignore_errors=True)
            shutil.rmtree(staging_dir, ignore_errors=True)
            raise
        finally:
            lock_path.unlink(missing_ok=True)
        return event_dir
