"""Registro de herramientas con contrato (versión de partida de la sesión 9).

Cada herramienta declara un modelo Pydantic de argumentos. El registro:

- genera el esquema que ve el modelo a partir del modelo Pydantic;
- valida los argumentos antes de ejecutar y devuelve errores útiles al modelo;
- marca las herramientas con efectos, que solo se ejecutan si una persona confirma.

    registro = Registro()

    class ArgsBuscar(BaseModel):
        consulta: str = Field(description="Qué buscar")

    @registro.herramienta(ArgsBuscar)
    def buscar(consulta: str) -> str:
        "Busca en la documentación."
        ...
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable

from pydantic import BaseModel, ValidationError

Confirmador = Callable[[str, dict[str, Any]], bool]


def denegar_siempre(nombre: str, argumentos: dict[str, Any]) -> bool:
    """Confirmador por defecto: sin una persona que confirme, no se ejecuta nada con efectos."""
    return False


@dataclass
class Herramienta:
    nombre: str
    descripcion: str
    argumentos: type[BaseModel]
    funcion: Callable[..., Any]
    con_efectos: bool = False

    def esquema(self) -> dict[str, Any]:
        parametros = self.argumentos.model_json_schema()
        parametros.pop("title", None)
        return {"type": "function", "function": {"name": self.nombre, "description": self.descripcion,
                                                 "parameters": parametros}}


class Registro:
    def __init__(self, confirmador: Confirmador = denegar_siempre) -> None:
        self.herramientas: dict[str, Herramienta] = {}
        self.confirmador = confirmador

    def herramienta(self, argumentos: type[BaseModel], *, con_efectos: bool = False, nombre: str | None = None,
                    descripcion: str | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorar(funcion: Callable[..., Any]) -> Callable[..., Any]:
            texto = descripcion or (funcion.__doc__ or "").strip()
            if not texto:
                raise ValueError(f"La herramienta {funcion.__name__} necesita una descripción para el modelo")
            self.agregar(Herramienta(nombre or funcion.__name__, texto, argumentos, funcion, con_efectos))
            return funcion

        return decorar

    def agregar(self, herramienta: Herramienta) -> None:
        self.herramientas[herramienta.nombre] = herramienta

    def esquemas(self) -> list[dict[str, Any]]:
        return [h.esquema() for h in self.herramientas.values()]

    def ejecutar(self, nombre: str, argumentos_json: str) -> str:
        """Firma ``ejecutor(nombre, argumentos_json) -> str`` que espera ``comun.agente.AgenteReAct``."""
        herramienta = self.herramientas.get(nombre)
        if herramienta is None:
            return f"ERROR: la herramienta {nombre!r} no existe. Disponibles: {', '.join(self.herramientas)}"
        try:
            datos = json.loads(argumentos_json or "{}")
            argumentos = herramienta.argumentos.model_validate(datos)
        except json.JSONDecodeError:
            return "ERROR: los argumentos no son un JSON válido"
        except ValidationError as error:
            detalles = "; ".join(f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in error.errors())
            return f"ERROR: argumentos no válidos: {detalles}. Corrígelos y vuelve a intentarlo."
        valores = argumentos.model_dump()
        if herramienta.con_efectos and not self.confirmador(nombre, valores):
            return f"ERROR: acción no autorizada: la persona no ha confirmado {nombre}. No la repitas."
        try:
            resultado = herramienta.funcion(**valores)
        except Exception as error:  # el error vuelve al modelo como texto
            return f"ERROR: {type(error).__name__}: {error}"
        return resultado if isinstance(resultado, str) else json.dumps(resultado, ensure_ascii=False, default=str)
