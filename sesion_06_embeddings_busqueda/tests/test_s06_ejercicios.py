"""Tests de los ejercicios de la sesión 6."""

import numpy as np
import pytest

import s06_ej1_similitud as ej1
import s06_ej2_busqueda as ej2
import s06_ej3_metricas as ej3
import s06_ej4_chroma as ej4
from comun.documentos import Trozo


def trozo(i, texto, documento="doc.md"):
    return Trozo(f"t{i}", documento, f"S{i}", texto)


TROZOS = [
    trozo(0, "Vacaciones: veinticinco días laborables. Se solicitan en el portal Ancla.", "vacaciones.md"),
    trozo(1, "Etiquetas obligatorias: proyecto, entorno, centro_coste y responsable. Código ATL-INF-006.", "nube.md"),
    trozo(2, "El Comité de Cambios (CAB) se reúne los jueves a las 10:00.", "cambios.md"),
    trozo(3, "Tipos de instancia permitidos: t3.micro, t3.medium y m6i.large.", "nube.md"),
]


# ---------------------------------------------------------------- Ejercicio 1
def test_ej1_normalizar():
    assert np.allclose(ej1.normalizar([3, 4]), [0.6, 0.8])
    assert np.allclose(ej1.normalizar([0, 0]), [0, 0])


def test_ej1_coseno_y_euclidea():
    assert ej1.coseno([1, 0], [2, 0]) == pytest.approx(1.0)
    assert ej1.coseno([1, 0], [0, 0]) == 0.0
    assert ej1.distancia_euclidea([0, 0], [3, 4]) == pytest.approx(5.0)


def test_ej1_matriz_similitud():
    m = ej1.matriz_similitud([[1, 0], [0, 2], [1, 1]])
    assert m.shape == (3, 3)
    assert np.allclose(np.diag(m), 1.0)
    assert m[0, 1] == pytest.approx(0.0) and m[0, 2] == pytest.approx(np.sqrt(0.5))
    assert np.allclose(m, m.T)


def test_ej1_mas_similares():
    resultado = ej1.mas_similares([1, 0], [[0, 1], [2, 0], [1, 1], [5, 0]], k=3)
    assert [i for i, _ in resultado] == [1, 3, 2]
    assert resultado[0][1] == pytest.approx(1.0)


# ---------------------------------------------------------------- Ejercicio 2
def test_ej2_tokenizar():
    assert ej2.tokenizar("¿Qué tipos de instancia, t3.medium o m6i.large?") == ["tipos", "instancia", "t3.medium", "m6i.large"]
    assert ej2.tokenizar("Política de AÑOS y Diseño.") == ["politica", "años", "diseño"]
    assert ej2.tokenizar("FARO-142 ya está revisada.") == ["faro-142", "revisada"]


def test_ej2_bm25_encuentra_codigos_exactos():
    resultados = ej2.BuscadorBM25(TROZOS).buscar("t3.medium", k=2)
    assert resultados[0][0].id == "t3"
    assert resultados[0][1] > resultados[1][1]


def test_ej2_semantico():
    resultados = ej2.BuscadorSemantico(TROZOS).buscar("etiquetas obligatorias proyecto", k=4)
    assert resultados[0][0].id == "t1" and len(resultados) == 4


def test_ej2_fusion_rrf():
    fusion = ej2.fusion_rrf([["a", "b", "c"], ["b", "a", "d"]], k=60)
    ids = [i for i, _ in fusion]
    assert ids == ["a", "b", "c", "d"]
    assert fusion[0][1] == pytest.approx(1 / 61 + 1 / 62)
    assert fusion[2][1] == pytest.approx(1 / 63)


def test_ej2_hibrido():
    hibrido = ej2.BuscadorHibrido(ej2.BuscadorBM25(TROZOS), ej2.BuscadorSemantico(TROZOS), candidatos=4)
    resultados = hibrido.buscar("Comité de Cambios jueves", k=2)
    assert resultados[0][0].id == "t2" and len(resultados) == 2


# ---------------------------------------------------------------- Ejercicio 3
def test_ej3_acierto_y_rango():
    docs = ["a", "b", "c"]
    assert ej3.acierto_en_k(docs, "b", 2) and not ej3.acierto_en_k(docs, "c", 2)
    assert ej3.rango_reciproco(docs, "c") == pytest.approx(1 / 3)
    assert ej3.rango_reciproco(docs, "z") == 0.0
    assert ej3.rango_reciproco(["a", "a"], "a") == 1.0


def test_ej3_cargar_preguntas_descarta_sin_fuente():
    preguntas = ej3.cargar_preguntas()
    assert len(preguntas) == 28 and all(p["fuente"] for p in preguntas)


def test_ej3_evaluar():
    preguntas = [{"id": "Q1", "pregunta": "vacaciones", "fuente": "vacaciones.md"},
                 {"id": "Q2", "pregunta": "cambios", "fuente": "cambios.md"}]
    respuestas = {"vacaciones": [TROZOS[0], TROZOS[1]], "cambios": [TROZOS[1], TROZOS[3]]}
    buscar = lambda pregunta, k: [(t, 0.0) for t in respuestas[pregunta][:k]]  # noqa: E731
    assert ej3.evaluar(buscar, preguntas, k=2) == {"hit@k": 0.5, "mrr": 0.5, "fallos": ["Q2"]}


def test_ej3_tabla():
    texto = ej3.tabla({"BM25": {"hit@k": 0.5, "mrr": 0.25, "fallos": ["Q2"]}, "Híbrida": {"hit@k": 1, "mrr": 1, "fallos": []}}, 3)
    lineas = texto.splitlines()
    assert lineas[0] == "| Estrategia | Hit@3 | MRR | Fallos |"
    assert lineas[2] == "| BM25 | 0.500 | 0.250 | Q2 |" and lineas[3] == "| Híbrida | 1.000 | 1.000 | — |"


# ---------------------------------------------------------------- Ejercicio 4
def test_ej4_indexar_y_consultar(tmp_path):
    coleccion = ej4.crear_coleccion(tmp_path / "chroma", "prueba")
    assert ej4.indexar(coleccion, TROZOS, lote=3) == 4
    assert ej4.indexar(coleccion, TROZOS) == 4  # upsert: no duplica
    resultados = ej4.consultar(coleccion, "Comité de Cambios jueves", k=2)
    assert resultados[0]["id"] == "t2" and resultados[0]["documento"] == "cambios.md"
    assert set(resultados[0]) == {"id", "documento", "seccion", "similitud", "texto"}
    assert 0 < resultados[0]["similitud"] <= 1


def test_ej4_filtro_por_documento(tmp_path):
    coleccion = ej4.crear_coleccion(tmp_path / "chroma", "filtro")
    ej4.indexar(coleccion, TROZOS)
    resultados = ej4.consultar(coleccion, "vacaciones", k=4, documento="nube.md")
    assert {r["documento"] for r in resultados} == {"nube.md"} and len(resultados) == 2
