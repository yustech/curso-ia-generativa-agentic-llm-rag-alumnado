"""Sesión 4 - Ejercicio 2: plantilla de prompt estructurado."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PlantillaPrompt:
    """Prompt de sistema organizado por secciones, con ejemplos few-shot opcionales."""

    rol: str
    objetivo: str
    contexto: str = ""
    instrucciones: list[str] = field(default_factory=list)
    formato: str = ""
    restricciones: list[str] = field(default_factory=list)
    ejemplos: list[tuple[str, str]] = field(default_factory=list)
    version: str = "v1"

    def sistema(self) -> str:
        """Mensaje de sistema con las secciones no vacías, en este orden y con estos títulos:

        ``# Rol``, ``# Objetivo``, ``# Contexto``, ``# Instrucciones``, ``# Formato de salida``, ``# Restricciones``.

        Cada título va en su línea, seguido del contenido. Las instrucciones se numeran
        («1. …», «2. …») y las restricciones van como viñetas («- …»). Las secciones se
        separan con una línea en blanco.
        """
        raise NotImplementedError("Completa este bloque")

    def mensajes(self, entrada: str) -> list[dict[str, Any]]:
        """Lista de mensajes: el de sistema, después un par ``user``/``assistant`` por ejemplo y,
        al final, la entrada del usuario envuelta en ``<entrada>`` y ``</entrada>`` (en líneas propias)."""
        raise NotImplementedError("Completa este bloque")

    def huella(self) -> str:
        """Primeros 8 caracteres del SHA-256 del mensaje de sistema más los ejemplos.
        Sirve para saber con qué versión exacta del prompt se obtuvo un resultado."""
        raise NotImplementedError("Completa este bloque")


def plantilla_infrapilot() -> PlantillaPrompt:
    """Ejemplo completo para el reto R2."""
    return PlantillaPrompt(
        rol="Eres InfraPilot, el asistente de infraestructura de Atlántica Logística.",
        objetivo="Convertir peticiones de entornos en propuestas conformes a la política de infraestructura en la nube.",
        contexto="Región principal eu-south-2. Entornos dev, pre y pro. Etiquetas obligatorias: proyecto, entorno, "
                 "centro_coste y responsable. Buckets siempre privados.",
        instrucciones=["Identifica proyecto, entorno, recursos y centro de coste.",
                       "Si falta información imprescindible, pide aclaración y no propongas nada.",
                       "Comprueba cada recurso contra la política antes de proponerlo."],
        formato="JSON con los campos conforme (bool), modulos (lista), motivo (texto) y preguntas (lista).",
        restricciones=["Nunca propongas recursos públicos ni regiones fuera de la UE.", "Nunca apliques cambios."],
        ejemplos=[("Un bucket público para faro en pro.",
                   '{"conforme": false, "modulos": [], "motivo": "La política prohíbe buckets públicos.", "preguntas": []}')],
    )


if __name__ == "__main__":
    plantilla = plantilla_infrapilot()
    print(plantilla.sistema())
    print("\nHuella:", plantilla.huella())
