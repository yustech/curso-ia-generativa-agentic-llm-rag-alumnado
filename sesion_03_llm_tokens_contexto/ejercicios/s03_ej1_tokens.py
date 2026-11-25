"""Sesión 3 - Ejercicio 1: tokens y coste."""

from __future__ import annotations

import tiktoken

CODIFICACION = "o200k_base"


def _codificador(nombre: str = CODIFICACION):
    return tiktoken.get_encoding(nombre)


def contar_tokens(texto: str, codificacion: str = CODIFICACION) -> int:
    """Número de tokens del texto con la codificación indicada."""
    raise NotImplementedError("Completa este bloque")


def trozos(texto: str, codificacion: str = CODIFICACION) -> list[str]:
    """Lista de tokens como texto (cada id decodificado por separado)."""
    raise NotImplementedError("Completa este bloque")


def tokens_por_palabra(texto: str) -> float:
    """Tokens divididos entre palabras (separadas por espacios), con 2 decimales. 0.0 si no hay palabras."""
    raise NotImplementedError("Completa este bloque")


def estimar_coste(tokens_entrada: int, tokens_salida: int, precio_entrada: float, precio_salida: float) -> float:
    """Coste en euros con precios por millón de tokens, redondeado a 4 decimales."""
    raise NotImplementedError("Completa este bloque")


def coste_mensual(peticiones_dia: int, tokens_entrada: int, tokens_salida: int,
                  precio_entrada: float, precio_salida: float, dias: int = 22) -> float:
    """Coste de un mes de uso (por defecto 22 días laborables), redondeado a 2 decimales."""
    raise NotImplementedError("Completa este bloque")


def comparar_textos(textos: dict[str, str]) -> list[dict]:
    """Para cada texto devuelve ``{"nombre", "palabras", "tokens", "tokens_por_palabra"}``, en el mismo orden."""
    raise NotImplementedError("Completa este bloque")


if __name__ == "__main__":
    filas = comparar_textos({
        "español": "La logística inversa recupera los palés vacíos de las tiendas.",
        "inglés": "Reverse logistics recovers empty pallets from the stores.",
    })
    for fila in filas:
        print(fila)
    # Asistente con 2.000 tokens de entrada y 400 de salida, 300 peticiones al día,
    # a 0,40 € y 1,60 € por millón (precios orientativos de un modelo comercial pequeño):
    print("Coste mensual estimado:", coste_mensual(300, 2000, 400, 0.40, 1.60), "€")
