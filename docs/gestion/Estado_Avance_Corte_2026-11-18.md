# Estado de avance para el informe — corte 18-11-2026

El tablero tiene tres sprints, no cuatro. Las tareas T01–T13 son el trabajo planificado. RF y RNF son requisitos asociados; no constituyen sprints ni tareas adicionales. Las columnas del Project representan estado (Todo, In Progress, Done), mientras que el sprint y la prioridad figuran en las tarjetas.

## Qué se completó con evidencia técnica

- T02 y T03: historias, criterios y diagramas disponibles; ya constaban como terminadas en el tablero.
- T06: el servidor demo registra vendedor, fecha/hora, productos y cantidades en SQLite local.
- T07: sobreventa, error con rollback, reintento y concurrencia se comprobaron; no se permitió stock negativo.
- T11: 12 solicitudes concurrentes respondieron con máximo 70.55 ms en la máquina local; una carrera de 13 solicitudes con stock 12 rechazó exactamente una.
- T12: los flujos de venta, inventario, historial y alerta están conectados en el prototipo local y pasaron regresión técnica.
- T13: guía breve de ejecución y uso preparada.

## Qué sigue abierto

- T01 y T05: falta catálogo real y confirmación del dueño/bodega.
- T04 y T10: falta revisión de usabilidad por un vendedor; Marcelo informó que no tiene participante disponible.
- T08: la alerta se muestra en la demo; faltan destinatario y canal externo acordados.
- T09: filtros técnicos listos, falta que el dueño confirme cuáles necesita.
- T12 y T13: falta aceptación del dueño y revisión de datos reales; por eso permanecen en progreso.
- Scrum: Marcelo indicó que no realizó eventos formales hasta ahora. No se fabricaron minutas. Adjuntar el formato de adaptación individual y registrar solo sesiones futuras reales.

## Desviación de calendario

T06 y T07 se completaron técnicamente el 18 de noviembre, después de las fechas originales asignadas a Sprint 2. T11 se midió el 18 de noviembre, dentro del Sprint 3 planificado para el 16–27 de noviembre. Explica el atraso de T06–T07; presenta Sprint 3 como corte parcial porque su cierre está previsto después de la fecha de evaluación.

## Evidencias relacionadas

- [`Evidencia_Sprints_01_02.md`](Evidencia_Sprints_01_02.md)
- [`Evidencia_Sprint3_API_12_sesiones.md`](../../evidencias/Evidencia_Sprint3_API_12_sesiones.md)
- [`T10_Protocolo_Usabilidad_Pendiente.md`](T10_Protocolo_Usabilidad_Pendiente.md)
- [`T12_Integracion_y_Aceptacion.md`](T12_Integracion_y_Aceptacion.md)
- [`T13_Guia_Breve_Demo.md`](T13_Guia_Breve_Demo.md)
