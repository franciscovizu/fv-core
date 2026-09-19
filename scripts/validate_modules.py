#!/usr/bin/env python3
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FV_ID = "VIZF850813D46"
AUTHOR = "José Francisco Villaseñor Zúñiga"
required = {"fv_id","id","name","human_author","brand_root","status","structural_test","functional_test","description"}
errors = []
registry = json.loads((ROOT / "core/modules.json").read_text(encoding="utf-8"))
seen = set()
for entry in registry["modules"]:
    mid = entry["id"]
    if mid in seen:
        errors.append(f"ID duplicado: {mid}")
    seen.add(mid)
    path = ROOT / entry["path"] / "module.json"
    if not path.exists():
        errors.append(f"Falta manifiesto: {path.relative_to(ROOT)}")
        continue
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = required - data.keys()
    if missing:
        errors.append(f"{mid}: faltan {sorted(missing)}")
    if data.get("fv_id") != FV_ID:
        errors.append(f"{mid}: FV-ID inválido")
    if data.get("human_author") != AUTHOR:
        errors.append(f"{mid}: autor humano inválido")
    if data.get("brand_root") != "FV®":
        errors.append(f"{mid}: marca raíz inválida")
    if data.get("status") == "functionally_tested" and data.get("functional_test") != "passed":
        errors.append(f"{mid}: no puede declararse probado sin resultado passed")
if len(seen) != len(registry["modules"]):
    errors.append("El registro contiene IDs repetidos")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: {len(seen)} módulos FV® Core registrados y estructuralmente válidos.")
