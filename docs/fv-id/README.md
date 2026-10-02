# FV-ID — Registro continuo de FV® Core

Este directorio conserva la línea temporal de FV-ID, respaldos y huellas de trabajo de FV® Core.

**Autor principal:** José Francisco Villaseñor Zúñiga  
**Marca raíz:** FV®  
**Colaboración tecnológica:** FV® & IA

## Estructura

- `INDEX.md`: índice cronológico maestro.
- `daily/`: constancias diarias reconstruidas o verificadas.
- `manifests/`: manifiestos e inventarios de hashes cuando se incorporen.
- `references/`: referencias a evidencia privada que no debe publicarse.

## Regla

Los registros son **append-only**. Una corrección nunca elimina la entrada previa: crea una nueva versión o una nota de corrección vinculada.

Los originales sensibles pueden permanecer fuera de GitHub; su existencia se representa mediante hash, fecha, nombre lógico y referencia de custodia.
