"""Acceso a la API nativa de Ollama.

La API compatible con OpenAI es la que usa todo el curso. La nativa (``/api/...``)
se usa solo en los experimentos de la sesión 3 porque permite lo que la otra no:

- fijar la ventana de contexto (``num_ctx``) y otros parámetros del motor;
- leer el número exacto de tokens que el modelo ha procesado;
- ver qué modelos están cargados en memoria y cuánto ocupan.
"""

from __future__ import annotations

from typing import Any

import httpx

from comun import llm


def url_nativa() -> str:
    """URL base de Ollama sin el sufijo ``/v1``."""
    base = llm.URL_BASE.rstrip("/")
    return base[:-3] if base.endswith("/v1") else base


def chat_nativo(
    mensajes: list[dict[str, Any]] | str,
    modelo: str | None = None,
    opciones: dict[str, Any] | None = None,
    pensar: bool | None = None,
    tiempo_maximo: float = 300,
) -> dict[str, Any]:
    """Llama a ``/api/chat`` sin streaming y devuelve la respuesta JSON completa.

    Campos útiles de la respuesta: ``message.content``, ``prompt_eval_count``
    (tokens de entrada), ``eval_count`` (tokens generados) y las duraciones en
    nanosegundos (``total_duration``, ``prompt_eval_duration``, ``eval_duration``).
    """
    cuerpo: dict[str, Any] = {
        "model": modelo or llm.MODELO_CHAT,
        "messages": llm.como_mensajes(mensajes),
        "stream": False,
        "options": opciones or {},
    }
    if pensar is not None:
        cuerpo["think"] = pensar
    respuesta = httpx.post(f"{url_nativa()}/api/chat", json=cuerpo, timeout=tiempo_maximo)
    respuesta.raise_for_status()
    return respuesta.json()


def tokens_por_segundo(respuesta: dict[str, Any]) -> float:
    """Velocidad de generación a partir de una respuesta de ``chat_nativo``."""
    duracion = respuesta.get("eval_duration") or 0
    return respuesta.get("eval_count", 0) / (duracion / 1e9) if duracion else 0.0


def modelos_cargados() -> list[dict[str, Any]]:
    """Modelos cargados ahora en memoria (``/api/ps``): nombre, tamaño, contexto."""
    respuesta = httpx.get(f"{url_nativa()}/api/ps", timeout=10)
    respuesta.raise_for_status()
    return respuesta.json().get("models", [])
