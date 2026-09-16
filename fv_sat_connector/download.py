from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DownloadedCFDI:
    xml_bytes: bytes
    source: str = "sat"
