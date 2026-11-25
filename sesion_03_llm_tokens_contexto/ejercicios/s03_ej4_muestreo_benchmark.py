"""Sesión 3 - Ejercicio 4: muestreo y benchmark local frente a servidor.

    python sesion_03_llm_tokens_contexto/ejercicios/s03_ej4_muestreo_benchmark.py
"""

from __future__ import annotations

import os
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402


def generar_varias(prompt: str, temperatura: float, n: int) -> list[str]:
    """Genera ``n`` respuestas al mismo prompt con la temperatura indicada (máximo 30 tokens cada una)."""
    raise NotImplementedError("Completa este bloque")


def diversidad(respuestas: list[str]) -> float:
    """Proporción de respuestas distintas (sin distinguir mayúsculas ni espacios de los extremos).
    Con 2 decimales; 0.0 si la lista está vacía."""
    raise NotImplementedError("Completa este bloque")


def experimento_temperatura(prompt: str, temperaturas: list[float], n: int = 5) -> dict[float, float]:
    """Diversidad para cada temperatura."""
    raise NotImplementedError("Completa este bloque")


def resumen(muestras: list[float]) -> dict[str, float]:
    """``{"media", "minimo", "maximo"}`` de una lista de velocidades, con 1 decimal. Lista vacía: todo 0.0."""
    raise NotImplementedError("Completa este bloque")


def benchmark(url: str, clave: str, modelo: str, prompt: str, repeticiones: int = 3) -> dict[str, float]:
    """Tokens por segundo de un servidor compatible con OpenAI. La primera llamada (calentamiento) no cuenta."""
    from openai import OpenAI

    cliente = OpenAI(base_url=url, api_key=clave, timeout=300)
    muestras = []
    for i in range(repeticiones + 1):
        inicio = time.perf_counter()
        r = cliente.chat.completions.create(model=modelo, messages=[{"role": "user", "content": prompt}],
                                            max_tokens=200, temperature=0)
        segundos = time.perf_counter() - inicio
        if i > 0 and r.usage and segundos:
            muestras.append(r.usage.completion_tokens / segundos)
    return resumen(muestras)


if __name__ == "__main__":
    print(experimento_temperatura("Propón un nombre para un asistente logístico. Solo el nombre.", [0.0, 0.7, 1.5]))
    prompt = "Explica en 150 palabras qué es la gestión de almacenes."
    print("Local:", benchmark(llm.URL_BASE, llm.CLAVE_API, llm.MODELO_CHAT, prompt))
    servidor = os.getenv("SERVIDOR_CURSO_URL")
    if servidor:
        print("Servidor:", benchmark(servidor, os.getenv("SERVIDOR_CURSO_CLAVE", "ollama"),
                                     os.getenv("SERVIDOR_CURSO_MODELO", "qwen3:14b"), prompt))
    else:
        print("Define SERVIDOR_CURSO_URL (y SERVIDOR_CURSO_CLAVE, SERVIDOR_CURSO_MODELO) en .env para medir el servidor.")
