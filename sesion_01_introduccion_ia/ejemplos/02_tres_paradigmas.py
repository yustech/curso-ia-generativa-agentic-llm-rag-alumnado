"""Ejemplo 2: el mismo problema resuelto con reglas, con machine learning y con un LLM.

Problema: clasificar incidencias de Atlántica en «transporte», «almacén» o «sistemas».

Ejecuta desde la raíz:
    python sesion_01_introduccion_ia/ejemplos/02_tres_paradigmas.py
"""

import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402

ENTRENAMIENTO = [
    ("El camión 4312 lleva dos horas parado en la AP-9", "transporte"),
    ("Retraso en la ruta Vigo-Valencia por avería del tráiler", "transporte"),
    ("El conductor no puede entregar: muelle cerrado", "transporte"),
    ("Faltan 12 palés en la ubicación B-14 del almacén", "almacén"),
    ("La carretilla del pasillo 3 no arranca", "almacén"),
    ("Error de inventario en la referencia 88213", "almacén"),
    ("Faro no carga la lista de envíos", "sistemas"),
    ("No puedo iniciar sesión en el portal de clientes", "sistemas"),
    ("La impresora de etiquetas da error de red", "sistemas"),
]
PRUEBA = [
    ("El tráiler 2207 ha pinchado cerca de Burgos", "transporte"),
    ("Inventario descuadrado en la zona de congelados", "almacén"),
    ("El portal muestra un error 500 al descargar albaranes", "sistemas"),
    ("La furgoneta de reparto no tiene batería", "transporte"),
]
CATEGORIAS = ["transporte", "almacén", "sistemas"]


# 1. Reglas escritas a mano (IA simbólica)
REGLAS = {
    "transporte": ["camión", "tráiler", "ruta", "conductor", "furgoneta", "pinchado", "avería"],
    "almacén": ["palé", "almacén", "inventario", "carretilla", "ubicación", "congelados"],
    "sistemas": ["faro", "portal", "sesión", "error", "impresora", "red"],
}


def por_reglas(texto: str) -> str:
    texto = texto.lower()
    puntos = {c: sum(p in texto for p in palabras) for c, palabras in REGLAS.items()}
    return max(puntos, key=puntos.get)


# 2. Machine learning: vecino más próximo sobre una bolsa de palabras
def vocabulario(textos):
    return sorted({p for t in textos for p in t.lower().split()})


VOCAB = vocabulario([t for t, _ in ENTRENAMIENTO])


def vectorizar(texto: str) -> np.ndarray:
    palabras = Counter(texto.lower().split())
    return np.array([palabras[p] for p in VOCAB], dtype=float)


X = np.array([vectorizar(t) for t, _ in ENTRENAMIENTO])
Y = [c for _, c in ENTRENAMIENTO]


def por_ml(texto: str) -> str:
    v = vectorizar(texto)
    similitudes = X @ v / (np.linalg.norm(X, axis=1) * (np.linalg.norm(v) or 1))
    return Y[int(np.argmax(similitudes))]


# 3. LLM sin ejemplos (zero-shot)
def por_llm(texto: str) -> str:
    respuesta = llm.chat(
        f"Clasifica esta incidencia en una sola palabra: transporte, almacén o sistemas.\nIncidencia: {texto}",
        temperatura=0,
    ).lower()
    return next((c for c in CATEGORIAS if c in respuesta), respuesta)


if __name__ == "__main__":
    print(f"{'Incidencia':55} {'Real':11} {'Reglas':11} {'ML':11} {'LLM':11}")
    for texto, real in PRUEBA:
        print(f"{texto[:54]:55} {real:11} {por_reglas(texto):11} {por_ml(texto):11} {por_llm(texto):11}")
    print("\nObserva: el ML falla con palabras que no vio al entrenar; el LLM generaliza sin ejemplos,")
    print("pero es más lento y no explica por qué. Las reglas son exactas... mientras no cambie el vocabulario.")
