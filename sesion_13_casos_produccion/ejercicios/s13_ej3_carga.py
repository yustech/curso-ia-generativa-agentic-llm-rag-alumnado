"""Sesión 13 - Ejercicio 3: prueba de carga de un servidor de inferencia (Ollama frente a vLLM).

    python sesion_13_casos_produccion/ejercicios/s13_ej3_carga.py --usuarios 1 4 8
    python sesion_13_casos_produccion/ejercicios/s13_ej3_carga.py --url http://servidor:8000/v1 --modelo <modelo vLLM>
"""

from __future__ import annotations

import argparse
import asyncio
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402
from s13_ej1_evaluacion_e2e import percentil  # noqa: E402

PROMPT = "Explica en unas 120 palabras qué es la gestión de almacenes en una empresa logística."


async def una_peticion(cliente, modelo: str, prompt: str, max_tokens: int = 200) -> dict:
    """Una petición asíncrona. Devuelve ``{"ok", "segundos", "tokens"}``; si falla, ``ok`` False y tokens 0."""
    raise NotImplementedError("Completa este bloque")


async def prueba_carga(cliente, modelo: str, usuarios: int, peticiones_por_usuario: int, prompt: str = PROMPT) -> dict:
    """Lanza ``usuarios`` tareas concurrentes que hacen ``peticiones_por_usuario`` peticiones seguidas cada una.
    Devuelve ``resumen(resultados, duración total)`` más la clave ``"usuarios"``."""
    raise NotImplementedError("Completa este bloque")


def resumen(resultados: list[dict], duracion: float) -> dict:
    """``{"peticiones", "errores", "latencia_p50", "latencia_p95", "tokens_por_segundo", "peticiones_por_segundo"}``.

    Latencias solo de las peticiones correctas (percentil del ejercicio 1). El rendimiento es el total de
    tokens (o de peticiones correctas) dividido por la duración, con 1 decimal (2 para peticiones/s).
    """
    raise NotImplementedError("Completa este bloque")


def tabla(filas: list[dict]) -> str:
    lineas = ["| Usuarios | Peticiones | Errores | p50 (s) | p95 (s) | Tokens/s | Peticiones/s |", "| --- | --- | --- | --- | --- | --- | --- |"]
    lineas += [f"| {f['usuarios']} | {f['peticiones']} | {f['errores']} | {f['latencia_p50']} | {f['latencia_p95']} | "
               f"{f['tokens_por_segundo']} | {f['peticiones_por_segundo']} |" for f in filas]
    return "\n".join(lineas)


async def main() -> None:
    from openai import AsyncOpenAI

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=llm.URL_BASE)
    parser.add_argument("--clave", default=llm.CLAVE_API)
    parser.add_argument("--modelo", default=llm.MODELO_CHAT)
    parser.add_argument("--usuarios", type=int, nargs="+", default=[1, 2, 4])
    parser.add_argument("--peticiones", type=int, default=2)
    args = parser.parse_args()
    cliente = AsyncOpenAI(base_url=args.url, api_key=args.clave, timeout=600)
    await una_peticion(cliente, args.modelo, "Hola", 5)  # calentamiento
    filas = [await prueba_carga(cliente, args.modelo, u, args.peticiones) for u in args.usuarios]
    print(f"Servidor {args.url} · modelo {args.modelo}\n\n{tabla(filas)}")


if __name__ == "__main__":
    asyncio.run(main())
