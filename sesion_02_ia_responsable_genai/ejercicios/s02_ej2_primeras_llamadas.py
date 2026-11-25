"""Sesión 2 - Ejercicio 2: primeras llamadas y una conversación con memoria."""

from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402

SISTEMA_ATLANTICA = (
    "Eres el asistente interno de Atlántica Logística. Respondes en español, con frases cortas. "
    "Si no sabes algo de la empresa, lo dices."
)


def preguntar(pregunta: str, sistema: str | None = SISTEMA_ATLANTICA, temperatura: float = 0.2) -> str:
    """Hace una pregunta suelta al modelo y devuelve el texto de la respuesta."""
    raise NotImplementedError("Completa este bloque")


class Conversacion:
    """Conversación que conserva el historial y lo reenvía en cada turno."""

    def __init__(self, sistema: str = SISTEMA_ATLANTICA) -> None:
        self.historial: list[dict[str, Any]] = [{"role": "system", "content": sistema}]

    def enviar(self, texto: str) -> str:
        """Añade el mensaje del usuario, llama al modelo con TODO el historial,
        añade la respuesta como mensaje ``assistant`` y la devuelve."""
        raise NotImplementedError("Completa este bloque")

    @property
    def turnos(self) -> int:
        """Número de mensajes del usuario enviados."""
        raise NotImplementedError("Completa este bloque")


def medir(funcion: Callable[..., Any], *args: Any, **kwargs: Any) -> tuple[Any, float]:
    """Ejecuta ``funcion`` y devuelve ``(resultado, segundos)`` medidos con ``time.perf_counter``."""
    raise NotImplementedError("Completa este bloque")


if __name__ == "__main__":
    respuesta, segundos = medir(preguntar, "¿Qué es un TMS en logística?")
    print(f"{respuesta}\n({segundos:.1f} s)\n")
    charla = Conversacion()
    print(charla.enviar("Soy Iván, líder técnico del proyecto Faro 2.0."))
    print(charla.enviar("¿En qué proyecto trabajo?"))
    print(f"Turnos: {charla.turnos}")
