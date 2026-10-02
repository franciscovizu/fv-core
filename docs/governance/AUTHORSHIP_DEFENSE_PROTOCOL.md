# FV® Core — Protocolo de defensa de autoría y procedencia

**Autor humano / originador:** José Francisco Villaseñor Zúñiga

## Objetivo

Preservar evidencia verificable de la evolución de FV® Core sin exagerar afirmaciones de prioridad o atribuir conductas a terceros sin prueba suficiente.

## Capas de evidencia

1. **Fuente original:** conversación, documento, código, imagen, audio, hoja de cálculo o diseño.
2. **Fecha verificable:** timestamp disponible en la fuente o sistema de custodia.
3. **FV-ID:** identificador de continuidad del trabajo.
4. **Hash:** SHA-256 cuando exista o pueda generarse.
5. **Commit:** incorporación al repositorio con fecha de consolidación.
6. **Referencia cruzada:** vínculo entre la fuente previa y su registro posterior en GitHub.
7. **Respaldo externo:** copia independiente cuando sea apropiado.
8. **Publicación/registro:** Devpost, GitHub, Copyright u otra fuente independiente cuando exista.

## Regla temporal

La fecha del commit de GitHub indica **cuándo se incorporó una evidencia al repositorio**, no necesariamente cuándo nació el concepto o se produjo la fuente.

Para trabajos anteriores a la creación o consolidación del repositorio debe registrarse:

- fecha original de la fuente;
- nombre exacto del archivo;
- hash disponible;
- contexto mínimo;
- fecha de incorporación a GitHub;
- relación con versiones posteriores.

## Regla de afirmaciones

Se puede afirmar:

- que una fuente existía en una fecha respaldada;
- que contiene un concepto, estructura o implementación concreta;
- que una versión posterior deriva de una anterior cuando la secuencia lo sustenta.

No se debe afirmar, sin evidencia adicional:

- que un tercero copió deliberadamente el material;
- que una coincidencia prueba plagio;
- que FV® fue “el primero del mundo” en una técnica ya conocida;
- que una empresa o persona conoció la obra antes de una fecha sin prueba verificable.

## Secuencia FV®

`Origen → estado esperado → evento → resultado → evidencia → hash → commit → historial`

Una ruptura de secuencia se registra como **anomalía a investigar**, no como atribución automática de responsable.
