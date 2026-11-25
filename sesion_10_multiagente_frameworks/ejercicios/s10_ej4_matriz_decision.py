"""Sesión 10 - Ejercicio 4: matriz de decisión tecnológica ponderada."""

from __future__ import annotations

from dataclasses import dataclass

CRITERIOS = {
    "simplicidad": "Menos piezas y dependencias",
    "control": "Control fino del flujo y del prompt",
    "depuracion": "Facilidad para trazar y depurar",
    "rag": "Soporte para ingesta y recuperación",
    "multiagente": "Soporte para flujos con estado y varios agentes",
    "ecosistema": "Integraciones, documentación y comunidad",
    "estabilidad": "Estabilidad de la API entre versiones",
}


@dataclass
class Opcion:
    nombre: str
    puntuaciones: dict[str, int]  # criterio → 1 a 5


def normalizar_pesos(pesos: dict[str, float]) -> dict[str, float]:
    """Pesos divididos por su suma (redondeados a 4 decimales). ``ValueError`` si algún peso es negativo o la suma es 0."""
    raise NotImplementedError("Completa este bloque")


def puntuar(opcion: Opcion, pesos: dict[str, float]) -> float:
    """Suma ponderada (pesos normalizados) de las puntuaciones, con 2 decimales.
    ``ValueError`` si falta la puntuación de algún criterio con peso o alguna está fuera de 1-5."""
    raise NotImplementedError("Completa este bloque")


def ranking(opciones: list[Opcion], pesos: dict[str, float]) -> list[tuple[str, float]]:
    """``(nombre, puntuación)`` de mayor a menor; a igual puntuación, por nombre."""
    raise NotImplementedError("Completa este bloque")


def tabla(opciones: list[Opcion], pesos: dict[str, float]) -> str:
    """Tabla Markdown: cabecera «| Criterio | Peso | <opción 1> | ... |», una fila por criterio con peso
    (peso normalizado con 2 decimales) y una última fila «| **Total** | 1.00 | <puntuaciones> |»."""
    raise NotImplementedError("Completa este bloque")


OPCIONES_EJEMPLO = [
    Opcion("Sin framework", {"simplicidad": 5, "control": 5, "depuracion": 4, "rag": 2, "multiagente": 2, "ecosistema": 2, "estabilidad": 5}),
    Opcion("LangGraph", {"simplicidad": 3, "control": 4, "depuracion": 4, "rag": 3, "multiagente": 5, "ecosistema": 5, "estabilidad": 3}),
    Opcion("LlamaIndex", {"simplicidad": 3, "control": 3, "depuracion": 3, "rag": 5, "multiagente": 3, "ecosistema": 4, "estabilidad": 3}),
]

if __name__ == "__main__":
    pesos = {"simplicidad": 2, "control": 2, "depuracion": 2, "rag": 3, "multiagente": 1, "ecosistema": 1, "estabilidad": 1}
    print(tabla(OPCIONES_EJEMPLO, pesos))
    print("\nRanking:", ranking(OPCIONES_EJEMPLO, pesos))
