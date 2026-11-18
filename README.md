# POS El Tornillo — prototipo MVP

Prototipo académico de un punto de venta para la ferretería El Tornillo. Permite recorrer el flujo de búsqueda, armado de una venta, validación de existencias, confirmación y generación de alertas de stock bajo.

## Ejecutar el prototipo integrado

Requiere Python 3.10 o posterior; no instala paquetes externos.

1. Abre una terminal en la carpeta del proyecto.
2. Ejecuta `python server.py`.
3. Abre `http://127.0.0.1:8000/` en el navegador.

El prototipo integrado usa una base SQLite local en `data/pos_demo.sqlite3`. Para detenerlo, vuelve a la terminal y presiona `Ctrl+C`. El servidor escucha únicamente en este equipo.

`index.html` conserva la versión anterior de interfaz con almacenamiento del navegador. La versión conectada a SQLite es `app.html`, que se entrega desde la ruta raíz del servidor.

## Repetir la comprobación técnica

Con Python 3.10 o posterior, ejecuta `python scripts/validate_api.py`. La prueba inicia un servidor temporal con una base SQLite aislada, revisa ventas, alertas, filtros, concurrencia y rollback; luego escribe los resultados en `evidencias/Evidencia_Sprint3_API_12_sesiones.md`. No altera la base de demostración del proyecto.

## Funciones que se pueden recorrer

- Buscar productos de demostración por nombre o código.
- Agregar cantidades al detalle de venta y validar que exista stock suficiente.
- Registrar el nombre del vendedor y confirmar la venta.
- Simular un error de guardado para observar el rechazo de la operación.
- Descontar las cantidades de la demostración y generar una alerta si el stock queda bajo 10 unidades. Con 10 exactas no se genera alerta.
- Consultar el historial local y filtrarlo por vendedor o fecha.
- Guardar ventas, historial, stock y alertas en SQLite local; el botón de reinicio restaura los productos ficticios y elimina las ventas de demostración.
- Mantener la venta, las líneas y el descuento dentro de una transacción; rechazar sobreventa y no duplicar el descuento cuando se repite la misma solicitud.

## Datos de demostración

El catálogo y las existencias iniciales son ficticios. No representan datos confirmados por el dueño o bodega. No ingresar datos reales de clientes ni información personal en esta demo.

## Alcance y límites

Esta es una demostración académica ejecutada en un solo equipo. SQLite permite observar persistencia y concurrencia local, pero no es una base compartida entre puestos de venta.

No incluye inicio de sesión, permisos por rol, precios ni cálculo de total, envío real de alertas, despliegue ni conexión compartida para vendedores. El canal de alerta, los campos del catálogo, las existencias iniciales y los permisos siguen pendientes de confirmación con el dueño y bodega. La prueba de 12 solicitudes concurrentes es una medición local sintética; no caracteriza la infraestructura del negocio.

## Documentos del proyecto

- `docs/requisitos/Historias_RF_RNF_Criterios.md`: historias y criterios de aceptación propuestos para los RF y RNF.
- `docs/gestion/Backlog_T01_T13_DoD.md`: tareas T01–T13, DoD propuesto y estado de la evidencia disponible.
- `docs/gestion/T01_Registro_Alcance_Por_Validar.md`: datos y acuerdos que faltan validar con dueño y bodega.
- `docs/gestion/Evidencia_Sprints_01_02.md`: avance, evidencia y pendientes de T01–T09.
- `docs/gestion/T10_Protocolo_Usabilidad_Pendiente.md`: protocolo preparado; falta un vendedor voluntario para ejecutarlo.
- `docs/gestion/T12_Integracion_y_Aceptacion.md`: regresión técnica ejecutada y aceptación de negocio pendiente.
- `docs/gestion/T13_Guia_Breve_Demo.md`: guía de ejecución y uso del prototipo local.
- `docs/gestion/Eventos_Scrum_Adaptacion_Individual_Eval3.md`: adaptación individual, calendario y formatos; no contiene minutas inventadas.
- `evidencias/Evidencia_Sprint3_API_12_sesiones.md`: resultados reproducibles de solicitudes API concurrentes y controles de stock.
- `docs/diagramas/`: diagramas editables de casos de uso, modelo de datos, flujo de venta y secuencia de venta/alerta.
- `evidencias/`: índice y capturas de comprobaciones del prototipo local.

El seguimiento ágil se mantiene en el [GitHub Project POS El Tornillo — MVP](https://github.com/users/BLuMuun/projects/1/views/1). Los Issues T01–T13 y los requisitos RF/RNF permanecen en el repositorio de clase y se muestran en ese tablero.

## Pendientes antes de considerar el MVP validado

1. Confirmar con el dueño y bodega el catálogo, campos, stock inicial, permisos y canal/destinatario de alertas.
2. Definir infraestructura compartida, usuarios, permisos, respaldos y canal de alerta antes de cualquier uso operacional.
3. Ejecutar la prueba de usabilidad cuando haya un vendedor disponible; el protocolo está listo, pero sus resultados siguen pendientes.
4. Solicitar al dueño revisión de flujos, catálogo, canal de alertas y aceptación. Registrar solo los eventos Scrum que se realicen realmente.
5. Mantener en GitHub como In Progress las tareas cuya validación externa todavía falte.

La evidencia de pruebas locales y simuladas está en `evidencias/`. No representa validación de usuarios ni aceptación del negocio.
