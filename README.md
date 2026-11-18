# POS El Tornillo — prototipo MVP

Prototipo académico de un punto de venta para la ferretería El Tornillo. Permite recorrer el flujo de búsqueda, armado de una venta, validación de existencias, confirmación y generación de alertas de stock bajo.

## Ejecutar

Abre `index.html` en un navegador actualizado. No requiere instalar dependencias ni iniciar un servidor.

## Funciones que se pueden recorrer

- Buscar productos de demostración por nombre o código.
- Agregar cantidades al detalle de venta y validar que exista stock suficiente.
- Registrar el nombre del vendedor y confirmar la venta.
- Simular un error de guardado para observar el rechazo de la operación.
- Descontar las cantidades de la demostración y generar una alerta si el stock queda bajo 10 unidades. Con 10 exactas no se genera alerta.
- Consultar el historial local y filtrarlo por vendedor o fecha.
- Mantener los datos en el almacenamiento local del navegador cuando está disponible; el botón de reinicio recupera el catálogo de demostración.

## Datos de demostración

El catálogo y las existencias iniciales son ficticios. No representan datos confirmados por el dueño o bodega. No ingresar datos reales de clientes ni información personal en esta demo.

## Alcance y límites

Esta versión es un prototipo de interfaz ejecutado en un solo navegador. `localStorage` no es una base de datos del negocio: los cambios no se comparten entre navegadores o vendedores y pueden borrarse desde el navegador. El guardado y el error mostrado son simulaciones locales.

No incluye servidor, base de datos, inicio de sesión, permisos por rol, precios ni cálculo de total, envío real de alertas, sincronización entre vendedores ni control de ventas concurrentes. El canal de alerta, los campos del catálogo, las existencias iniciales y los permisos siguen pendientes de confirmación con el dueño y bodega. El prototipo no demuestra el requisito de 12 sesiones concurrentes ni un tiempo de respuesta medido.

## Documentos del proyecto

- `docs/requisitos/Historias_RF_RNF_Criterios.md`: historias y criterios de aceptación propuestos para los RF y RNF.
- `docs/gestion/Backlog_T01_T13_DoD.md`: tareas T01–T13, DoD propuesto y estado de la evidencia disponible.
- `docs/diagramas/`: diagramas editables de casos de uso, modelo de datos, flujo de venta y secuencia de venta/alerta.

El seguimiento ágil se mantiene en el [GitHub Project POS El Tornillo — MVP](https://github.com/users/BLuMuun/projects/1/views/1). Este repositorio local no mueve ni cambia los Issues existentes; al publicar el código habrá que vincular el repositorio al proyecto y decidir si se conservan esos Issues donde están.

## Pendientes antes de considerar el MVP validado

1. Confirmar con el dueño y bodega el catálogo, campos, stock inicial, permisos y canal/destinatario de alertas.
2. Definir una base de datos y un servidor para compartir el inventario entre vendedores y manejar confirmaciones de forma segura.
3. Ejecutar y registrar las pruebas acordadas, incluidas usabilidad, error al guardar, umbral de alerta, integridad y carga de 12 sesiones.
4. Actualizar el estado de las tareas en GitHub solo cuando exista evidencia real de su cumplimiento.

No se incluyen resultados de pruebas; deben registrarse después de ejecutar cada escenario.

