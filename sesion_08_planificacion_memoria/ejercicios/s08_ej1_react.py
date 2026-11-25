"""Sesión 8 - Ejercicio 1: agente ReAct con trazas y detección de bucles.

    python sesion_08_planificacion_memoria/ejercicios/s08_ej1_react.py
"""

from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402
from comun.herramientas import ejecutar_herramienta  # noqa: E402
from comun.trazas import Traza  # noqa: E402


@dataclass
class Resultado:
    respuesta: str
    terminado: bool
    motivo: str  # "respuesta", "max_pasos" o "bucle"
    pasos: list[dict] = field(default_factory=list)
    llamadas_modelo: int = 0
    segundos: float = 0.0


class AgenteReAct:
    """Agente que alterna razonar (el modelo decide) y actuar (herramientas), con trazas."""

    def __init__(self, registro: dict[str, Callable[..., Any]], herramientas: list[dict], sistema: str,
                 max_pasos: int = 6, max_repeticiones: int = 2, nombre_traza: str = "agente") -> None:
        self.registro, self.herramientas, self.sistema = registro, herramientas, sistema
        self.max_pasos, self.max_repeticiones = max_pasos, max_repeticiones
        self.traza = Traza(nombre_traza)

    @staticmethod
    def clave_llamada(nombre: str, argumentos: str) -> str:
        """Clave canónica de una llamada: ``nombre`` + argumentos JSON con las claves ordenadas.
        Si los argumentos no son JSON válido, se usan tal cual."""
        raise NotImplementedError("Completa este bloque")

    def ejecutar(self, objetivo: str) -> Resultado:
        """Bucle ReAct.

        - Registra en la traza un paso ``"inicio"`` con el objetivo.
        - En cada iteración llama al modelo (y suma ``llamadas_modelo``) y registra ``"modelo"`` con
          las herramientas pedidas (lista de nombres, vacía si responde).
        - Sin ``tool_calls``: registra ``"fin"`` y devuelve ``motivo="respuesta"``.
        - Con ``tool_calls``: para cada llamada, si la misma llamada (``clave_llamada``) ya se ha hecho
          ``max_repeticiones`` veces, registra ``"fin"`` y devuelve ``terminado=False, motivo="bucle"``.
          Si no, la ejecuta con ``ejecutar_herramienta``, la añade al historial, a ``pasos``
          (``{"herramienta", "argumentos", "resultado"}``) y registra ``"herramienta"``.
        - Al agotar ``max_pasos``: registra ``"fin"`` y devuelve ``terminado=False, motivo="max_pasos"``.
        ``segundos`` es el tiempo total.
        """
        raise NotImplementedError("Completa este bloque")


if __name__ == "__main__":
    from comun.herramientas import ESQUEMA_CALCULAR, buscar_documentacion, calcular, esquema_buscar_documentacion

    agente = AgenteReAct({"buscar_documentacion": buscar_documentacion, "calcular": calcular},
                         [esquema_buscar_documentacion(), ESQUEMA_CALCULAR],
                         sistema="Eres un asistente de Atlántica. Busca los datos en la documentación y usa calcular para las cuentas.",
                         nombre_traza="s08_react")
    r = agente.ejecutar("Una petición de entorno pre tiene red_base, un balanceador y dos máquinas t3.medium. "
                        "¿Cuánto cuesta al mes y entra en el límite que aprueba el responsable del proyecto?")
    print(r.respuesta, "\n")
    print(f"motivo={r.motivo} · llamadas al modelo={r.llamadas_modelo} · {r.segundos:.1f} s · traza: {agente.traza.fichero}")
