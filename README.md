# fv-core

FV® SAT Connector scaffold for the FV® Connector → FV® Core → FV® ERP chain.

## Current scope

This repository now contains a minimal, incremental Python implementation of the fiscal connector foundations requested for Mexico SAT CFDI ingestion:

- secure configuration through environment-variable names only;
- CFDI XML parsing and normalization;
- UUID-based duplicate protection;
- FV® Fiscal Event creation;
- FV-ID `VIZF850813D46` traceability and SHA-256 document hashing;
- separated persistence for original document, metadata, normalized data, processing output, and append-only audit logs;
- AI-assisted classification as advisory only;
- decoupled Odoo adapter prepared for Odoo 18 and 20 targets.

## Package layout

`fv_sat_connector/`

- `auth.py` authentication configuration inspection
- `sat.py` SAT request model
- `download.py` download payload model
- `parser.py` CFDI parsing and normalization
- `validator.py` fiscal validation and duplicate detection
- `fiscal_event.py` FV® Fiscal Event creation
- `traceability.py` FV-ID, hashes, audit helpers
- `ai_agent.py` advisory fiscal classification
- `odoo.py` Odoo mapping adapter
- `storage.py` separated filesystem persistence
- `logs.py` append-only JSONL audit writer
- `api.py` orchestration entry point

## Running tests

```bash
python3 -m unittest discover -s tests -v
```

## Security note

This scaffold never stores SAT or Odoo secrets in source code. Use environment variables or a secret manager for credentials, certificates, private keys, and tokens.
