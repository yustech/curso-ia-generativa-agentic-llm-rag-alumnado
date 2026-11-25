"""Tests de los ejercicios de la sesión 2."""

import pytest
from pydantic import ValidationError

import s02_ej1_matriz_riesgos as ej1
import s02_ej2_primeras_llamadas as ej2
import s02_ej3_comparar_modelos as ej3
from comun import llm


def riesgo(id_, p, i, controles=None):
    return ej1.Riesgo(id=id_, descripcion=f"Riesgo {id_}", categoria="seguridad", probabilidad=p, impacto=i,
                      controles=controles or [])


# ---------------------------------------------------------------- Ejercicio 1
def test_ej1_exposicion():
    assert ej1.exposicion(riesgo("A", 4, 4)) == 16


@pytest.mark.parametrize("valor, esperado", [(1, "bajo"), (6, "bajo"), (7, "medio"), (14, "medio"), (15, "alto"), (25, "alto")])
def test_ej1_nivel(valor, esperado):
    assert ej1.nivel(valor) == esperado


def test_ej1_probabilidad_fuera_de_rango():
    with pytest.raises(ValidationError):
        riesgo("X", 6, 1)


def test_ej1_ordenar():
    riesgos = [riesgo("B", 2, 2), riesgo("C", 5, 4), riesgo("A", 2, 2)]
    assert [r.id for r in ej1.ordenar(riesgos)] == ["C", "A", "B"]


def test_ej1_sin_control():
    riesgos = [riesgo("A", 1, 2), riesgo("B", 3, 3), riesgo("C", 5, 5, ["Revisión humana"])]
    assert ej1.sin_control(riesgos) == ["B"]


def test_ej1_a_markdown():
    tabla = ej1.a_markdown([riesgo("A", 1, 1), riesgo("B", 4, 4, ["MFA", "Registro"])]).splitlines()
    assert tabla[0] == "| Id | Riesgo | Categoría | P | I | Exposición | Nivel | Controles |"
    assert tabla[2] == "| B | Riesgo B | seguridad | 4 | 4 | 16 | alto | MFA; Registro |"
    assert tabla[3].endswith("| 1 | bajo | (ninguno) |")


def test_ej1_ejemplo_tiene_un_riesgo_sin_control():
    assert ej1.sin_control(ej1.riesgos_ejemplo()) == ["R4"]


# ---------------------------------------------------------------- Ejercicio 2
def test_ej2_preguntar_usa_sistema_y_devuelve_texto():
    falso = llm.usar_llm_falso(["Un TMS es un sistema de gestión del transporte."])
    assert ej2.preguntar("¿Qué es un TMS?") == "Un TMS es un sistema de gestión del transporte."
    enviados = falso.recibidos[0]
    assert enviados[0]["role"] == "system" and "Atlántica" in enviados[0]["content"]
    assert enviados[-1] == {"role": "user", "content": "¿Qué es un TMS?"}


def test_ej2_conversacion_reenvia_el_historial():
    falso = llm.usar_llm_falso(["Encantado, Iván.", "Trabajas en Faro 2.0."])
    charla = ej2.Conversacion()
    charla.enviar("Soy Iván y trabajo en Faro 2.0.")
    assert charla.enviar("¿En qué proyecto trabajo?") == "Trabajas en Faro 2.0."
    segunda = falso.recibidos[1]
    assert [m["role"] for m in segunda] == ["system", "user", "assistant", "user"]
    assert segunda[2]["content"] == "Encantado, Iván."
    assert charla.turnos == 2
    assert len(charla.historial) == 5


def test_ej2_medir():
    resultado, segundos = ej2.medir(lambda a, b: a + b, 2, b=3)
    assert resultado == 5 and 0 <= segundos < 1


# ---------------------------------------------------------------- Ejercicio 3
def test_ej3_ejecutar_en_modelo():
    llm.usar_llm_falso(["uno dos tres cuatro"])
    r = ej3.ejecutar_en_modelo("Pregunta", "modelo-x")
    assert r["modelo"] == "modelo-x" and r["respuesta"] == "uno dos tres cuatro"
    assert r["tokens_salida"] == 4
    assert set(r) == {"modelo", "respuesta", "segundos", "tokens_salida", "tokens_por_segundo"}


def test_ej3_comparar_sigue_si_un_modelo_falla():
    def fallar(_):
        raise RuntimeError("modelo no encontrado")

    llm.usar_llm_falso(["bien", fallar, "también"])
    resultados = ej3.comparar_modelos("P", ["a", "b", "c"])
    assert [r["modelo"] for r in resultados] == ["a", "b", "c"]
    assert resultados[1]["respuesta"].startswith("ERROR:") and resultados[1]["tokens_salida"] == 0
    assert resultados[2]["respuesta"] == "también"


def test_ej3_tabla_recorta_y_limpia():
    resultados = [{"modelo": "m", "respuesta": "línea uno\nlínea dos " + "x" * 80, "segundos": 1.234,
                   "tokens_salida": 9, "tokens_por_segundo": 7.3}]
    fila = ej3.tabla_markdown(resultados, ancho=20).splitlines()[2]
    assert fila.startswith("| m | 1.2 | 9 | 7.3 | línea uno línea dos ")
    assert fila.endswith("… |") and "\n" not in fila
