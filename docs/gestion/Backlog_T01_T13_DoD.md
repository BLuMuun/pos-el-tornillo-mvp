# Product Backlog T01–T13 y Definition of Done propuesta

**Proyecto:** Sistema POS — Ferretería El Tornillo  
**Uso:** material de apoyo para el informe de la Evaluación 3. Los criterios son propuestas comprobables; contrástalos con el tablero y con lo que efectivamente construyas. No marques una tarea como Done solo porque su criterio esté escrito.

| ID | Entregable/tarea | Definition of Done propuesta | Estado de evidencia disponible en esta carpeta |
|---|---|---|---|
| T01 | Confirmar problema, objetivos, alcance y datos iniciales | El dueño y bodega revisan y confirman alcance, fuente/campos del catálogo, stock inicial, permisos de ajuste y destinatario/canal de alerta; se registra fecha y evidencia de la validación. | **Pendiente:** no hay catálogo real ni confirmación del dueño/bodega. El documento T01 identifica lo que falta. |
| T02 | Crear historias, criterios de aceptación y priorización MoSCoW | Las historias cubren los RF/RNF, tienen criterios de aceptación verificables y prioridades revisadas; el Product Backlog refleja esas decisiones. | **Borrador disponible:** ver `T02_Historias_y_criterios_MoSCoW.md`. Confirmar prioridades/sprints contra GitHub. |
| T03 | Modelar datos y dibujar el flujo de venta | El modelo de clases muestra atributos, métodos, asociaciones y multiplicidades; el flujo cubre éxito, falta de stock, error de guardado y alerta bajo 10; ambos quedan editables y coherentes con RF-01 a RF-05. | **Artefactos iniciales disponibles:** modelo de clases y flujo `.drawio`; el modelo sigue sujeto a T01. |
| T04 | Prototipar pantalla de venta y probar navegación | Un usuario puede navegar el prototipo desde la búsqueda hasta la confirmación/rechazo; se registran los problemas de navegación observados y sus ajustes. | **Prototipo fuente disponible:** `prototipo_pos_mvp.html`; falta abrirlo y registrar pruebas de navegación con usuario(s). |
| T05 | Cargar catálogo, buscar productos y mostrar stock | Se carga el catálogo validado por T01; una búsqueda por código/nombre muestra el producto y existencia vigente; los casos sin coincidencia se informan. | **Pendiente para catálogo real:** el prototipo contiene datos ficticios marcados como demostración. |
| T06 | Registrar venta con vendedor, detalle y fecha/hora | Una venta confirmada guarda vendedor, fecha/hora, productos y cantidades; una venta no confirmada no figura como realizada. | **Prototipo local parcial:** guarda vendedor, fecha/hora y detalle en el almacenamiento del navegador; no hay servidor ni base de datos compartida, y falta registrar pruebas. |
| T07 | Validar stock y descontarlo de forma consistente | Al confirmar se revalida el stock; se bloquea la sobreventa; venta, detalles y descuento se confirman juntos; ante error no queda venta parcial ni stock descontado; el descuento ocurre una sola vez. | **Lógica demostrativa en el prototipo:** incluye validación y simulación de error en el navegador; falta ejecutar/documentar pruebas de servidor e integridad concurrente. |
| T08 | Mostrar alerta cuando el stock sea menor que 10 | Tras una venta confirmada se genera alerta con producto, stock observado y fecha/hora cuando el resultado es menor que 10; con 10 exactas no se alerta; el canal fue confirmado en T01. | **Demostración local preparada:** umbral menor que 10; destinatario/canal pendiente y falta prueba documentada. |
| T09 | Guardar historial de ventas y agregar filtros aprobados | El historial persistente permite consultar las ventas confirmadas y aplicar solo los filtros aprobados; ventas rechazadas/fallidas no aparecen como confirmadas. | **Prototipo local parcial:** guarda historial en el navegador y permite filtrar por vendedor/fecha; los filtros y la persistencia real deben acordarse con el dueño y validarse en un backend. |
| T10 | Probar usabilidad con vendedores y registrar resultados | Vendedores realizan tareas acordadas; se registran participantes, tareas, observaciones, dificultades y cambios derivados. El umbral de aprobación, si se usa, queda acordado antes de la prueba. | **Pendiente:** no se han hecho pruebas con vendedores ni se deben inventar resultados. |
| T11 | Medir respuesta de venta con 12 sesiones concurrentes | Se ejecuta una prueba reproducible con 12 sesiones concurrentes; se registran entorno, tiempos y resultado frente al máximo de 3 segundos. | **Pendiente:** el prototipo local no demuestra concurrencia de 12 sesiones ni medición de respuesta. |
| T12 | Integrar flujos, corregir defectos y solicitar aceptación | Los flujos comprometidos están integrados; los defectos detectados quedan resueltos o documentados; se realiza regresión de los criterios acordados y se registra la aceptación o los pendientes del dueño/docente. | **Pendiente:** no hay integración de software ni aceptación externa registrada. |
| T13 | Preparar guía breve, revisar datos y cerrar incremento | La guía describe el uso de las funciones entregadas; se revisan catálogo y datos aprobados; el incremento queda presentado con evidencia y pendientes identificados. | **Pendiente:** no hay guía de usuario ni cierre del incremento. |

## Antes de pasar estos estados al informe

- Verifica en GitHub los sprints, prioridades y estados actuales; esta tabla no sustituye el tablero.
- En cada sprint registra qué se comprometió, qué se completó, las fechas reales, la evidencia y las desviaciones.
- Separa “prototipo preparado” de “función probada” y de “función aceptada”.
- Si una dependencia de T01 sigue pendiente, indícalo y no completes con datos supuestos como si fueran reales.

