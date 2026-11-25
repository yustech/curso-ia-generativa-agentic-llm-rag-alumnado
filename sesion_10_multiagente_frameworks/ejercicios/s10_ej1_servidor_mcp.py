"""Sesión 10 - Ejercicio 1: tu propio servidor MCP con la documentación de Atlántica.

Cualquier cliente MCP (tu agente, un IDE, un asistente de escritorio) podrá usar
estas herramientas sin saber nada de cómo están programadas.

Se arranca lo lanza el cliente (transporte stdio). Para probarlo a mano:
    python sesion_10_multiagente_frameworks/ejercicios/s10_ej2_cliente_mcp.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from mcp.server import MCPServer

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun.documentos import CARPETA_DOCUMENTOS, leer_front_matter  # noqa: E402

servidor = MCPServer("atlantica-documentacion", instructions="Documentación interna de Atlántica Logística (ficticia).")


def listar_documentos() -> list[dict]:
    """Lista los documentos internos de Atlántica con su nombre de fichero, título y código."""
    raise NotImplementedError("Completa este bloque")


def leer_documento(nombre: str) -> str:
    """Devuelve el texto completo de un documento por su nombre de fichero (por ejemplo, 06_politica_infraestructura_cloud.md).

    Solo permite leer ficheros de la carpeta de documentos: un nombre con rutas («../», «/») lanza ``PermissionError``;
    un documento inexistente, ``FileNotFoundError``.
    """
    raise NotImplementedError("Completa este bloque")


def buscar_documentacion(consulta: str, k: int = 3) -> str:
    """Busca en la documentación interna de Atlántica y devuelve los k fragmentos más relevantes, numerados y con su origen."""
    raise NotImplementedError("Completa este bloque")


def indice() -> str:
    """Índice de documentos en Markdown (una línea por documento: «- código · título (nombre)»)."""
    raise NotImplementedError("Completa este bloque")


# Registro en el servidor: las funciones siguen siendo funciones normales (los tests las llaman directamente).
servidor.tool()(listar_documentos)
servidor.tool()(leer_documento)
servidor.tool()(buscar_documentacion)
servidor.resource("atlantica://indice", mime_type="text/markdown")(indice)


if __name__ == "__main__":
    servidor.run()  # transporte stdio
