"""Servidor académico local para el prototipo POS El Tornillo.

Utiliza únicamente la biblioteca estándar de Python y SQLite. Se enlaza
solo a 127.0.0.1 y usa productos ficticios de demostración.
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


PROJECT_ROOT = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("POS_DB_PATH", PROJECT_ROOT / "data" / "pos_demo.sqlite3"))
DEMO_PRODUCTS = (
    ("P-001", "Tornillo demo 2 pulgadas", 12, 10),
    ("P-002", "Martillo demo", 10, 10),
    ("P-003", "Guantes demo", 11, 10),
)


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str, **details: object) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message
        self.details = details


def open_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout = 10000")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_db() -> None:
    with open_db() as conn:
        conn.execute("PRAGMA journal_mode = WAL")
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                stock INTEGER NOT NULL CHECK (stock >= 0),
                threshold INTEGER NOT NULL DEFAULT 10 CHECK (threshold >= 0)
            );
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id TEXT NOT NULL UNIQUE,
                seller TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sale_lines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL REFERENCES sales(id) ON DELETE CASCADE,
                product_id TEXT NOT NULL REFERENCES products(id),
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity > 0)
            );
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT NOT NULL REFERENCES products(id),
                product_name TEXT NOT NULL,
                stock INTEGER NOT NULL CHECK (stock >= 0),
                created_at TEXT NOT NULL,
                channel_status TEXT NOT NULL DEFAULT 'pendiente'
            );
            """
        )
        count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count == 0:
            conn.executemany(
                "INSERT INTO products (id, name, stock, threshold) VALUES (?, ?, ?, ?)",
                DEMO_PRODUCTS,
            )


def reset_demo_db() -> None:
    with open_db() as conn:
        conn.execute("BEGIN IMMEDIATE")
        conn.execute("DELETE FROM alerts")
        conn.execute("DELETE FROM sale_lines")
        conn.execute("DELETE FROM sales")
        conn.execute("DELETE FROM products")
        conn.executemany(
            "INSERT INTO products (id, name, stock, threshold) VALUES (?, ?, ?, ?)",
            DEMO_PRODUCTS,
        )
        conn.execute("COMMIT")


def list_products() -> list[dict[str, object]]:
    with open_db() as conn:
        rows = conn.execute("SELECT id, name, stock, threshold FROM products ORDER BY id").fetchall()
        return [dict(row) for row in rows]


def sale_detail(conn: sqlite3.Connection, sale_id: int) -> dict[str, object] | None:
    sale = conn.execute(
        "SELECT id, request_id, seller, created_at FROM sales WHERE id = ?", (sale_id,)
    ).fetchone()
    if sale is None:
        return None
    lines = conn.execute(
        "SELECT product_id, product_name, quantity FROM sale_lines WHERE sale_id = ? ORDER BY id",
        (sale_id,),
    ).fetchall()
    result = dict(sale)
    result["items"] = [dict(line) for line in lines]
    return result


def list_sales(seller: str = "", sale_date: str = "") -> list[dict[str, object]]:
    clauses: list[str] = []
    values: list[str] = []
    if seller:
        clauses.append("LOWER(seller) LIKE LOWER(?)")
        values.append(f"%{seller}%")
    if sale_date:
        clauses.append("substr(created_at, 1, 10) = ?")
        values.append(sale_date)
    where = " WHERE " + " AND ".join(clauses) if clauses else ""
    with open_db() as conn:
        rows = conn.execute(
            "SELECT id FROM sales" + where + " ORDER BY id DESC", values
        ).fetchall()
        return [sale_detail(conn, int(row["id"])) for row in rows]


def list_alerts() -> list[dict[str, object]]:
    with open_db() as conn:
        rows = conn.execute(
            "SELECT id, product_id, product_name, stock, created_at, channel_status "
            "FROM alerts ORDER BY id DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def create_sale(payload: object) -> tuple[int, dict[str, object]]:
    if not isinstance(payload, dict):
        raise ApiError(400, "invalid_body", "El cuerpo de la solicitud no es válido.")

    seller = payload.get("seller")
    request_id = payload.get("request_id")
    items = payload.get("items")
    if not isinstance(seller, str) or not seller.strip() or len(seller.strip()) > 80:
        raise ApiError(400, "invalid_seller", "Escribe un vendedor válido (máximo 80 caracteres).")
    if not isinstance(request_id, str) or not request_id.strip() or len(request_id) > 100:
        raise ApiError(400, "invalid_request_id", "La solicitud requiere un identificador válido.")
    if not isinstance(items, list) or not items:
        raise ApiError(400, "empty_sale", "Agrega al menos un producto al detalle.")

    quantities: dict[str, int] = {}
    for item in items:
        if not isinstance(item, dict):
            raise ApiError(400, "invalid_item", "El detalle de la venta contiene un producto inválido.")
        product_id = item.get("product_id")
        quantity = item.get("quantity")
        if not isinstance(product_id, str) or not product_id:
            raise ApiError(400, "invalid_product", "Cada producto requiere un código válido.")
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
            raise ApiError(400, "invalid_quantity", "Las cantidades deben ser enteros mayores que cero.")
        quantities[product_id] = quantities.get(product_id, 0) + quantity

    with open_db() as conn:
        try:
            conn.execute("BEGIN IMMEDIATE")

            prior = conn.execute("SELECT id FROM sales WHERE request_id = ?", (request_id,)).fetchone()
            if prior:
                existing = sale_detail(conn, int(prior["id"]))
                conn.execute("COMMIT")
                return 200, {"sale": existing, "alerts": [], "idempotent_replay": True}

            products: list[sqlite3.Row] = []
            for product_id, quantity in quantities.items():
                product = conn.execute(
                    "SELECT id, name, stock, threshold FROM products WHERE id = ?", (product_id,)
                ).fetchone()
                if product is None:
                    raise ApiError(404, "product_not_found", f"No se encontró el producto {product_id}.")
                if quantity > int(product["stock"]):
                    raise ApiError(
                        409,
                        "insufficient_stock",
                        f"Stock insuficiente para {product['name']}. Disponible: {product['stock']}.",
                        product_id=product_id,
                        available=int(product["stock"]),
                    )
                products.append(product)

            now = datetime.now().astimezone().isoformat(timespec="seconds")
            resulting_stock: dict[str, int] = {}
            for product in products:
                product_id = str(product["id"])
                quantity = quantities[product_id]
                cursor = conn.execute(
                    "UPDATE products SET stock = stock - ? WHERE id = ? AND stock >= ?",
                    (quantity, product_id, quantity),
                )
                if cursor.rowcount != 1:
                    raise ApiError(409, "insufficient_stock", "El stock cambió; vuelve a consultar e intenta otra vez.")
                resulting_stock[product_id] = int(product["stock"]) - quantity

            if payload.get("simulate_error") is True:
                raise ApiError(500, "simulated_save_error", "Error simulado al guardar la venta.")

            cursor = conn.execute(
                "INSERT INTO sales (request_id, seller, created_at) VALUES (?, ?, ?)",
                (request_id, seller.strip(), now),
            )
            sale_id = int(cursor.lastrowid)
            for product in products:
                product_id = str(product["id"])
                quantity = quantities[product_id]
                conn.execute(
                    "INSERT INTO sale_lines (sale_id, product_id, product_name, quantity) VALUES (?, ?, ?, ?)",
                    (sale_id, product_id, str(product["name"]), quantity),
                )

            alert_rows: list[dict[str, object]] = []
            for product in products:
                product_id = str(product["id"])
                stock = resulting_stock[product_id]
                if stock < int(product["threshold"]):
                    conn.execute(
                        "INSERT INTO alerts (product_id, product_name, stock, created_at) VALUES (?, ?, ?, ?)",
                        (product_id, str(product["name"]), stock, now),
                    )
                    alert_rows.append(
                        {"product_id": product_id, "product_name": str(product["name"]), "stock": stock, "created_at": now}
                    )

            conn.execute("COMMIT")
            return 201, {"sale": sale_detail(conn, sale_id), "alerts": alert_rows, "idempotent_replay": False}
        except ApiError:
            if conn.in_transaction:
                conn.execute("ROLLBACK")
            raise
        except sqlite3.IntegrityError as exc:
            if conn.in_transaction:
                conn.execute("ROLLBACK")
            raise ApiError(409, "integrity_error", "No se pudo guardar la venta por un conflicto de inventario.") from exc
        except Exception:
            if conn.in_transaction:
                conn.execute("ROLLBACK")
            raise


class PosHandler(BaseHTTPRequestHandler):
    server_version = "PosDemo/1.0"

    def log_message(self, format_string: str, *args: object) -> None:
        # The server logs status and duration without including sale payloads.
        super().log_message(format_string, *args)

    def send_json(self, status: int, payload: object) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> object:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ApiError(400, "invalid_length", "Longitud de solicitud inválida.") from exc
        if length <= 0 or length > 100_000:
            raise ApiError(400, "invalid_length", "La solicitud está vacía o supera el límite permitido.")
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ApiError(400, "invalid_json", "El JSON enviado no es válido.") from exc

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            self.send_json(200, {"ok": True, "storage": "SQLite local", "demo_data": True})
        elif parsed.path == "/api/products":
            self.send_json(200, {"products": list_products()})
        elif parsed.path == "/api/sales":
            query = parse_qs(parsed.query)
            self.send_json(
                200,
                {"sales": list_sales(query.get("seller", [""])[0], query.get("date", [""])[0])},
            )
        elif parsed.path == "/api/alerts":
            self.send_json(200, {"alerts": list_alerts()})
        elif parsed.path in ("/", "/app.html"):
            self.serve_app()
        elif parsed.path == "/index.html":
            self.serve_static(PROJECT_ROOT / "index.html", "text/html; charset=utf-8")
        else:
            self.send_json(404, {"error": "No se encontró el recurso."})

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        try:
            if parsed.path == "/api/sales":
                status, payload = create_sale(self.read_json())
                self.send_json(status, payload)
            elif parsed.path == "/api/reset":
                reset_demo_db()
                self.send_json(200, {"ok": True, "message": "Datos demo restablecidos."})
            else:
                self.send_json(404, {"error": "No se encontró el recurso."})
        except ApiError as exc:
            self.send_json(exc.status, {"code": exc.code, "error": exc.message, **exc.details})
        except Exception:
            self.send_json(500, {"code": "internal_error", "error": "Ocurrió un error interno al procesar la solicitud."})

    def serve_static(self, path: Path, content_type: str) -> None:
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def serve_app(self) -> None:
        self.serve_static(PROJECT_ROOT / "app.html", "text/html; charset=utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="POS académico local con datos ficticios.")
    parser.add_argument("--port", type=int, default=8000, help="Puerto local (por defecto 8000).")
    args = parser.parse_args()
    initialize_db()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), PosHandler)
    print(f"POS El Tornillo demo disponible en http://127.0.0.1:{args.port}/")
    print("Datos demo ficticios; escucha solo en localhost. Ctrl+C para detener.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
