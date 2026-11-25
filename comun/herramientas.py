"""Piezas de agente de referencia (equivalentes a tu ejercicio 3 de la sesión 7).

A partir de la sesión 8 los laboratorios las importan de aquí.
"""

from __future__ import annotations

import ast
import json
import operator
from typing import Any, Callable

_OPERADORES = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
               ast.Pow: operator.pow, ast.USub: operator.neg, ast.Mod: operator.mod}


def calcular(expresion: str) -> float:
    """Evalúa una expresión aritmética de forma segura (sin ``eval``)."""

    def evaluar(nodo: ast.AST) -> float:
        if isinstance(nodo, ast.Expression):
            return evaluar(nodo.body)
        if isinstance(nodo, ast.Constant) and isinstance(nodo.value, (int, float)) and not isinstance(nodo.value, bool):
            return nodo.value
        if isinstance(nodo, ast.BinOp) and type(nodo.op) in _OPERADORES:
            return _OPERADORES[type(nodo.op)](evaluar(nodo.left), evaluar(nodo.right))
        if isinstance(nodo, ast.UnaryOp) and type(nodo.op) in _OPERADORES:
            return _OPERADORES[type(nodo.op)](evaluar(nodo.operand))
        raise ValueError("Expresión no permitida")

    try:
        return evaluar(ast.parse(expresion.replace(",", "."), mode="eval"))
    except SyntaxError as error:
        raise ValueError(f"Expresión no válida: {expresion}") from error


def esquema(nombre: str, descripcion: str, propiedades: dict[str, dict], requeridas: list[str]) -> dict:
    return {"type": "function", "function": {"name": nombre, "description": descripcion,
                                             "parameters": {"type": "object", "properties": propiedades, "required": requeridas}}}


def ejecutar_herramienta(nombre: str, argumentos_json: str, registro: dict[str, Callable[..., Any]]) -> str:
    """Ejecuta una herramienta y devuelve texto; los errores vuelven como ``ERROR: ...``."""
    if nombre not in registro:
        return f"ERROR: la herramienta {nombre!r} no existe"
    try:
        resultado = registro[nombre](**json.loads(argumentos_json or "{}"))
    except Exception as error:
        return f"ERROR: {type(error).__name__}: {error}"
    return resultado if isinstance(resultado, str) else json.dumps(resultado, ensure_ascii=False, default=str)


ESQUEMA_CALCULAR = esquema("calcular", "Calcula una expresión aritmética. Úsala siempre para hacer cuentas.",
                           {"expresion": {"type": "string", "description": "Por ejemplo: (2 * 36 + 70) * 1.1"}}, ["expresion"])


def esquema_buscar_documentacion() -> dict:
    return esquema("buscar_documentacion",
                   "Busca en la documentación interna de Atlántica Logística (políticas, guías, procedimientos) "
                   "y devuelve los fragmentos más relevantes numerados.",
                   {"consulta": {"type": "string", "description": "Qué buscar, con palabras del tema"}}, ["consulta"])


_BUSCADORES: dict[bool, Any] = {}


def buscar_documentacion(consulta: str, k: int = 3) -> str:
    """Herramienta de RAG sobre la documentación de Atlántica (buscador de referencia con caché).

    Se guarda un buscador para el modelo real y otro para el LLM falso de los tests,
    porque sus vectores no son compatibles.
    """
    from comun import llm
    from comun.buscador import BuscadorSemantico, contexto_numerado

    modo = llm.es_falso()
    if modo not in _BUSCADORES:
        _BUSCADORES[modo] = BuscadorSemantico.de_documentos()
    return contexto_numerado(_BUSCADORES[modo].buscar(consulta, k))
