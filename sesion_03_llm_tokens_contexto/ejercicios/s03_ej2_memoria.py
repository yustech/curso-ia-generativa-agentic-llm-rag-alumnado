"""Sesión 3 - Ejercicio 2: ¿cabe este modelo en mi portátil?"""

from __future__ import annotations

GIB = 1024 ** 3

# Bits efectivos por parámetro de los formatos más comunes de GGUF.
BITS_FORMATO = {"F16": 16.0, "Q8_0": 8.5, "Q6_K": 6.6, "Q5_K_M": 5.7, "Q4_K_M": 4.8, "Q3_K_M": 3.9, "Q2_K": 3.0}


def memoria_pesos_gb(miles_de_millones: float, bits: float) -> float:
    """Memoria de los pesos en GiB: parámetros × bits / 8. Redondeada a 2 decimales."""
    raise NotImplementedError("Completa este bloque")


def memoria_kv_gb(capas: int, cabezas_kv: int, dim_cabeza: int, contexto: int, bytes_por_valor: int = 2) -> float:
    """Memoria de la caché KV en GiB: 2 (claves y valores) × capas × cabezas_kv × dim_cabeza × contexto × bytes.
    Redondeada a 2 decimales."""
    raise NotImplementedError("Completa este bloque")


def memoria_total_gb(miles_de_millones: float, formato: str, capas: int, cabezas_kv: int, dim_cabeza: int,
                     contexto: int, margen: float = 0.10) -> float:
    """Pesos (según ``BITS_FORMATO[formato]``) más caché KV, más un margen (10 % por defecto). 2 decimales.

    Lanza ``ValueError`` si el formato no está en ``BITS_FORMATO``.
    """
    raise NotImplementedError("Completa este bloque")


def cabe(memoria_necesaria_gb: float, ram_gb: float = 16, reservada_gb: float = 7) -> bool:
    """True si el modelo cabe en la RAM libre (RAM total menos lo que usan sistema, IDE y navegador)."""
    raise NotImplementedError("Completa este bloque")


def contexto_maximo(miles_de_millones: float, formato: str, capas: int, cabezas_kv: int, dim_cabeza: int,
                    ram_gb: float = 16, reservada_gb: float = 7) -> int:
    """Mayor contexto, en múltiplos de 1.024 tokens, que cabe en la memoria libre. 0 si ni siquiera caben los pesos."""
    raise NotImplementedError("Completa este bloque")


if __name__ == "__main__":
    # Arquitectura aproximada de un modelo de 8B con atención agrupada (32 capas, 8 cabezas KV de 128).
    for formato in ("F16", "Q8_0", "Q4_K_M"):
        total = memoria_total_gb(8, formato, 32, 8, 128, 8192)
        print(f"8B en {formato:6} con 8K de contexto: {total:5.2f} GB · ¿cabe en 16 GB? {cabe(total)}")
    print("Contexto máximo de un 8B Q4_K_M en un portátil de 16 GB:",
          contexto_maximo(8, "Q4_K_M", 32, 8, 128), "tokens")
