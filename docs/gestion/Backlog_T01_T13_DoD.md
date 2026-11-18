# Product Backlog T01–T13 y Definition of Done propuesta

**Proyecto:** Sistema POS — Ferretería El Tornillo  
**Uso:** material de apoyo para el informe de la Evaluación 3. Los criterios son propuestas comprobables; contrástalos con el tablero y con lo que efectivamente construyas. No marques una tarea como Done solo porque su criterio esté escrito.

| ID | Entregable/tarea | Definition of Done propuesta | Estado de evidencia disponible en esta carpeta |
|---|---|---|---|
| T01 | Confirmar problema, objetivos, alcance y datos iniciales | El dueño y bodega revisan y confirman alcance, fuente/campos del catálogo, stock inicial, permisos de ajuste y destinatario/canal de alerta; se registra fecha y evidencia de la validación. | **Pendiente:** no hay catálogo real ni confirmación del dueño/bodega. El documento T01 identifica lo que falta. |
| T02 | Crear historias, criterios de aceptación y priorización MoSCoW | Las historias cubren los RF/RNF, tienen criterios de aceptación verificables y prioridades revisadas; el Product Backlog refleja esas decisiones. | **Borrador disponible:** ver [`Historias_RF_RNF_Criterios.md`](../requisitos/Historias_RF_RNF_Criterios.md). Confirmar prioridades/sprints contra GitHub. |
| T03 | Modelar datos y dibujar el flujo de venta | El modelo de clases muestra atributos, métodos, asociaciones y multiplicidades; el flujo cubre éxito, falta de stock, error de guardado y alerta bajo 10; ambos quedan editables y coherentes con RF-01 a RF-05. | **Artefactos iniciales disponibles:** modelo de clases y flujo `.drawio`; el modelo sigue sujeto a T01. |
| T04 | Prototipar pantalla de venta y probar navegación | Un usuario puede navegar el prototipo desde la búsqueda hasta la confirmación/rechazo; se registran los problemas de navegación observados y sus ajustes. | **Prototipo fuente disponible:** [`app.html`](../../app.html); falta registrar una prueba de navegación con usuario. El protocolo T10 permite preparar esa sesión. |
| T05 | Cargar catálogo, buscar productos y mostrar stock | Se carga el catálogo validado por T01; una búsqueda por código/nombre muestra el producto y existencia vigente; los casos sin coincidencia se informan. | **Pendiente para catálogo real:** el prototipo contiene datos ficticios marcados como demostración. |
| T06 | Registrar venta con vendedor, detalle y fecha/hora | Una venta confirmada guarda vendedor, fecha/hora, productos y cantidades; una venta no confirmada no figura como realizada. | **Implementado y probado localmente:** el servidor demo guarda la venta en SQLite y permite consultarla. Ver informe T11. No es almacenamiento compartido del negocio. |
| T07 | Validar stock y descontarlo de forma consistente | Al confirmar se revalida el stock; se bloquea la sobreventa; venta, detalles y descuento se confirman juntos; ante error no queda venta parcial ni stock descontado; el descuento ocurre una sola vez. | **Implementado y probado en demo local:** sobreventa rechazada, rollback ante fallo, reintento idempotente y carrera de 13 solicitudes documentados en el informe T11. |
| T08 | Mostrar alerta cuando el stock sea menor que 10 | Tras una venta confirmada se genera alerta con producto, stock observado y fecha/hora cuando el resultado es menor que 10; con 10 exactas no se alerta; el canal fue confirmado en T01. | **Regla local probada:** 10 no genera alerta y 9 sí. **Pendiente:** confirmar destinatario/canal con el dueño; no se envían notificaciones externas. |
| T09 | Guardar historial de ventas y agregar filtros aprobados | El historial persistente permite consultar las ventas confirmadas y aplicar solo los filtros aprobados; ventas rechazadas/fallidas no aparecen como confirmadas. | **Implementado y probado localmente:** historial SQLite y filtros por vendedor/fecha. **Pendiente:** aprobación de filtros y almacenamiento compartido del negocio. |
| T10 | Probar usabilidad con vendedores y registrar resultados | Vendedores realizan tareas acordadas; se registran participantes, tareas, observaciones, dificultades y cambios derivados. El umbral de aprobación, si se usa, queda acordado antes de la prueba. | **Protocolo listo; prueba pendiente:** Marcelo no cuenta con un vendedor disponible. No se registran resultados ficticios. |
| T11 | Medir respuesta de venta con 12 sesiones concurrentes | Se ejecuta una prueba reproducible con 12 sesiones concurrentes; se registran entorno, tiempos y resultado frente al máximo de 3 segundos. | **Prueba técnica local completada:** 12/12 solicitudes confirmadas; máximo medido 70.55 ms. Simulación en un equipo, no representa 12 vendedores reales ni una red de producción. |
| T12 | Integrar flujos, corregir defectos y solicitar aceptación | Los flujos comprometidos están integrados; los defectos detectados quedan resueltos o documentados; se realiza regresión de los criterios acordados y se registra la aceptación o los pendientes del dueño/docente. | **Integración/regresión local completada; aceptación pendiente:** catálogo, permisos, alertas externas y revisión del dueño siguen sin validar. |
| T13 | Preparar guía breve, revisar datos y cerrar incremento | La guía describe el uso de las funciones entregadas; se revisan catálogo y datos aprobados; el incremento queda presentado con evidencia y pendientes identificados. | **Guía lista; cierre pendiente:** no hay catálogo ni datos aprobados para revisar con dueño/bodega. |

## Estado de trabajo al 18 de noviembre de 2026

| Tarea | Estado sugerido en GitHub | Motivo |
|---|---|---|
| T01 | In Progress | Falta confirmación de alcance, catálogo, stock y canal de alertas. |
| T02–T03 | Done | Historias/criterios y diagramas preparados; T02 y T03 ya estaban cerradas en el tablero. |
| T04–T05 | In Progress | Prototipo y catálogo de ejemplo listos; falta revisión con vendedor y carga real. |
| T06–T07 | Done | Flujos implementados en SQLite local y comprobaciones técnicas aprobadas. |
| T08–T10 | In Progress | Regla/alerta y protocolo disponibles; falta canal externo y sesión con vendedor. |
| T11 | Done | Prueba reproducible de 12 solicitudes completada dentro del límite local. |
| T12–T13 | In Progress | Integración y guía preparadas; falta aceptación del dueño y revisión de datos reales. |

## Antes de pasar estos estados al informe

- Verifica en GitHub los sprints, prioridades y estados actuales; esta tabla no sustituye el tablero.
- En cada sprint registra qué se comprometió, qué se completó, las fechas reales, la evidencia y las desviaciones.
- Separa “prototipo preparado” de “función probada” y de “función aceptada”.
- Si una dependencia de T01 sigue pendiente, indícalo y no completes con datos supuestos como si fueran reales.
- T06 y T07 se completaron técnicamente el 18-11, después de las fechas de Sprint 2. T11 se midió el 18-11, dentro del periodo planificado para Sprint 3. Explica la desviación de T06–T07 y el corte parcial de Sprint 3 con esas fechas.
