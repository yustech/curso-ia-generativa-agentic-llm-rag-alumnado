"""Sesión 9 - Ejercicio 3: agente con dos herramientas y recuperación ante fallos.

Con la API simulada arrancada (``python -m comun.api_backlog --fallos 0.3``):
    python sesion_09_herramientas_apis/ejercicios/s09_ej3_agente_backlog.py
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun.agente import AgenteReAct  # noqa: E402
from s09_ej1_herramientas import Registro  # noqa: E402
from s09_ej2_cliente_api import ClienteBacklog, ErrorAPI  # noqa: E402

Estado = Literal["Por hacer", "En curso", "En revisión", "Hecho"]


class ArgsListar(BaseModel):
    estado: Estado | None = Field(default=None, description="Filtrar por estado")
    sprint: int | None = Field(default=None, ge=1, description="Número de sprint")


class ArgsConsultar(BaseModel):
    identificador: str = Field(pattern=r"^FARO-\d+$", description="Identificador, por ejemplo FARO-142")


SISTEMA = ("Eres PMO Copilot, el asistente de proyectos de Atlántica Logística. Consulta el backlog con las herramientas; "
           "no inventes identificadores ni estados. Si una herramienta devuelve un error, explícalo y no inventes datos.")
MENSAJE_DEGRADADO = ("El sistema de seguimiento de proyectos no responde en este momento. No puedo darte datos fiables "
                     "del backlog; vuelve a intentarlo en unos minutos.")


def crear_registro(cliente: ClienteBacklog) -> Registro:
    """Registro con dos herramientas de SOLO LECTURA:

    - ``listar_historias(estado, sprint)``: devuelve una lista resumida ``{"id", "titulo", "estado", "puntos"}``.
    - ``consultar_historia(identificador)``: devuelve la historia completa.
    """
    registro = Registro()

    raise NotImplementedError("Completa este bloque")

    return registro


def api_disponible(cliente: ClienteBacklog) -> bool:
    """True si ``GET /salud`` responde (con los reintentos del cliente)."""
    raise NotImplementedError("Completa este bloque")


def responder(pregunta: str, cliente: ClienteBacklog, max_pasos: int = 5) -> str:
    """Si la API no está disponible devuelve ``MENSAJE_DEGRADADO`` sin llamar al modelo.
    Si lo está, ejecuta un ``AgenteReAct`` con el registro y devuelve su respuesta."""
    raise NotImplementedError("Completa este bloque")


if __name__ == "__main__":
    cliente = ClienteBacklog()
    for pregunta in ["¿Qué historias hay en el sprint 23 y cuántos puntos suman?",
                     "¿En qué estado está FARO-141 y quién es responsable?",
                     "¿Qué pasa con la historia FARO-999?"]:
        print(f"\n### {pregunta}\n{responder(pregunta, cliente)}")
    print(f"\nPeticiones HTTP realizadas (incluidos reintentos): {cliente.intentos_realizados}")
