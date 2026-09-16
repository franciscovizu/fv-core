from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from fv_sat_connector import SATConnectorService
from fv_sat_connector.validator import DuplicateCFDIError


SAMPLE_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/4"
                  xmlns:tfd="http://www.sat.gob.mx/TimbreFiscalDigital"
                  Version="4.0"
                  Fecha="2026-09-15T12:00:00"
                  TipoDeComprobante="I"
                  Moneda="MXN"
                  SubTotal="100.00"
                  Total="116.00">
  <cfdi:Emisor Rfc="AAA010101AAA" Nombre="Emisor SA de CV"/>
  <cfdi:Receptor Rfc="BBB010101BBB" Nombre="Receptor SA de CV"/>
  <cfdi:CfdiRelacionados TipoRelacion="01">
    <cfdi:CfdiRelacionado UUID="11111111-1111-1111-1111-111111111111"/>
  </cfdi:CfdiRelacionados>
  <cfdi:Impuestos TotalImpuestosTrasladados="16.00"/>
  <cfdi:Complemento>
    <tfd:TimbreFiscalDigital UUID="12345678-1234-1234-1234-1234567890AB"/>
  </cfdi:Complemento>
</cfdi:Comprobante>
"""


class SATConnectorServiceTest(unittest.TestCase):
    def test_ingest_builds_traceable_fiscal_event(self) -> None:
        service = SATConnectorService()

        event = service.ingest_cfdi(SAMPLE_XML, source="sat", actor="unit-test")

        self.assertEqual(event.fv_id, "VIZF850813D46")
        self.assertEqual(event.metadata.uuid, "12345678-1234-1234-1234-1234567890AB")
        self.assertEqual(event.normalized_data["currency"], "MXN")
        self.assertTrue(event.document_sha256)
        self.assertTrue(event.operation_id.startswith("VIZF850813D46-"))
        self.assertEqual(event.processing_result["classification"]["operation_type"], "ingreso")
        self.assertTrue(event.processing_result["immutable_source_preserved"])

    def test_persist_keeps_original_metadata_normalized_processing_and_audit_separate(self) -> None:
        service = SATConnectorService()

        with tempfile.TemporaryDirectory() as temp_dir:
            event = service.ingest_cfdi(
                SAMPLE_XML,
                source="sat",
                actor="unit-test",
                persist_to=temp_dir,
            )
            event_dir = Path(temp_dir) / event.event_id

            self.assertTrue((event_dir / "original" / "cfdi.xml").is_file())
            self.assertTrue((event_dir / "metadata" / "cfdi.json").is_file())
            self.assertTrue((event_dir / "normalized" / "cfdi.json").is_file())
            self.assertTrue((event_dir / "processing" / "result.json").is_file())
            self.assertTrue((event_dir / "audit" / "log.jsonl").is_file())

            metadata = json.loads((event_dir / "metadata" / "cfdi.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["uuid"], event.metadata.uuid)

    def test_duplicate_uuid_is_rejected(self) -> None:
        service = SATConnectorService()
        service.ingest_cfdi(SAMPLE_XML)

        with self.assertRaises(DuplicateCFDIError):
            service.ingest_cfdi(SAMPLE_XML)


if __name__ == "__main__":
    unittest.main()
