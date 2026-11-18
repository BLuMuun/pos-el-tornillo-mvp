# T13 — Guía breve del prototipo POS

## Iniciar

1. Instala/usa Python 3.10 o posterior.
2. Abre PowerShell o una terminal dentro de la carpeta `POS_El_Tornillo_MVP`.
3. Ejecuta `python server.py`.
4. En el navegador abre `http://127.0.0.1:8000/`.
5. Para detener el servidor, vuelve a la terminal y usa `Ctrl+C`.

El primer inicio crea `data/pos_demo.sqlite3`. El servidor escucha solo en este computador. No cambies la dirección a `0.0.0.0` ni compartas el puerto: el prototipo no tiene inicio de sesión.

## Probar una venta

1. Busca por código (por ejemplo, `P-001`) o por nombre.
2. Indica una cantidad y presiona **Agregar**.
3. Escribe un nombre de vendedor ficticio para la prueba.
4. Presiona **Confirmar venta**. El sistema vuelve a validar el stock antes de guardar.
5. Revisa el stock actualizado, el historial y, si corresponde, la alerta.
6. En el historial puedes filtrar por vendedor o fecha.

El checkbox permite simular un error de guardado para observar que la transacción se revierte. No cuenta como venta.

## Restablecer

**Restablecer datos demo** elimina las ventas y alertas de demostración y repone el stock inicial ficticio. Úsalo antes de repetir una prueba; la acción no tiene confirmación.

## Datos y límites

Los tres productos y sus existencias son ficticios. No agregues clientes ni información real. El servidor no tiene usuarios, permisos, precios, cálculo de total, respaldo ni notificación externa. La base SQLite es local a un solo equipo. El canal de alerta y el catálogo real deben confirmarse antes de cualquier uso operacional.

Para revisar resultados reproducibles de API y concurrencia, consulta `../../evidencias/Evidencia_Sprint3_API_12_sesiones.md`. Esos datos son sintéticos y la prueba no equivale a aceptación del dueño ni a prueba de usabilidad con vendedores.
