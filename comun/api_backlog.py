"""API REST simulada del backlog de Atlántica (para la sesión 9 y el reto PMO Copilot).

Arranca el servidor en otra terminal:

    python -m comun.api_backlog                      # sin fallos
    python -m comun.api_backlog --fallos 0.3          # 30 % de respuestas 503
    python -m comun.api_backlog --latencia 2          # 2 s de retraso por petición

Endpoints (JSON):

    GET   /salud
    GET   /historias?estado=En%20curso&sprint=23
    GET   /historias/FARO-142
    PATCH /historias/FARO-142      cuerpo {"estado": "En curso"}    cabecera X-Api-Key obligatoria

La clave de API por defecto es «clave-curso» (variable de entorno ``API_BACKLOG_CLAVE``).
"""

from __future__ import annotations

import argparse
import json
import os
import random
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from equipos.e3_pmo_copilot.herramientas import ESTADOS, Backlog

CLAVE = os.getenv("API_BACKLOG_CLAVE", "clave-curso")


def crear_manejador(backlog: Backlog, fallos: float, latencia: float):
    class Manejador(BaseHTTPRequestHandler):
        def _responder(self, codigo: int, cuerpo: object) -> None:
            datos = json.dumps(cuerpo, ensure_ascii=False).encode("utf-8")
            self.send_response(codigo)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(datos)))
            self.end_headers()
            self.wfile.write(datos)

        def _simular(self) -> bool:
            if latencia:
                time.sleep(latencia)
            if fallos and random.random() < fallos:
                self._responder(503, {"error": "Servicio no disponible temporalmente"})
                return True
            return False

        def do_GET(self) -> None:  # noqa: N802
            if self._simular():
                return
            url = urlparse(self.path)
            partes = [p for p in url.path.split("/") if p]
            if partes == ["salud"]:
                return self._responder(200, {"estado": "ok"})
            if partes == ["historias"]:
                q = parse_qs(url.query)
                sprint = int(q["sprint"][0]) if "sprint" in q else None
                return self._responder(200, backlog.listar(q.get("estado", [None])[0], sprint))
            if len(partes) == 2 and partes[0] == "historias":
                try:
                    return self._responder(200, backlog.obtener(partes[1]))
                except KeyError as error:
                    return self._responder(404, {"error": str(error)})
            self._responder(404, {"error": "Ruta no encontrada"})

        def do_PATCH(self) -> None:  # noqa: N802
            if self._simular():
                return
            if self.headers.get("X-Api-Key") != CLAVE:
                return self._responder(401, {"error": "Clave de API no válida"})
            partes = [p for p in urlparse(self.path).path.split("/") if p]
            if len(partes) != 2 or partes[0] != "historias":
                return self._responder(404, {"error": "Ruta no encontrada"})
            longitud = int(self.headers.get("Content-Length", 0))
            try:
                cuerpo = json.loads(self.rfile.read(longitud) or b"{}")
            except json.JSONDecodeError:
                return self._responder(400, {"error": "JSON no válido"})
            if cuerpo.get("estado") not in ESTADOS:
                return self._responder(422, {"error": f"Estado no válido. Valores: {', '.join(ESTADOS)}"})
            try:
                return self._responder(200, backlog.actualizar_estado(partes[1], cuerpo["estado"]))
            except KeyError as error:
                return self._responder(404, {"error": str(error)})

        def log_message(self, formato, *args) -> None:  # registro breve
            print(f"[api_backlog] {self.command} {self.path} {args[1] if len(args) > 1 else ''}")

    return Manejador


def main() -> None:
    parser = argparse.ArgumentParser(description="API REST simulada del backlog de Atlántica")
    parser.add_argument("--puerto", type=int, default=8765)
    parser.add_argument("--fallos", type=float, default=0.0, help="Proporción de respuestas 503 (0 a 1)")
    parser.add_argument("--latencia", type=float, default=0.0, help="Segundos de retraso por petición")
    parser.add_argument("--reiniciar", action="store_true", help="Restaura el backlog original")
    args = parser.parse_args()
    servidor = ThreadingHTTPServer(("127.0.0.1", args.puerto), crear_manejador(Backlog(reiniciar=args.reiniciar), args.fallos, args.latencia))
    print(f"API del backlog en http://127.0.0.1:{args.puerto} (fallos={args.fallos}, latencia={args.latencia}s). Ctrl+C para parar.")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
