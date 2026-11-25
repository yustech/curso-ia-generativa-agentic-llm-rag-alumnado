"""Sesión 8 - Ejercicio 3: memoria y estado de un agente."""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402


def tokens_aproximados(mensajes: list[dict[str, Any]]) -> int:
    """Estimación rápida: palabras de todos los contenidos × 1,5, redondeado hacia arriba (int)."""
    raise NotImplementedError("Completa este bloque")


class MemoriaVentana:
    """Memoria de corto plazo: conserva el mensaje de sistema y los últimos ``max_mensajes`` mensajes."""

    def __init__(self, sistema: str, max_mensajes: int = 6) -> None:
        self.sistema = {"role": "system", "content": sistema}
        self.max_mensajes = max_mensajes
        self.mensajes: list[dict[str, Any]] = []

    def agregar(self, rol: str, contenido: str) -> None:
        raise NotImplementedError("Completa este bloque")

    def contexto(self) -> list[dict[str, Any]]:
        """Sistema + últimos ``max_mensajes``. Si el primero de la ventana es de rol ``assistant``,
        se descarta para que el contexto empiece siempre por un mensaje del usuario."""
        raise NotImplementedError("Completa este bloque")


class MemoriaResumen(MemoriaVentana):
    """Cuando el historial supera ``umbral_tokens``, resume con el LLM todo menos los ``conservar`` últimos
    mensajes y guarda el resumen, que se añade al mensaje de sistema."""

    def __init__(self, sistema: str, umbral_tokens: int = 800, conservar: int = 4) -> None:
        super().__init__(sistema, max_mensajes=10_000)
        self.umbral_tokens, self.conservar = umbral_tokens, conservar
        self.resumen = ""

    def compactar(self) -> bool:
        """Si hace falta, resume y recorta. Devuelve True si ha compactado.

        El prompt de resumen incluye el resumen anterior (si lo hay) y los mensajes antiguos
        como líneas «rol: contenido». El nuevo resumen sustituye al anterior.
        """
        raise NotImplementedError("Completa este bloque")

    def contexto(self) -> list[dict[str, Any]]:
        """Como la ventana, pero con «Resumen de la conversación anterior: …» al final del mensaje de sistema."""
        raise NotImplementedError("Completa este bloque")


@dataclass
class EstadoPeticion:
    """Estado estructurado de una petición de entorno (memoria de trabajo del agente InfraPilot)."""

    proyecto: str | None = None
    entorno: str | None = None
    centro_coste: str | None = None
    recursos: list[str] = field(default_factory=list)
    aprobada: bool = False

    OBLIGATORIOS = ("proyecto", "entorno", "centro_coste", "recursos")

    def faltan(self) -> list[str]:
        """Campos obligatorios vacíos (None, "" o lista vacía), en el orden de ``OBLIGATORIOS``."""
        raise NotImplementedError("Completa este bloque")

    def actualizar(self, **datos: Any) -> list[str]:
        """Actualiza solo los campos conocidos con valores no vacíos y devuelve los nombres actualizados.
        ``entorno`` solo admite «dev», «pre» o «pro» (si no, ``ValueError``). Los recursos se añaden
        a los existentes sin duplicar."""
        raise NotImplementedError("Completa este bloque")

    def como_texto(self) -> str:
        """Resumen para el prompt: «proyecto=faro · entorno=pre · centro_coste=? · recursos=vm_linux, red_base · aprobada=no»."""
        raise NotImplementedError("Completa este bloque")
