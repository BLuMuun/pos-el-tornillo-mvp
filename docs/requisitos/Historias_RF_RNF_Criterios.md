# T02 — Historias de usuario, criterios de aceptación y prioridad

**Proyecto:** Sistema POS — Ferretería El Tornillo  
**Estado:** propuesta de análisis para revisar con el dueño y bodega. No representa funciones ya implementadas ni pruebas ya ejecutadas.

## Criterio general de terminado (DoD)

Un requerimiento se considera terminado cuando:

- existe una versión implementada o un prototipo navegable que cubre el alcance acordado;
- sus criterios de aceptación se pueden comprobar y fueron revisados;
- las pruebas previstas se ejecutaron y sus resultados quedaron registrados;
- no se produce una venta con stock insuficiente ni un inventario negativo;
- se adjunta evidencia real (captura, enlace al prototipo o registro de prueba) y se actualiza el estado en GitHub;
- los datos, permisos y canales que dependen del dueño o de bodega están confirmados, o se identifican claramente como pendientes.

El DoD anterior es una propuesta para el proyecto. Los datos del catálogo, los permisos de edición y el canal de alerta siguen pendientes de validación en T01.

## Requerimientos funcionales

### RF-01 — Buscar producto y consultar stock

**Historia:** Como vendedor, quiero buscar un producto por código o nombre para conocer su stock antes de vender.

**Prioridad y sprint del tablero:** Must · Sprint 1.

**Criterios de aceptación:**

- Si existe una coincidencia por código o nombre, el sistema muestra el producto y su stock vigente.
- Si no existe coincidencia, el sistema informa que no encontró el producto.
- La consulta no modifica el stock.

**DoD específico:** se comprueba la búsqueda por código, por nombre y sin coincidencias; se conserva evidencia de esos resultados.

### RF-02 — Registrar una venta con vendedor, detalle y fecha/hora

**Historia:** Como vendedor, quiero registrar los productos y cantidades vendidos con mi identificación y la fecha/hora para dejar constancia de la operación.

**Prioridad y sprint del tablero:** Must · Sprint 2.

**Criterios de aceptación:**

- La venta guarda vendedor, fecha/hora y uno o más productos con sus cantidades.
- La venta queda confirmada solo cuando se valida y guarda correctamente.
- Una venta que no se confirma no aparece como venta completada.

**DoD específico:** se revisa el detalle guardado y se conserva una evidencia de una venta confirmada y de una operación rechazada o no confirmada.

### RF-03 — Validar stock e impedir la sobreventa

**Historia:** Como vendedor, quiero que el sistema compruebe las existencias para no vender más unidades de las disponibles.

**Prioridad y sprint del tablero:** Must · Sprint 2.

**Criterios de aceptación:**

- Al confirmar, se vuelve a comprobar el stock disponible.
- Si la cantidad solicitada supera el stock, la venta se rechaza y el inventario no cambia.
- Si el stock alcanza para todos los productos, la venta puede continuar a confirmación.

**DoD específico:** se registra evidencia de una venta válida y de otra rechazada por falta de stock; en el caso rechazado, el stock permanece igual.

### RF-04 — Descontar inventario al confirmar la venta

**Historia:** Como encargado del inventario, quiero que el stock se descuente una sola vez después de confirmar la venta para mantener las existencias actualizadas.

**Prioridad y sprint del tablero:** Must · Sprint 2.

**Criterios de aceptación:**

- Después de confirmar, cada producto reduce su stock según la cantidad vendida.
- Una venta no confirmada o fallida no descuenta stock.
- La cantidad no se descuenta más de una vez por la misma venta.

**DoD específico:** se compara el stock anterior y posterior a una venta confirmada y se registra el resultado de una operación fallida.

### RF-05 — Alertar al dueño cuando el stock sea menor que 10

**Historia:** Como dueño, quiero recibir una alerta cuando un producto quede bajo 10 unidades para revisar su reposición.

**Prioridad y sprint del tablero:** Must · Sprint 2.

**Criterios de aceptación:**

- Después de actualizar correctamente el inventario, se genera una alerta si el stock queda en 9 o menos.
- Con 10 unidades exactas no se genera la alerta.
- La alerta identifica el producto, el stock observado y la fecha/hora.
- El canal y destinatario concreto deben confirmarse con el dueño en T01.

**DoD específico:** se comprueban los casos de stock final 9 y 10; se adjunta evidencia y se deja el canal como pendiente hasta obtener confirmación.

### RF-06 — Consultar historial de ventas

**Historia:** Como dueño, quiero consultar el historial de ventas para revisar las operaciones registradas.

**Prioridad y sprint del tablero:** Should · Sprint 3.

**Criterios de aceptación:**

- El historial muestra fecha/hora, vendedor y detalle de cada venta confirmada.
- Las ventas rechazadas o fallidas no aparecen como confirmadas.
- Los filtros se limitan a los aprobados por el dueño; aún se debe confirmar cuáles serán.

**DoD específico:** se verifica el historial con ventas de prueba y se registra la lista de filtros confirmados o pendientes.

### RF-07 — Mantener el catálogo y el stock autorizado

**Historia:** Como usuario autorizado, quiero mantener los datos del catálogo y sus existencias para disponer de información correcta.

**Prioridad y sprint del tablero:** Should · Sprint 1.

**Criterios de aceptación:**

- Se pueden crear o actualizar los campos del catálogo que se hayan confirmado en T01.
- Solo los roles autorizados pueden editar esos datos.
- Se informa el resultado de la actualización.

**DoD específico:** se documentan los campos y permisos aprobados, y se prueba una actualización autorizada y una acción no autorizada. Los campos y roles aún deben confirmarse.

### RF-08 — Actualizar el stock compartido entre vendedores

**Historia:** Como vendedor, quiero consultar la misma existencia actualizada que los demás vendedores para evitar basarme en datos antiguos.

**Prioridad y sprint del tablero:** Should · Sprint 2.

**Criterios de aceptación:**

- Después de una venta confirmada, la siguiente consulta muestra el stock actualizado.
- Dos consultas de vendedores distintos muestran la misma existencia vigente.
- Una consulta o venta rechazada no modifica el stock.

**DoD específico:** se documentan las consultas de más de un vendedor o sesión y el stock observado después de una actualización.

## Requerimientos no funcionales

### RNF-01 — Usabilidad para vendedores

**Historia:** Como vendedor con poca experiencia tecnológica, quiero completar las tareas habituales con pasos claros para usar el sistema sin dificultad.

**Prioridad y sprint del tablero:** Must · Sprint 1 y Sprint 3.

**Criterios de aceptación:**

- Se prueba con vendedores y tareas acordadas, como buscar un producto y registrar una venta.
- Se anotan el resultado, las dudas y los problemas observados.
- **Umbral propuesto para validar:** al menos 80 % de las tareas de prueba se completa sin ayuda. Este porcentaje no viene definido en el caso; hay que acordarlo con el docente o dueño antes de presentarlo como criterio aprobado.

**DoD específico:** se adjunta el registro real de las pruebas y se indican los cambios hechos a partir de sus resultados.

### RNF-02 — Respuesta de venta en un máximo de 3 segundos

**Historia:** Como vendedor, quiero que la confirmación de la venta responda en un máximo de 3 segundos para continuar atendiendo.

**Prioridad y sprint del tablero:** Must · Sprint 2 y Sprint 3.

**Criterios de aceptación:**

- Se mide el tiempo entre confirmar la venta y recibir el resultado.
- Cada prueba dentro de la carga acordada debe responder en 3 segundos o menos.
- El informe indica el equipo, el entorno, la cantidad de sesiones y los resultados medidos.

**DoD específico:** se adjunta una tabla o captura con las mediciones reales; no se afirma el cumplimiento sin haberlo medido.

### RNF-03 — Integridad del inventario ante errores y concurrencia

**Historia:** Como dueño, quiero que los errores o ventas simultáneas no dejen ventas parciales ni inventario incorrecto.

**Prioridad y sprint del tablero:** Must · Sprint 2 y Sprint 3.

**Criterios de aceptación:**

- Si falla el guardado, no queda una venta parcial ni se descuenta el stock.
- El stock no queda negativo.
- Si dos ventas intentan usar las últimas unidades disponibles, el sistema vuelve a validar y no confirma cantidades que excedan el stock.

**DoD específico:** se registran pruebas de error y de concurrencia, con el stock inicial, las acciones realizadas y el resultado observado.

## Revisión antes de incluirlo en el informe

- Las prioridades y sprints anotados reflejan las etiquetas que aparecían en el tablero de GitHub; comprueba que sigan iguales.
- Las historias y criterios son una propuesta derivada del caso, no evidencia de implementación.
- No agregues resultados de pruebas hasta ejecutarlas realmente.
- Completa los datos y permisos pendientes cuando dueño o bodega los confirmen.

