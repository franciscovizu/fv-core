from __future__ import annotations

from .models import CfdiMetadata


class FiscalAIAgent:
    def analyze(self, metadata: CfdiMetadata) -> dict[str, object]:
        operation_map = {
            "I": ("ingreso", "Ventas", "out_invoice"),
            "E": ("egreso", "Gastos", "in_refund"),
            "P": ("pago", "Conciliación", "entry"),
            "N": ("nómina", "Contabilidad", "entry"),
        }
        operation_type, suggested_module, move_type = operation_map.get(
            metadata.tipo_comprobante,
            ("por_clasificar", "Contabilidad", "entry"),
        )
        review_required = metadata.tipo_comprobante not in operation_map or metadata.impuestos < 0
        return {
            "operation_type": operation_type,
            "suggested_odoo_module": suggested_module,
            "suggested_move_type": move_type,
            "human_review_required": review_required,
            "notes": [
                "La IA solo sugiere clasificación y excepciones.",
                "El CFDI original permanece sin modificación.",
            ],
        }
