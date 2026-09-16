from __future__ import annotations

from pathlib import Path

from .ai_agent import FiscalAIAgent
from .config import ConnectorConfig
from .fiscal_event import FiscalEventFactory
from .models import FiscalEvent
from .odoo import OdooAdapter
from .parser import parse_cfdi_xml
from .storage import FilesystemStorage
from .validator import DuplicateDetector, validate_metadata


class SATConnectorService:
    def __init__(
        self,
        *,
        config: ConnectorConfig | None = None,
        duplicate_detector: DuplicateDetector | None = None,
        ai_agent: FiscalAIAgent | None = None,
        odoo_adapter: OdooAdapter | None = None,
        storage: FilesystemStorage | None = None,
    ) -> None:
        self.config = config or ConnectorConfig.from_env()
        self.duplicate_detector = duplicate_detector or DuplicateDetector()
        self.ai_agent = ai_agent or FiscalAIAgent()
        self.odoo_adapter = odoo_adapter or OdooAdapter("18")
        self.storage = storage
        self.factory = FiscalEventFactory(self.config)

    def _resolve_storage(self, persist_to: str | Path | None) -> FilesystemStorage | None:
        if persist_to is not None:
            return FilesystemStorage(persist_to)
        return self.storage

    def ingest_cfdi(
        self,
        xml_bytes: bytes,
        *,
        source: str = "sat",
        actor: str = "connector",
        persist_to: str | Path | None = None,
    ) -> FiscalEvent:
        """Parse, validate, classify, and optionally persist a CFDI as an FV Fiscal Event.

        Returns the created FiscalEvent. Duplicate UUID protection is reserved before processing,
        committed only after a successful ingest, and rolled back automatically if processing or
        persistence fails. When ``persist_to`` is provided, that destination is used for separated
        filesystem persistence; otherwise, an injected storage backend is used when available.
        """
        metadata, normalized_data = parse_cfdi_xml(xml_bytes)
        validate_metadata(metadata)
        self.duplicate_detector.reserve(metadata.uuid)
        try:
            classification = self.ai_agent.analyze(metadata)
            odoo_payload = self.odoo_adapter.prepare_document(metadata, normalized_data, classification)
            event = self.factory.create(
                source=source,
                actor=actor,
                original_document=xml_bytes,
                metadata=metadata,
                normalized_data=normalized_data,
                processing_result={
                    "classification": classification,
                    "odoo_payload": odoo_payload,
                    "immutable_source_preserved": True,
                },
            )
            storage = self._resolve_storage(persist_to)
            if storage is not None:
                storage.persist(event, xml_bytes)
            self.duplicate_detector.commit(metadata.uuid)
            return event
        except Exception:
            self.duplicate_detector.release(metadata.uuid)
            raise
