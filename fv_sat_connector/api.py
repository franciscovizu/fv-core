from __future__ import annotations

from pathlib import Path

from .ai_agent import FiscalAIAgent
from .config import ConnectorConfig
from .fiscal_event import FiscalEventFactory
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

    def ingest_cfdi(
        self,
        xml_bytes: bytes,
        *,
        source: str = "sat",
        actor: str = "connector",
        persist_to: str | Path | None = None,
    ):
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
            if persist_to is not None:
                storage = self.storage or FilesystemStorage(persist_to)
                storage.persist(event, xml_bytes)
            self.duplicate_detector.commit(metadata.uuid)
            return event
        except Exception:
            self.duplicate_detector.release(metadata.uuid)
            raise
