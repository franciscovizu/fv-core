from __future__ import annotations

from .models import CfdiMetadata


class OdooAdapter:
    def __init__(self, target_version: str = "18") -> None:
        if target_version not in {"18", "20"}:
            raise ValueError("Only Odoo 18 and 20 targets are supported")
        self.target_version = target_version

    def prepare_document(
        self,
        metadata: CfdiMetadata,
        normalized_data: dict[str, object],
        classification: dict[str, object],
    ) -> dict[str, object]:
        return {
            "target_version": self.target_version,
            "external_uuid": metadata.uuid,
            "partner_vat": metadata.rfc_emisor,
            "company_vat": metadata.rfc_receptor,
            "move_type": classification["suggested_move_type"],
            "currency": normalized_data["currency"],
            "invoice_date": normalized_data["issued_at"],
            "amount_total": normalized_data["total"],
            "module_hint": classification["suggested_odoo_module"],
        }
