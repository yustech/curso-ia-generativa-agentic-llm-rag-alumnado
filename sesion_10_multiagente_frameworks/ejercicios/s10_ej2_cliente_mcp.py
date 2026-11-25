"""Sesión 10 - Ejercicio 2: cliente MCP y agente que usa las herramientas del servidor.

    python sesion_10_multiagente_frameworks/ejercicios/s10_ej2_cliente_mcp.py
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402

SERVIDOR = Path(__file__).with_name("s10_ej1_servidor_mcp.py")


def parametros_servidor(ruta: Path | str = SERVIDOR) -> StdioServerParameters:
    """Parámetros para lanzar el servidor con el mismo intérprete de Python."""
    return StdioServerParameters(command=sys.executable, args=[str(ruta)])


def mcp_a_openai(herramienta: Any) -> dict:
    """Convierte una herramienta MCP (``name``, ``description``, ``input_schema``) al formato de herramienta
    de la API de OpenAI. Al esquema se le quita la clave ``title`` (también la de cada propiedad)."""
    raise NotImplementedError("Completa este bloque")


def texto_resultado(resultado: Any) -> str:
    """Texto de un ``CallToolResult``: los ``text`` de su ``content`` unidos con saltos de línea.
    Si ``is_error`` es verdadero, el texto empieza por «ERROR: »."""
    raise NotImplementedError("Completa este bloque")


async def listar_herramientas(ruta: Path | str = SERVIDOR) -> list[str]:
    """Nombres de las herramientas que ofrece el servidor."""
    async with stdio_client(parametros_servidor(ruta)) as (lectura, escritura):
        async with ClientSession(lectura, escritura) as sesion:
            await sesion.initialize()
            return [h.name for h in (await sesion.list_tools()).tools]


async def agente_mcp(objetivo: str, ruta: Path | str = SERVIDOR, max_pasos: int = 5, sistema: str | None = None) -> dict:
    """Bucle de agente cuyas herramientas son las del servidor MCP.

    Abre la sesión, convierte las herramientas con ``mcp_a_openai`` y ejecuta el bucle: cada ``tool_call``
    se resuelve con ``await sesion.call_tool(nombre, argumentos)`` y ``texto_resultado``.
    Devuelve ``{"respuesta", "pasos": [{"herramienta", "argumentos", "resultado"}], "terminado"}``.
    """
    raise NotImplementedError("Completa este bloque")


if __name__ == "__main__":
    print("Herramientas del servidor:", asyncio.run(listar_herramientas()))
    resultado = asyncio.run(agente_mcp(
        "¿Qué documento regula los cambios en producción y cuál es su ventana de cambios?",
        sistema="Eres un asistente de Atlántica. Usa las herramientas para consultar la documentación y cita el documento."))
    for paso in resultado["pasos"]:
        print(f"  → {paso['herramienta']}({paso['argumentos']})")
    print(resultado["respuesta"])
