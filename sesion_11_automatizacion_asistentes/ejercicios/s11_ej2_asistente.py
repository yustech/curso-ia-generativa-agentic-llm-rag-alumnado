"""Sesión 11 - Ejercicio 2: el núcleo de un asistente conversacional.

El asistente se presenta como IA, mantiene una memoria de ventana, consulta la
documentación cuando se le da un buscador, cita fuentes y deriva a una persona
cuando hace falta. La interfaz (ejercicio 3) solo dibuja lo que devuelve.
"""

from __future__ import annotations

import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402

FRASES_ESCALADO = ["hablar con una persona", "hablar con alguien", "quiero un humano", "persona real", "reclamacion",
                   "queja formal", "es urgente", "denuncia", "acoso"]
MENSAJE_ESCALADO = ("Entiendo. Esta consulta la debe atender una persona. He registrado tu petición y el equipo "
                    "responsable te contactará; si es urgente, llama a la extensión 4000.")


def _normal(texto: str) -> str:
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def necesita_humano(mensaje: str) -> bool:
    """True si el mensaje contiene alguna de ``FRASES_ESCALADO`` (sin distinguir mayúsculas ni tildes)."""
    raise NotImplementedError("Completa este bloque")


@dataclass
class Respuesta:
    texto: str
    fuentes: list[str] = field(default_factory=list)
    escalado: bool = False


class Asistente:
    def __init__(self, nombre: str, sistema: str, buscar: Callable[[str, int], list] | None = None,
                 k: int = 3, max_mensajes: int = 6) -> None:
        self.nombre, self.sistema, self.buscar, self.k, self.max_mensajes = nombre, sistema, buscar, k, max_mensajes
        self.historial: list[dict] = []

    def bienvenida(self) -> str:
        """Mensaje de bienvenida que deja claro que es un asistente de IA (obligación de transparencia):
        «Hola, soy <nombre>, un asistente de inteligencia artificial de Atlántica Logística. …»."""
        raise NotImplementedError("Completa este bloque")

    def _contexto(self, pregunta: str) -> tuple[str, list[str]]:
        """Fragmentos numerados y sus referencias. ``buscar`` devuelve ``[(trozo, puntuación)]`` y cada trozo
        tiene ``referencia`` y ``texto``. Sin buscador, ``("", [])``."""
        raise NotImplementedError("Completa este bloque")

    def responder(self, mensaje: str) -> Respuesta:
        """Un turno de conversación.

        1. Si ``necesita_humano(mensaje)``: devuelve ``MENSAJE_ESCALADO`` con ``escalado=True`` (sin llamar al modelo),
           y guarda ambos mensajes en el historial.
        2. Si no: construye los mensajes = sistema + últimos ``max_mensajes`` del historial + mensaje del usuario
           (si hay contexto, el mensaje del usuario es «<fragmentos>\\n\\nPregunta: <mensaje>»), llama a ``llm.chat``,
           guarda en el historial el mensaje ORIGINAL del usuario y la respuesta, y devuelve la respuesta con las
           referencias de los fragmentos citados con [n].
        """
        raise NotImplementedError("Completa este bloque")

    def reiniciar(self) -> None:
        self.historial.clear()


def asistente_atlantica() -> Asistente:
    """Asistente general de Atlántica con el buscador de referencia."""
    from comun.buscador import BuscadorSemantico

    buscador = BuscadorSemantico.de_documentos()
    return Asistente("Faro-IA", "Eres el asistente interno de Atlántica Logística. Responde en español, en pocas frases, "
                     "solo con la información de los fragmentos y citando [n]. Si no está, di «No consta en la documentación».",
                     buscar=buscador.buscar)
