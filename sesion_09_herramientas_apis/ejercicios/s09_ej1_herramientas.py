"""Sesión 9 - Ejercicio 1: herramientas con contrato validado.

Cada herramienta declara sus argumentos con un modelo Pydantic. De ese modelo
salen dos cosas a la vez: el JSON Schema que ve el LLM y la validación de lo
que el LLM propone antes de ejecutar nada.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, Callable

from pydantic import BaseModel, ValidationError


@dataclass
class ResultadoHerramienta:
    ok: bool
    datos: Any = None
    error: str | None = None
    segundos: float = 0.0

    def como_texto(self) -> str:
        """Texto para el mensaje ``tool``: ``{"ok": true, "datos": ...}`` o ``{"ok": false, "error": "..."}``
        (JSON sin escapar caracteres no ASCII; los datos no serializables se convierten con ``str``)."""
        raise NotImplementedError("Completa este bloque")


def describir_errores(error: ValidationError) -> str:
    """Errores de validación en una línea legible para el modelo:
    «Argumentos no válidos: campo1: mensaje; campo2: mensaje». Campos anidados unidos con «.»."""
    raise NotImplementedError("Completa este bloque")


class Registro:
    """Registro de herramientas con esquema y validación."""

    def __init__(self) -> None:
        self.herramientas: dict[str, tuple[Callable[..., Any], type[BaseModel], str, bool]] = {}

    def herramienta(self, argumentos: type[BaseModel], descripcion: str, con_efectos: bool = False):
        """Decorador que registra una función. El nombre de la herramienta es el de la función.

        Uso::

            @registro.herramienta(ArgsBuscar, "Busca historias del backlog")
            def buscar_historias(estado: str | None = None) -> list: ...
        """
        raise NotImplementedError("Completa este bloque")

    def esquemas(self) -> list[dict]:
        """Definiciones para la API (formato OpenAI). ``parameters`` es el ``model_json_schema()`` del modelo
        de argumentos, sin la clave ``title``. Si la herramienta tiene efectos, la descripción termina en
        « Acción con efectos: requiere confirmación humana.»"""
        raise NotImplementedError("Completa este bloque")

    def con_efectos(self) -> set[str]:
        return {n for n, (_, _, _, efectos) in self.herramientas.items() if efectos}

    def ejecutar(self, nombre: str, argumentos_json: str) -> ResultadoHerramienta:
        """Valida y ejecuta. Nunca lanza excepciones:

        - Herramienta inexistente → error «Herramienta desconocida: <nombre>».
        - JSON inválido → error «Los argumentos no son JSON válido».
        - Validación → error de ``describir_errores``.
        - Excepción de la función → error «<TipoDeExcepción>: <mensaje>».
        La función recibe los argumentos validados (``modelo.model_dump()``). ``segundos`` mide la ejecución.
        """
        raise NotImplementedError("Completa este bloque")

    def ejecutor(self) -> Callable[[str, str], str]:
        """Adaptador para ``comun.agente.AgenteReAct``: devuelve el texto del resultado."""
        return lambda nombre, argumentos: self.ejecutar(nombre, argumentos).como_texto()
