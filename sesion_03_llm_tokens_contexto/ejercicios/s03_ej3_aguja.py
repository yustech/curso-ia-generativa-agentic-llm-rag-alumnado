"""Sesión 3 - Ejercicio 3: la aguja en el pajar (ventana de contexto).

Se esconde un dato (la aguja) dentro de un texto largo de relleno (el pajar) y se
pregunta por él. Variando la longitud del pajar, la posición de la aguja y
``num_ctx`` se observa cuándo el modelo deja de encontrarla.

    python sesion_03_llm_tokens_contexto/ejercicios/s03_ej3_aguja.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import ollama  # noqa: E402

AGUJA = "Dato importante: el código de acceso del almacén de Bilbao es 7342."
PREGUNTA = "¿Cuál es el código de acceso del almacén de Bilbao? Responde solo con el número."
VALOR = "7342"
FRASES = [
    "El centro de Zaragoza es el hub de distribución nacional de Atlántica.",
    "Los camiones frigoríficos se revisan cada 15.000 kilómetros.",
    "La campaña de Navidad concentra el 30 % de los envíos del año.",
    "El portal de clientes muestra la posición de los camiones cada dos minutos.",
    "Los palés retornables se recogen en la siguiente entrega a la tienda.",
    "El equipo de Faro despliega en producción los martes y jueves por la noche.",
    "Las tiendas reciben un aviso cuando el camión está a treinta minutos.",
    "La flota propia tiene 420 camiones, 18 de ellos eléctricos.",
]


def construir_pajar(n_frases: int, aguja: str, posicion: float) -> str:
    """Texto de ``n_frases`` frases de relleno (tomadas de ``FRASES`` en orden, repitiendo)
    con la ``aguja`` insertada en la posición relativa ``posicion`` (0 = principio, 1 = final).

    La aguja se inserta antes de la frase de índice ``round(posicion * n_frases)``.
    Las frases se separan con un espacio. Lanza ``ValueError`` si ``posicion`` no está entre 0 y 1.
    """
    raise NotImplementedError("Completa este bloque")


def encontrada(respuesta: str, valor: str = VALOR) -> bool:
    """True si el valor aparece en la respuesta (ignorando espacios y puntos de miles)."""
    raise NotImplementedError("Completa este bloque")


def prueba(n_frases: int, posicion: float, num_ctx: int, modelo: str | None = None) -> dict:
    """Ejecuta una prueba con la API nativa de Ollama y devuelve
    ``{"frases", "posicion", "num_ctx", "tokens_entrada", "encontrada", "segundos", "respuesta"}``."""
    texto = construir_pajar(n_frases, AGUJA, posicion)
    inicio = time.perf_counter()
    r = ollama.chat_nativo(f"{texto}\n\n{PREGUNTA}", modelo=modelo,
                           opciones={"num_ctx": num_ctx, "temperature": 0, "num_predict": 20})
    respuesta = r["message"]["content"]
    return {"frases": n_frases, "posicion": posicion, "num_ctx": num_ctx, "tokens_entrada": r.get("prompt_eval_count"),
            "encontrada": encontrada(respuesta), "segundos": round(time.perf_counter() - inicio, 1), "respuesta": respuesta.strip()}


def tabla(resultados: list[dict]) -> str:
    """Tabla Markdown: | Frases | Posición | num_ctx | Tokens | ¿Encontrada? | Segundos |  («sí»/«no»)."""
    raise NotImplementedError("Completa este bloque")


if __name__ == "__main__":
    resultados = []
    for n_frases in (50, 400):
        for posicion in (0.0, 0.5, 1.0):
            for num_ctx in (2048, 8192):
                resultados.append(prueba(n_frases, posicion, num_ctx))
                print(resultados[-1])
    print("\n" + tabla(resultados))
