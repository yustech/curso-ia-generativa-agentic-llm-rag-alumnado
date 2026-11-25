"""Sesión 6 - Ejercicio 1: medidas de similitud."""

from __future__ import annotations

import numpy as np


def normalizar(v) -> np.ndarray:
    """Vector dividido por su norma. Un vector de norma 0 se devuelve sin cambios (como array de float)."""
    raise NotImplementedError("Completa este bloque")


def coseno(a, b) -> float:
    """Similitud coseno. 0.0 si alguno de los vectores tiene norma 0."""
    raise NotImplementedError("Completa este bloque")


def distancia_euclidea(a, b) -> float:
    """Distancia euclídea entre dos vectores."""
    raise NotImplementedError("Completa este bloque")


def matriz_similitud(vectores) -> np.ndarray:
    """Matriz n × n de similitudes coseno, calculada con una multiplicación de matrices (sin bucles)."""
    raise NotImplementedError("Completa este bloque")


def mas_similares(consulta, vectores, k: int = 3) -> list[tuple[int, float]]:
    """Índices de los ``k`` vectores más similares a la consulta con su similitud coseno,
    de mayor a menor. A igual similitud, el índice menor primero."""
    raise NotImplementedError("Completa este bloque")
