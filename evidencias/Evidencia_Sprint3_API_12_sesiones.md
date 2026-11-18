# T11 — Evidencia de API y carga local de 12 sesiones

**Fecha de ejecución:** 2026-11-18  
**Entorno:** Windows 10 · Python 3.13.17 · SQLite 3.50.4 · localhost  
**Datos:** catálogo ficticio; base SQLite temporal, aislada de la demo del usuario.  
**Alcance:** solicitudes HTTP paralelas al servidor local; no son 12 vendedores reales ni una prueba sobre red/internet.

## Resultados

- **Sobreventa 13/12:** PASS — HTTP 409; stock permanece en 12.
- **Error de guardado:** PASS — rollback; stock 12 y ninguna venta persistida.
- **Venta persistida:** PASS — vendedor, fecha/hora, detalle; stock de 12 a 10.
- **Reintento idempotente:** PASS — la repetición devolvió la venta existente; un solo descuento.
- **Alerta y filtros:** PASS — 10 sin alerta; 9 con alerta; filtros vendedor/fecha comprobados.
- **RNF-02 / 12 sesiones:** PASS — 12/12 confirmadas; máximo 70.55 ms; stock de 12 a 0.
- **Integridad ante concurrencia:** PASS — 12 ventas aceptadas de 13; una rechazada; stock final 0.

## Mediciones de las 12 sesiones

- Confirmaciones: 12/12.
- Tiempo mínimo: 10.85 ms.
- Tiempo promedio: 35.04 ms.
- Percentil 95: 70.55 ms.
- Tiempo máximo: 70.55 ms.
- Requisito técnico observado: máximo ≤ 3000 ms en esta ejecución local.

## Límites

La medición corresponde a un único equipo y base local con datos sintéticos. No caracteriza el servidor del negocio ni garantiza rendimiento en producción. La concurrencia se simuló con clientes HTTP de prueba. Se necesita repetir con el entorno acordado si el docente exige otra carga o plataforma.

La aplicación no incorpora autenticación/roles, canal de alerta externo, copias de seguridad ni datos reales. La prueba técnica no reemplaza la prueba de usabilidad con vendedores (T10) ni la aceptación del dueño (T12).
