"""Sesión 9 - Ejercicio 2: cliente de API robusto (timeouts, reintentos y errores).

Arranca antes la API simulada en otra terminal:
    python -m comun.api_backlog --fallos 0.3
y ejecuta:
    python sesion_09_herramientas_apis/ejercicios/s09_ej2_cliente_api.py
"""

from __future__ import annotations

import os
import time
from typing import Any, Callable

import httpx

URL_API = os.getenv("API_BACKLOG_URL", "http://127.0.0.1:8765")
CODIGOS_TRANSITORIOS = {429, 500, 502, 503, 504}


class ErrorAPI(Exception):
    """Error de la API con código HTTP (None si no hubo respuesta) y detalle."""

    def __init__(self, codigo: int | None, detalle: str) -> None:
        super().__init__(f"{codigo}: {detalle}" if codigo else detalle)
        self.codigo, self.detalle = codigo, detalle


def espera_exponencial(intento: int, base: float = 0.5, maximo: float = 8.0) -> float:
    """Segundos de espera antes del reintento ``intento`` (1, 2, 3…): base × 2^(intento−1), sin superar ``maximo``."""
    raise NotImplementedError("Completa este bloque")


class ClienteBacklog:
    def __init__(self, url: str = URL_API, clave: str | None = None, tiempo_maximo: float = 5.0, reintentos: int = 3,
                 transporte: httpx.BaseTransport | None = None, dormir: Callable[[float], None] = time.sleep) -> None:
        self.http = httpx.Client(base_url=url, timeout=tiempo_maximo, transport=transporte,
                                 headers={"X-Api-Key": clave or os.getenv("API_BACKLOG_CLAVE", "clave-curso")})
        self.reintentos, self.dormir = reintentos, dormir
        self.intentos_realizados = 0

    def _peticion(self, metodo: str, ruta: str, **opciones: Any) -> Any:
        """Hace la petición con reintentos y devuelve el JSON.

        - Respuesta 2xx → devuelve ``respuesta.json()``.
        - Código transitorio (``CODIGOS_TRANSITORIOS``) o ``httpx.TransportError`` (incluye timeouts):
          reintenta hasta ``reintentos`` veces, esperando ``espera_exponencial(n)`` con ``self.dormir``.
          Si se agotan, lanza ``ErrorAPI`` con el último código (None si fue de transporte).
        - Otro código 4xx/5xx → ``ErrorAPI`` inmediato con el campo «error» del JSON (o el texto).
        ``self.intentos_realizados`` cuenta todas las peticiones enviadas.
        """
        raise NotImplementedError("Completa este bloque")

    def listar(self, estado: str | None = None, sprint: int | None = None) -> list[dict]:
        """``GET /historias`` con los filtros que no sean None como parámetros de consulta."""
        raise NotImplementedError("Completa este bloque")

    def obtener(self, identificador: str) -> dict:
        raise NotImplementedError("Completa este bloque")

    def actualizar_estado(self, identificador: str, estado: str) -> dict:
        """``PATCH /historias/<id>`` con el cuerpo JSON ``{"estado": estado}``."""
        raise NotImplementedError("Completa este bloque")


if __name__ == "__main__":
    cliente = ClienteBacklog()
    try:
        historias = cliente.listar(sprint=23)
        print(f"{len(historias)} historias del sprint 23 en {cliente.intentos_realizados} intentos")
        print(cliente.obtener("FARO-142")["titulo"])
        cliente.obtener("FARO-999")
    except ErrorAPI as error:
        print("ErrorAPI:", error.codigo, error.detalle)
