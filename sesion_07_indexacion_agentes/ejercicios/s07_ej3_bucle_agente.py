"""Sesión 7 - Ejercicio 3: tu primer bucle de agente, sin frameworks.

Un agente es un bucle: el modelo decide si llama a una herramienta; si lo hace,
el programa la ejecuta y le devuelve el resultado; el bucle sigue hasta que el
modelo responde sin pedir herramientas o se alcanza el máximo de pasos.

    python sesion_07_indexacion_agentes/ejercicios/s07_ej3_bucle_agente.py
"""

from __future__ import annotations

import ast
import json
import operator
import sys
from datetime import date
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402

_OPERADORES = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
               ast.Pow: operator.pow, ast.USub: operator.neg, ast.Mod: operator.mod}


def calcular(expresion: str) -> float:
    """Evalúa una expresión aritmética de forma SEGURA (sin ``eval``): solo números, + - * / ** %,
    signo negativo y paréntesis. Lanza ``ValueError`` con cualquier otra cosa."""
    raise NotImplementedError("Completa este bloque")


def esquema(nombre: str, descripcion: str, propiedades: dict[str, dict], requeridas: list[str]) -> dict:
    """Definición de herramienta en el formato de la API de OpenAI:
    ``{"type": "function", "function": {"name", "description", "parameters": {"type": "object",
    "properties", "required"}}}``."""
    raise NotImplementedError("Completa este bloque")


def ejecutar_herramienta(nombre: str, argumentos_json: str, registro: dict[str, Callable[..., Any]]) -> str:
    """Ejecuta la herramienta y devuelve su resultado como texto (``json.dumps`` si no es str).

    Nunca lanza excepciones: si la herramienta no existe, los argumentos no son JSON o la función
    falla, devuelve un texto que empieza por ``ERROR:`` para que el modelo pueda reaccionar.
    """
    raise NotImplementedError("Completa este bloque")


def bucle(objetivo: str, registro: dict[str, Callable[..., Any]], herramientas: list[dict],
          sistema: str | None = None, max_pasos: int = 5) -> dict:
    """Ejecuta el bucle del agente.

    En cada paso llama a ``llm.chat_completo(mensajes, herramientas=herramientas, temperatura=0)``.
    Si el mensaje trae ``tool_calls``: añade el mensaje del asistente (``mensaje.model_dump(exclude_none=True)``),
    ejecuta cada llamada y añade ``{"role": "tool", "tool_call_id": id, "content": resultado}``, y registra
    ``{"herramienta", "argumentos", "resultado"}`` en ``pasos``. Si no trae, termina con su contenido.

    Devuelve ``{"respuesta": texto, "pasos": [...], "terminado": bool}``. Si se agotan los pasos,
    ``terminado`` es False y la respuesta es «No he podido completar la tarea en el número máximo de pasos».
    """
    raise NotImplementedError("Completa este bloque")


# ------------------------------------------------------------------ herramientas de ejemplo
def buscar_documentacion(consulta: str) -> str:
    """Busca en la documentación de Atlántica y devuelve los 3 fragmentos más relevantes."""
    from comun.buscador import BuscadorSemantico, contexto_numerado

    global _BUSCADOR
    if "_BUSCADOR" not in globals():
        _BUSCADOR = BuscadorSemantico.de_documentos()
    return contexto_numerado(_BUSCADOR.buscar(consulta, 3))


REGISTRO = {"buscar_documentacion": buscar_documentacion, "calcular": calcular,
            "fecha_de_hoy": lambda: date.today().isoformat()}


def herramientas_de_ejemplo() -> list[dict]:
    """Esquemas de las tres herramientas de ejemplo (usan tu función ``esquema``)."""
    return [
        esquema("buscar_documentacion", "Busca en la documentación interna de Atlántica Logística (políticas, guías, procedimientos).",
                {"consulta": {"type": "string", "description": "Qué buscar"}}, ["consulta"]),
        esquema("calcular", "Calcula una expresión aritmética. Úsala siempre para hacer cuentas.",
                {"expresion": {"type": "string", "description": "Por ejemplo: (2 * 36 + 70) * 1.1"}}, ["expresion"]),
        esquema("fecha_de_hoy", "Devuelve la fecha de hoy en formato AAAA-MM-DD.", {}, []),
    ]


SISTEMA = ("Eres un asistente de Atlántica Logística. Usa buscar_documentacion para cualquier dato de la empresa "
           "y calcular para cualquier operación aritmética. Responde en español citando el documento.")


if __name__ == "__main__":
    for objetivo in ["¿Cuántos días de vacaciones tengo y cuántos me quedan si ya he gastado 9?",
                     "¿Cuánto cuestan al mes dos máquinas m6i.large y una base de datos db.t3.medium según el catálogo?"]:
        resultado = bucle(objetivo, REGISTRO, herramientas_de_ejemplo(), sistema=SISTEMA, max_pasos=6)
        print(f"\n### {objetivo}")
        for paso in resultado["pasos"]:
            print(f"  → {paso['herramienta']}({paso['argumentos']}) = {paso['resultado'][:80]!r}")
        print(resultado["respuesta"])
