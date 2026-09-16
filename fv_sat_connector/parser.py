from __future__ import annotations

from decimal import Decimal
from xml.etree import ElementTree

from .models import CfdiMetadata


CFDI_NS = {"cfdi": "http://www.sat.gob.mx/cfd/4", "tfd": "http://www.sat.gob.mx/TimbreFiscalDigital"}


def _decimal(value: str | None) -> Decimal:
    return Decimal(value or "0")


def parse_cfdi_xml(xml_bytes: bytes) -> tuple[CfdiMetadata, dict[str, object]]:
    root = ElementTree.fromstring(xml_bytes)
    emisor = root.find("cfdi:Emisor", CFDI_NS)
    receptor = root.find("cfdi:Receptor", CFDI_NS)
    timbre = root.find(".//tfd:TimbreFiscalDigital", CFDI_NS)
    impuestos = root.find("cfdi:Impuestos", CFDI_NS)
    relacionados = root.findall(".//cfdi:CfdiRelacionado", CFDI_NS)

    metadata = CfdiMetadata(
        uuid=(timbre.attrib.get("UUID") if timbre is not None else "") or "",
        rfc_emisor=(emisor.attrib.get("Rfc") if emisor is not None else "") or "",
        rfc_receptor=(receptor.attrib.get("Rfc") if receptor is not None else "") or "",
        fecha=root.attrib.get("Fecha", ""),
        tipo_comprobante=root.attrib.get("TipoDeComprobante", ""),
        subtotal=_decimal(root.attrib.get("SubTotal")),
        impuestos=_decimal(impuestos.attrib.get("TotalImpuestosTrasladados") if impuestos is not None else None)
        + _decimal(impuestos.attrib.get("TotalImpuestosRetenidos") if impuestos is not None else None),
        total=_decimal(root.attrib.get("Total")),
        moneda=root.attrib.get("Moneda", ""),
        related_uuids=tuple(rel.attrib.get("UUID", "") for rel in relacionados if rel.attrib.get("UUID")),
    )

    normalized = {
        "uuid": metadata.uuid,
        "issuer_rfc": metadata.rfc_emisor,
        "receiver_rfc": metadata.rfc_receptor,
        "issued_at": metadata.fecha,
        "document_type": metadata.tipo_comprobante,
        "subtotal": str(metadata.subtotal),
        "taxes": str(metadata.impuestos),
        "total": str(metadata.total),
        "currency": metadata.moneda,
        "status": metadata.estado,
        "related_uuids": list(metadata.related_uuids),
    }
    return metadata, normalized
