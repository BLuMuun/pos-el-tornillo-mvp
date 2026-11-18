# T12 — Integración, regresión y aceptación

**Proyecto:** POS El Tornillo  
**Corte:** 18 de noviembre de 2026  
**Integración técnica:** realizada en el prototipo local mediante `app.html`, `server.py` y SQLite.  
**Aceptación de negocio:** pendiente; el dueño aún no ha confirmado catálogo, permisos ni canal de alertas.

## Flujos integrados

La aplicación conectada permite buscar los productos de demostración, preparar una venta con vendedor y cantidades, validar stock, persistir venta y detalle, consultar el historial, filtrar por vendedor/fecha y revisar alertas bajo el umbral configurado. El flujo registra stock, venta y alerta de forma transaccional. Los productos iniciales son ficticios.

## Regresión técnica disponible

Los resultados completos, el entorno y las limitaciones están en [`../../evidencias/Evidencia_Sprint3_API_12_sesiones.md`](../../evidencias/Evidencia_Sprint3_API_12_sesiones.md).

| Caso | Resultado observado | Evidencia |
|---|---|---|
| Venta válida y consulta posterior | Venta, vendedor, detalle, fecha/hora e inventario quedaron persistidos | Informe API, “Venta persistida” |
| Sobreventa de 13 con stock 12 | HTTP 409; stock siguió en 12 | Informe API, “Sobreventa 13/12” |
| Error antes de confirmar persistencia | Rollback; no quedó venta y stock siguió en 12 | Informe API, “Error de guardado” |
| Repetición de solicitud | Se devolvió la venta existente y se aplicó un solo descuento | Informe API, “Reintento idempotente” |
| Umbral de alerta y filtros | Stock 10 sin alerta; stock 9 con alerta; vendedor y fecha filtraron correctamente | Informe API, “Alerta y filtros” |
| 12 solicitudes concurrentes | 12 aceptadas; máximo observado 70,55 ms en la ejecución documentada | Informe API, “12 sesiones” |
| 13 solicitudes compitiendo por 12 unidades | 12 aceptadas, una rechazada y stock final 0 | Informe API, “Integridad ante concurrencia” |

La carga es una simulación de solicitudes HTTP paralelas en un equipo con datos sintéticos. No demuestra el comportamiento de una instalación en red ni reemplaza una prueba con 12 vendedores reales.

## Revisión de aceptación pendiente

- Catálogo, campos y stock inicial confirmados por dueño/bodega: **pendiente**.
- Roles y permisos acordados: **pendiente**.
- Destinatario/canal de alertas acordado y probado: **pendiente**.
- Prueba de usabilidad con vendedor: **pendiente** (ver protocolo T10).
- Revisión del dueño y aceptación del incremento: **pendiente**.
- Minuta de Review/aceptación: **no realizada al corte**.

Por lo anterior, T12 se mantiene In Progress. No utilizar esta demostración como sistema de ventas real.
