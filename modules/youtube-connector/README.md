# FV® YouTube Connector

**FV-ID:** VIZF850813D46  
**Autor humano, originador y director:** José Francisco Villaseñor Zúñiga  
**Marca raíz:** FV®  
**Aliado estratégico:** FV® & IA  
**Canal oficial previsto:** @franciscovizu

Módulo nativo de FV® Core para conectar, con autorización OAuth del titular, un canal de YouTube y consultar su identidad, videos y analítica.

## Alcance inicial

- Verificar el canal autorizado.
- Consultar título, descripción, identificador y estadísticas públicas/permitidas.
- Consultar la lista de videos del canal.
- Consultar métricas autorizadas de YouTube Analytics.
- Conservar registros técnicos sin almacenar contraseñas ni códigos.

## Seguridad

El módulo comienza en modo de solo lectura. El token OAuth se recibe por variable de entorno `FV_YOUTUBE_ACCESS_TOKEN` o por un gestor de secretos. Nunca debe subirse a GitHub.

La autorización real debe realizarla el propietario de la cuenta directamente en Google. Este repositorio no contiene un Client Secret, token de acceso ni credenciales personales.

## Estado de prueba

- Registro dentro de FV® Core: realizado.
- Pruebas unitarias sin conexión: incluidas.
- Conexión real con @franciscovizu: pendiente de autorización OAuth.
- Prueba funcional contra YouTube: no ejecutada todavía.
