# Avance y evidencia — Sprint 1 y Sprint 2

**Fecha de revisión:** 18 de noviembre de 2026.  
**Proyecto de seguimiento:** [POS El Tornillo — MVP](https://github.com/users/BLuMuun/projects/1/views/1).  
**Repositorio del prototipo:** [BLuMuun/pos-el-tornillo-mvp](https://github.com/BLuMuun/pos-el-tornillo-mvp).

Este registro separa el trabajo observable del prototipo de las validaciones que requieren información o participantes externos. Las capturas numeradas están en [`evidencias/`](../../evidencias/README_Evidencias_Eval3.md). El catálogo usado es ficticio. No se simula aprobación de dueño, bodega o vendedores.

## Sprint 1 — 19 al 30 de octubre

### T01 — Confirmar problema, objetivos, alcance y datos iniciales

- **Issue:** [T01 #12](https://github.com/BLuMuun/clase1/issues/12).
- **Avance:** se preparó el registro de alcance, datos y preguntas por validar en [`T01_Registro_Alcance_Por_Validar.md`](T01_Registro_Alcance_Por_Validar.md).
- **Pendiente:** catálogo real, fuente del stock, permisos, canal/destinatario de alerta y confirmación de dueño/bodega. No hubo conversación registrada.
- **Estado que corresponde:** In Progress.

### T02 — Historias, criterios de aceptación y MoSCoW

- **Issue:** [T02 #13](https://github.com/BLuMuun/clase1/issues/13).
- **Evidencia:** [`Historias_RF_RNF_Criterios.md`](../requisitos/Historias_RF_RNF_Criterios.md) contiene historias y criterios propuestos.
- **Estado del tablero:** Done, ya estaba cerrado antes de esta revisión.
- **Pendiente de negocio:** las prioridades/filtros deben revisarse si el dueño cambia el alcance.

### T03 — Modelo de datos y flujo de venta

- **Issue:** [T03 #19](https://github.com/BLuMuun/clase1/issues/19).
- **Evidencia:** [`Modelo_Datos_MVP.drawio`](../diagramas/Modelo_Datos_MVP.drawio), [`Flujo_Venta_Control_Stock.drawio`](../diagramas/Flujo_Venta_Control_Stock.drawio), [`Casos_Uso_POS_El_Tornillo.drawio`](../diagramas/Casos_Uso_POS_El_Tornillo.drawio) y [`Secuencia_Venta_Alerta.drawio`](../diagramas/Secuencia_Venta_Alerta.drawio). Los cuatro archivos se analizaron como XML válido.
- **Estado que corresponde:** Done para los artefactos de modelado preparados. Campos de negocio aún pueden cambiar tras validar T01.

### T04 — Prototipo de venta y navegación

- **Issue:** [T04 #14](https://github.com/BLuMuun/clase1/issues/14).
- **Evidencia:** [`index.html`](../../index.html) permite recorrer búsqueda, detalle, confirmación, rechazo, historial y alertas; capturas 01–09.
- **Pendiente:** la revisión de navegación y usabilidad con vendedores que exige la tarea no se ha hecho. Las interacciones automatizadas del navegador no se presentan como participantes humanos.
- **Estado que corresponde:** In Progress.

### T05 — Catálogo, búsqueda y stock

- **Issue:** [T05 #20](https://github.com/BLuMuun/clase1/issues/20).
- **Evidencia:** el catálogo demo permite búsqueda por código/nombre y presenta stock; captura 01. La búsqueda sin coincidencias se comprobó y mostró un mensaje claro; captura 12.
- **Pendiente:** reemplazar los tres productos demo por el catálogo real y validar existencias con bodega; ver T01.
- **Estado que corresponde:** In Progress.

## Sprint 2 — 2 al 13 de noviembre

### T06 — Registrar venta con vendedor, detalle y fecha/hora

- **Issue:** [T06 #15](https://github.com/BLuMuun/clase1/issues/15).
- **Evidencia:** una venta de demostración quedó con vendedor, fecha/hora, producto y cantidad; se consultó en el historial y persistió tras recargar; capturas 04 y 06.
- **Ampliación técnica posterior:** el 18-11 se integró una demo local con SQLite. La venta, líneas y vendedor ahora persisten en la base demo y se pueden consultar por API; ver `../../evidencias/Evidencia_Sprint3_API_12_sesiones.md`.
- **Límite:** SQLite está en un solo equipo, usa datos ficticios y no equivale a persistencia compartida del negocio.
- **Estado que corresponde:** Done para el flujo técnico demostrado; la implantación del negocio sigue pendiente.

### T07 — Validar stock, descontarlo una vez y manejar fallos

- **Issue:** [T07 #21](https://github.com/BLuMuun/clase1/issues/21).
- **Evidencia:** cantidad sobre stock rechazada sin descuento (02); error simulado sin venta ni descuento (03); venta confirmada reduce stock (04); reconfirmar con el detalle vacío no agrega otra venta (14).
- **Ampliación técnica posterior:** el 18-11 la venta y el descuento se integraron en una transacción SQLite; una solicitud repetida no duplica el descuento, una falla simulada revierte todo y una carrera de 13 solicitudes con stock 12 dejó 12 ventas y una rechazada. Ver `../../evidencias/Evidencia_Sprint3_API_12_sesiones.md`.
- **Límite:** comprobación local sintética; no es despliegue compartido ni aceptación operacional.
- **Estado que corresponde:** Done para la regla técnica demostrada.

### T08 — Alerta con stock menor que 10

- **Issue:** [T08 #16](https://github.com/BLuMuun/clase1/issues/16).
- **Evidencia:** stock final 10 sin alerta (07); stock final 9 genera alerta con producto y cantidad (08); los datos de demo permanecen tras recargar (09).
- **Pendiente:** confirmar destinatario y canal con dueño; la demo no envía notificaciones fuera de la página.
- **Estado que corresponde:** In Progress.

### T09 — Historial y filtros

- **Issue:** [T09 #22](https://github.com/BLuMuun/clase1/issues/22).
- **Evidencia:** la venta aparece en historial, el filtro de vendedor devuelve la coincidencia (05) y el filtro de fecha distingue el día de venta de otro día (13).
- **Pendiente:** confirmar con el dueño qué filtros debe tener el incremento y adoptar almacenamiento compartido.
- **Estado que corresponde:** In Progress.

## Estados que se deben reflejar en GitHub

- T01: In Progress.
- T02: Done.
- T03: Done.
- T04–T05: In Progress.
- T06–T07: Done por la ampliación técnica del 18-11; mantener en el informe la desviación frente a las fechas de Sprint 2.
- T08–T10: In Progress.
- T11: Done por la prueba local del 18-11; reportar el alcance y las limitaciones.
- T12–T13: In Progress mientras falte aceptación y revisión del dueño.

No se deben mover T01, T04, T05 ni T09 a Done mientras sus validaciones externas sigan pendientes. T06–T08 son demostraciones locales y conservan limitaciones frente a una implementación compartida.

## Hechos para el informe

- El registro que se puede afirmar es el de las comprobaciones locales descritas en estas evidencias; no hubo sesión con dueño, bodega o vendedores.
- Sprint 1 y Sprint 2 tienen fechas ya vencidas. T06 y T07 se completaron técnicamente el 18-11, después del cierre de Sprint 2; informa esa desviación con claridad. En Sprint 1 y otras tareas quedan criterios externos pendientes.
- Se ejecutó una prueba sintética local de 12 solicitudes con máximo 70.55 ms el 18-11, fecha incluida en Sprint 3 (16–27 nov.); más una carrera de 13 solicitudes sobre stock 12. Esto verifica el prototipo local; no certifica la infraestructura real.
