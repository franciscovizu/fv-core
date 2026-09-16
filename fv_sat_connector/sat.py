from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SATDownloadRequest:
    rfc: str
    start_date: str
    end_date: str
    include_received: bool = True
    include_issued: bool = True
