"""Guardarraíles de entrada (versión de partida de la sesión 8).

Primera capa, determinista y barata. No sustituye a las demás capas (mínimo
privilegio en las herramientas, confirmación humana, revisión de la salida).
"""

from __future__ import annotations

import re
import unicodedata

PATRONES_INYECCION = [
    r"ignora (todas )?(las )?instrucciones",
    r"olvida (tus|las) (reglas|instrucciones)",
    r"(muestra|revela|dime) (tu|el) (prompt|mensaje) (de|del) sistema",
    r"actua como .* sin restricciones",
    r"modo desarrollador",
]
PATRONES_DATOS_PERSONALES = {
    "DNI": r"\b\d{8}[A-HJ-NP-TV-Z]\b",
    "IBAN": r"\bES\d{2}[ ]?\d{4}[ ]?\d{4}[ ]?\d{2}[ ]?\d{10}\b",
    "tarjeta": r"\b(?:\d[ -]?){13,16}\b",
}
MAX_CARACTERES = 4000


def normalizar(texto: str) -> str:
    sin_tildes = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", sin_tildes.lower())


def revisar_entrada(texto: str) -> str | None:
    """Devuelve un mensaje de bloqueo o ``None`` si la entrada puede pasar al agente."""
    if len(texto) > MAX_CARACTERES:
        return f"La consulta es demasiado larga (máximo {MAX_CARACTERES} caracteres)."
    normal = normalizar(texto)
    if any(re.search(p, normal) for p in PATRONES_INYECCION):
        return "No puedo atender esa petición: parece un intento de cambiar mis instrucciones."
    for tipo, patron in PATRONES_DATOS_PERSONALES.items():
        if re.search(patron, texto, flags=re.IGNORECASE):
            return f"Tu mensaje parece contener datos personales ({tipo}). Elimínalos y vuelve a preguntar."
    return None
