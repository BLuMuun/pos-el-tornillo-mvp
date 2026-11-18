"""Comprobación funcional y simulación local de 12 sesiones concurrentes.

Ejecutar con: python scripts/validate_api.py
Usa una base temporal y no modifica la base demo del usuario.
"""

from __future__ import annotations

import json
import math
import os
import platform
import socket
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = PROJECT_ROOT / "evidencias" / "Evidencia_Sprint3_API_12_sesiones.md"


def find_free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def request_json(base_url: str, path: str, method: str = "GET", payload: dict | None = None) -> tuple[int, dict, float]:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(
        base_url + path,
        data=body,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    started = time.perf_counter()
    try:
        with urlopen(request, timeout=10) as response:
            status = response.status
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as response:
        status = response.code
        result = json.loads(response.read().decode("utf-8"))
    elapsed_ms = (time.perf_counter() - started) * 1000
    return status, result, elapsed_ms


def expect(condition: bool, description: str) -> None:
    if not condition:
        raise AssertionError(description)


def one_item_sale(request_id: str, seller: str) -> dict:
    return {
        "seller": seller,
        "request_id": request_id,
        "items": [{"product_id": "P-001", "quantity": 1}],
    }


def main() -> int:
    port = find_free_port()
    base_url = f"http://127.0.0.1:{port}"
    cases: list[tuple[str, str]] = []
    timings: dict[str, object] = {}

    with tempfile.TemporaryDirectory(prefix="pos_tornillo_test_") as temp_dir:
        env = os.environ.copy()
        env["POS_DB_PATH"] = str(Path(temp_dir) / "pos_test.sqlite3")
        process = subprocess.Popen(
            [sys.executable, str(PROJECT_ROOT / "server.py"), "--port", str(port)],
            cwd=PROJECT_ROOT,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            for _ in range(60):
                if process.poll() is not None:
                    raise RuntimeError("El servidor POS se cerró durante el arranque.")
                try:
                    status, _, _ = request_json(base_url, "/api/health")
                    if status == 200:
                        break
                except (URLError, TimeoutError):
                    time.sleep(0.1)
            else:
                raise RuntimeError("El servidor POS no respondió dentro de 6 segundos.")

            request_json(base_url, "/api/reset", method="POST", payload={})

            # T07: sobreventa rechazada y stock sin cambios.
            status, body, _ = request_json(
                base_url,
                "/api/sales",
                "POST",
                {"seller": "QA demo", "request_id": "oversell", "items": [{"product_id": "P-001", "quantity": 13}]},
            )
            products = request_json(base_url, "/api/products")[1]["products"]
            p001 = next(item for item in products if item["id"] == "P-001")
            expect(status == 409 and body.get("code") == "insufficient_stock" and p001["stock"] == 12, "Sobreventa no rechazada sin alterar stock")
            cases.append(("Sobreventa 13/12", "PASS — HTTP 409; stock permanece en 12."))

            # T07/RNF-03: error previo al commit produce rollback completo.
            status, body, _ = request_json(
                base_url,
                "/api/sales",
                "POST",
                {"seller": "QA demo", "request_id": "rollback", "items": [{"product_id": "P-001", "quantity": 2}], "simulate_error": True},
            )
            products = request_json(base_url, "/api/products")[1]["products"]
            p001 = next(item for item in products if item["id"] == "P-001")
            sales = request_json(base_url, "/api/sales")[1]["sales"]
            expect(status == 500 and body.get("code") == "simulated_save_error" and p001["stock"] == 12 and not sales, "Rollback no conservó stock y venta consistentemente")
            cases.append(("Error de guardado", "PASS — rollback; stock 12 y ninguna venta persistida."))

            # T06: venta válida y persistencia consultable.
            status, body, _ = request_json(
                base_url,
                "/api/sales",
                "POST",
                {"seller": "QA demo", "request_id": "valid-sale", "items": [{"product_id": "P-001", "quantity": 2}]},
            )
            expect(status == 201 and body["sale"]["seller"] == "QA demo" and body["sale"]["items"][0]["quantity"] == 2, "No se registró la venta válida")
            products = request_json(base_url, "/api/products")[1]["products"]
            p001 = next(item for item in products if item["id"] == "P-001")
            expect(p001["stock"] == 10 and len(request_json(base_url, "/api/sales")[1]["sales"]) == 1, "Venta no persistió o no descontó stock")
            cases.append(("Venta persistida", "PASS — vendedor, fecha/hora, detalle; stock de 12 a 10."))

            # T07: mismo identificador de reintento no duplica descuento.
            idempotent_payload = {"seller": "QA demo", "request_id": "retry-once", "items": [{"product_id": "P-002", "quantity": 1}]}
            first_status, first, _ = request_json(base_url, "/api/sales", "POST", idempotent_payload)
            second_status, second, _ = request_json(base_url, "/api/sales", "POST", idempotent_payload)
            products = request_json(base_url, "/api/products")[1]["products"]
            p002 = next(item for item in products if item["id"] == "P-002")
            expect(first_status == 201 and second_status == 200 and second.get("idempotent_replay") is True and p002["stock"] == 9, "Reintento idempotente duplicó venta o descuento")
            cases.append(("Reintento idempotente", "PASS — la repetición devolvió la venta existente; un solo descuento."))

            # T08: frontera de 10/9 y T09 filtros vendedor/fecha.
            request_json(base_url, "/api/reset", method="POST", payload={})
            status10, sale10, _ = request_json(base_url, "/api/sales", "POST", {"seller": "Filtro demo", "request_id": "threshold-10", "items": [{"product_id": "P-003", "quantity": 1}]})
            alerts10 = request_json(base_url, "/api/alerts")[1]["alerts"]
            status9, sale9, _ = request_json(base_url, "/api/sales", "POST", {"seller": "Filtro demo", "request_id": "threshold-9", "items": [{"product_id": "P-003", "quantity": 1}]})
            alerts9 = request_json(base_url, "/api/alerts")[1]["alerts"]
            sale_date = sale9["sale"]["created_at"][:10]
            filtered_seller = request_json(base_url, "/api/sales?seller=Filtro%20demo")[1]["sales"]
            filtered_date = request_json(base_url, f"/api/sales?date={sale_date}")[1]["sales"]
            other_date = (date.fromisoformat(sale_date) - timedelta(days=1)).isoformat()
            filtered_other_date = request_json(base_url, f"/api/sales?date={other_date}")[1]["sales"]
            expect(status10 == 201 and not alerts10 and status9 == 201 and len(alerts9) == 1 and alerts9[0]["stock"] == 9, "Umbral de alerta 10/9 incorrecto")
            expect(len(filtered_seller) == 2 and len(filtered_date) == 2 and not filtered_other_date, "Filtro de historial no devolvió resultados esperados")
            cases.append(("Alerta y filtros", "PASS — 10 sin alerta; 9 con alerta; filtros vendedor/fecha comprobados."))

            # T11: doce solicitudes de venta válidas en paralelo, sobre stock 12.
            request_json(base_url, "/api/reset", method="POST", payload={})
            with ThreadPoolExecutor(max_workers=12) as pool:
                concurrent_results = list(pool.map(
                    lambda i: request_json(base_url, "/api/sales", "POST", one_item_sale(f"load-12-{i}", f"Vendedor {i:02d}")),
                    range(12),
                ))
            codes = [status for status, _, _ in concurrent_results]
            latencies = [elapsed for _, _, elapsed in concurrent_results]
            sorted_latencies = sorted(latencies)
            p95_ms = sorted_latencies[math.ceil(0.95 * len(sorted_latencies)) - 1]
            products = request_json(base_url, "/api/products")[1]["products"]
            p001 = next(item for item in products if item["id"] == "P-001")
            sale_count = len(request_json(base_url, "/api/sales")[1]["sales"])
            expect(codes == [201] * 12 and p001["stock"] == 0 and sale_count == 12, "La carga de 12 sesiones perdió ventas o produjo stock inesperado")
            expect(max(latencies) <= 3000, "Al menos una sesión superó 3 segundos")
            timings["12_sessions"] = {
                "sessions": 12,
                "successes": codes.count(201),
                "stock_final": p001["stock"],
                "sales_persisted": sale_count,
                "min_ms": round(min(latencies), 2),
                "mean_ms": round(sum(latencies) / len(latencies), 2),
                "p95_ms": round(p95_ms, 2),
                "max_ms": round(max(latencies), 2),
            }
            cases.append(("RNF-02 / 12 sesiones", f"PASS — 12/12 confirmadas; máximo {max(latencies):.2f} ms; stock de 12 a 0."))

            # RNF-03: 13 solicitudes simultáneas compiten por stock 12.
            request_json(base_url, "/api/reset", method="POST", payload={})
            with ThreadPoolExecutor(max_workers=13) as pool:
                race_results = list(pool.map(
                    lambda i: request_json(base_url, "/api/sales", "POST", one_item_sale(f"race-13-{i}", f"Concurrente {i:02d}")),
                    range(13),
                ))
            race_codes = [status for status, _, _ in race_results]
            products = request_json(base_url, "/api/products")[1]["products"]
            p001 = next(item for item in products if item["id"] == "P-001")
            race_sales = request_json(base_url, "/api/sales")[1]["sales"]
            expect(race_codes.count(201) == 12 and race_codes.count(409) == 1 and p001["stock"] == 0 and len(race_sales) == 12, "La carrera concurrente permitió stock negativo o venta extra")
            timings["13_competing_requests"] = {"requests": 13, "successes": race_codes.count(201), "rejected": race_codes.count(409), "stock_final": p001["stock"]}
            cases.append(("Integridad ante concurrencia", "PASS — 12 ventas aceptadas de 13; una rechazada; stock final 0."))

            report_date = date.today().isoformat()
            environment = f"{platform.system()} {platform.release()} · Python {platform.python_version()} · SQLite {__import__('sqlite3').sqlite_version} · localhost"
            report_lines = [
                "# T11 — Evidencia de API y carga local de 12 sesiones",
                "",
                f"**Fecha de ejecución:** {report_date}  ",
                f"**Entorno:** {environment}  ",
                "**Datos:** catálogo ficticio; base SQLite temporal, aislada de la demo del usuario.  ",
                "**Alcance:** solicitudes HTTP paralelas al servidor local; no son 12 vendedores reales ni una prueba sobre red/internet.",
                "",
                "## Resultados",
                "",
            ]
            report_lines.extend(f"- **{name}:** {result}" for name, result in cases)
            report_lines.extend([
                "",
                "## Mediciones de las 12 sesiones",
                "",
                f"- Confirmaciones: {timings['12_sessions']['successes']}/12.",
                f"- Tiempo mínimo: {timings['12_sessions']['min_ms']} ms.",
                f"- Tiempo promedio: {timings['12_sessions']['mean_ms']} ms.",
                f"- Percentil 95: {timings['12_sessions']['p95_ms']} ms.",
                f"- Tiempo máximo: {timings['12_sessions']['max_ms']} ms.",
                "- Requisito técnico observado: máximo ≤ 3000 ms en esta ejecución local.",
                "",
                "## Límites",
                "",
                "La medición corresponde a un único equipo y base local con datos sintéticos. No caracteriza el servidor del negocio ni garantiza rendimiento en producción. La concurrencia se simuló con clientes HTTP de prueba. Se necesita repetir con el entorno acordado si el docente exige otra carga o plataforma.",
                "",
                "La aplicación no incorpora autenticación/roles, canal de alerta externo, copias de seguridad ni datos reales. La prueba técnica no reemplaza la prueba de usabilidad con vendedores (T10) ni la aceptación del dueño (T12).",
                "",
            ])
            EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
            EVIDENCE_PATH.write_text("\n".join(report_lines), encoding="utf-8")
            print(json.dumps({"result":"PASS", "checks":cases, "measurements":timings, "report":str(EVIDENCE_PATH)}, ensure_ascii=False, indent=2))
            return 0
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
