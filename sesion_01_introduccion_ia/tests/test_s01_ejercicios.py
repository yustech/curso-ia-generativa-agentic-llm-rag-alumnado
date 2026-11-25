"""Tests de los ejercicios de la sesión 1."""

import json

import pytest

import s01_ej1_clasificacion as ej1
import s01_ej2_clasificar_con_llm as ej2
from comun import llm


# ---------------------------------------------------------------- Ejercicio 1
def test_ej1_cargar_casos():
    casos = ej1.cargar_casos()
    assert len(casos) == 8
    assert {"id", "caso"} <= set(casos[0])


def test_ej1_ficha_completa_y_valida():
    assert ej1.validar_ficha(ej1.clasificacion_manual()) == []


@pytest.mark.parametrize("caso, aceptables", [
    ("C1", {"ml_supervisado"}),
    ("C2", {"ia_generativa"}),
    ("C3", {"deep_learning_vision"}),
    ("C4", {"reglas_optimizacion"}),
    ("C5", {"ia_generativa"}),
    ("C6", {"ml_no_supervisado", "ml_supervisado"}),
    ("C7", {"ml_no_supervisado"}),
    ("C8", {"agente"}),
])
def test_ej1_paradigmas_razonables(caso, aceptables):
    assert ej1.clasificacion_manual()[caso]["paradigma"] in aceptables


def test_ej1_validar_detecta_problemas():
    casos = [{"id": "C1", "caso": "x"}, {"id": "C2", "caso": "y"}]
    ficha = {"C1": {"paradigma": "magia", "tipo_modelo": "", "justificacion": "corta"}}
    problemas = ej1.validar_ficha(ficha, casos)
    texto = " ".join(problemas)
    assert "C2" in texto and "falta la clasificación" in texto
    assert "paradigma no válido" in texto
    assert "tipo de modelo" in texto
    assert "demasiado corta" in texto


def test_ej1_resumen_por_paradigma():
    ficha = {"A": {"paradigma": "agente"}, "B": {"paradigma": "agente"}, "C": {"paradigma": "ml_supervisado"}}
    resumen = ej1.resumen_por_paradigma(ficha)
    assert list(resumen) == list(ej1.PARADIGMAS)
    assert resumen["agente"] == 2 and resumen["ml_supervisado"] == 1 and resumen["ia_generativa"] == 0


def test_ej1_a_markdown():
    casos = [{"id": "C1", "caso": "Prever demanda"}]
    ficha = {"C1": {"paradigma": "ml_supervisado", "tipo_modelo": "regresión", "justificacion": "Hay histórico etiquetado."}}
    tabla = ej1.a_markdown(ficha, casos).splitlines()
    assert tabla[0].startswith("| Caso |") and tabla[1].startswith("| ---")
    assert "| C1 | Prever demanda | ml_supervisado | regresión |" in tabla[2]


# ---------------------------------------------------------------- Ejercicio 2
def test_ej2_prompt_incluye_caso_y_paradigmas():
    prompt = ej2.construir_prompt("Leer matrículas con cámaras")
    assert "Leer matrículas con cámaras" in prompt
    for p in ej2.PARADIGMAS:
        assert p in prompt
    assert "JSON" in prompt


def test_ej2_clasificar_devuelve_objeto_validado():
    falso = llm.usar_llm_falso([json.dumps({"paradigma": "deep_learning_vision", "tipo_modelo": "OCR", "justificacion": "Imágenes."})])
    resultado = ej2.clasificar_con_llm("Leer matrículas")
    assert isinstance(resultado, ej2.Clasificacion)
    assert resultado.paradigma == "deep_learning_vision"
    assert "Leer matrículas" in falso.recibidos[0][-1]["content"]


def test_ej2_clasificar_reintenta_si_el_json_no_vale():
    llm.usar_llm_falso(["no es json", json.dumps({"paradigma": "agente", "tipo_modelo": "LLM", "justificacion": "Actúa."})])
    assert ej2.clasificar_con_llm("Caso").paradigma == "agente"


def test_ej2_comparar():
    manual = {"C1": {"paradigma": "a"}, "C2": {"paradigma": "b"}, "C3": {"paradigma": "c"}, "C4": {"paradigma": "d"}}
    auto = {"C1": {"paradigma": "a"}, "C2": {"paradigma": "x"}, "C3": {"paradigma": "c"}}
    assert ej2.comparar(manual, auto) == {"coincidencias": 2, "total": 3, "porcentaje": 66.7, "discrepancias": ["C2"]}


def test_ej2_comparar_vacio():
    assert ej2.comparar({}, {})["porcentaje"] == 0.0
