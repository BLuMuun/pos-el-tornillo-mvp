# T01 — Registro inicial de alcance y datos por validar

**Estado:** avance de análisis; pendiente de validación con el dueño y bodega.  
**Fuente:** caso de la Evaluación 3, requisitos del proyecto y planificación del tablero.  
**Importante:** este registro no representa una reunión ni una aprobación que haya ocurrido.

## Problema abordado

El proyecto propone un punto de venta que ayude a registrar operaciones y consultar existencias, controlar el inventario al confirmar ventas y señalar productos con stock bajo. La situación descrita y los detalles reales del negocio deben confirmarse con el dueño y bodega antes de dar por validado el alcance.

## Objetivo propuesto para el MVP

Permitir buscar productos, registrar ventas con vendedor, detalle y fecha/hora, validar y actualizar el stock, consultar un historial y mostrar una alerta cuando el stock quede bajo 10 unidades.

## Alcance inicial propuesto

- Búsqueda de productos por código o nombre.
- Registro de vendedor, fecha/hora, productos y cantidades.
- Rechazo de cantidades que superen las existencias disponibles.
- Descuento de stock después de confirmar la venta.
- Alerta cuando el stock resultante sea menor que 10.
- Consulta de historial con filtros que apruebe el dueño.

El alcance anterior se deriva del caso y los RF/RNF registrados. No es una aprobación del negocio.

## Datos y decisiones pendientes

| Punto que debe confirmarse | Propuesta para conversar | Validación real |
|---|---|---|
| Catálogo inicial | Código, nombre y stock inicial; confirmar si se requieren otros campos. | Pendiente: fuente y archivo del catálogo no entregados. |
| Stock inicial | Confirmar quién lo informa y quién puede corregirlo. | Pendiente con bodega/dueño. |
| Permisos | Identificar qué personas pueden vender y quién puede modificar el catálogo o el stock. | Pendiente con dueño. |
| Umbral de alerta | La planificación usa stock menor que 10; confirmar la regla. | Pendiente con dueño. |
| Canal y destinatario | La demo muestra alertas en pantalla; falta acordar si se enviarán y a quién. | Pendiente con dueño. |
| Filtros del historial | La demo permite vendedor y fecha. | Pendiente de aprobación. |
| Inventario compartido | Confirmar cuántos vendedores consultan o actualizan stock y desde qué equipos. | Pendiente con dueño. |

## Registro de validación que debe completar Marcelo

- Fecha de conversación: pendiente.
- Participantes del negocio: pendiente.
- Acuerdos y cambios al alcance: pendiente.
- Evidencia adjunta (acta, mensaje autorizado o documento revisado): pendiente.
- Confirmación del dueño y bodega: pendiente.

## Criterio de término de T01

T01 podrá pasar a Done cuando el dueño y bodega revisen y confirmen los datos, permisos, reglas y límites, y quede una evidencia real de esa revisión. Mientras falte esa confirmación, el tablero debe conservar T01 en In Progress.
