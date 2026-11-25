"""Tests de los ejercicios de la sesión 3."""

import pytest

import s03_ej1_tokens as ej1
import s03_ej2_memoria as ej2
import s03_ej3_aguja as ej3
import s03_ej4_muestreo_benchmark as ej4
from comun import llm


# ---------------------------------------------------------------- Ejercicio 1
def test_ej1_contar_y_trozos_coinciden():
    texto = "La logística inversa recupera los palés vacíos."
    piezas = ej1.trozos(texto)
    assert ej1.contar_tokens(texto) == len(piezas)
    assert "".join(piezas) == texto


def test_ej1_espanol_gasta_mas_que_ingles():
    es = ej1.tokens_por_palabra("La logística inversa recupera los palés vacíos de las tiendas.")
    en = ej1.tokens_por_palabra("Reverse logistics recovers empty pallets from the stores.")
    assert es > en


def test_ej1_tokens_por_palabra_vacio():
    assert ej1.tokens_por_palabra("   ") == 0.0


def test_ej1_estimar_coste():
    assert ej1.estimar_coste(1_000_000, 500_000, 0.40, 1.60) == 1.2
    assert ej1.estimar_coste(2000, 400, 0.40, 1.60) == 0.0014


def test_ej1_coste_mensual():
    assert ej1.coste_mensual(300, 2000, 400, 0.40, 1.60) == 9.24
    assert ej1.coste_mensual(100, 1000, 0, 1.0, 0, dias=30) == 3.0


def test_ej1_comparar_textos():
    filas = ej1.comparar_textos({"a": "hola mundo", "b": "adiós"})
    assert [f["nombre"] for f in filas] == ["a", "b"]
    assert filas[0]["palabras"] == 2 and filas[0]["tokens"] >= 2
    assert set(filas[0]) == {"nombre", "palabras", "tokens", "tokens_por_palabra"}


# ---------------------------------------------------------------- Ejercicio 2
def test_ej2_memoria_pesos():
    assert ej2.memoria_pesos_gb(8, 16) == 14.9
    assert ej2.memoria_pesos_gb(8, 4.8) == 4.47


def test_ej2_memoria_kv():
    assert ej2.memoria_kv_gb(32, 8, 128, 8192) == 1.0


def test_ej2_memoria_total():
    assert ej2.memoria_total_gb(8, "Q4_K_M", 32, 8, 128, 8192) == round((4.47 + 1.0) * 1.1, 2)
    with pytest.raises(ValueError):
        ej2.memoria_total_gb(8, "Q9", 32, 8, 128, 8192)


def test_ej2_cabe():
    assert ej2.cabe(8.9) and ej2.cabe(9.0)
    assert not ej2.cabe(9.1)
    assert ej2.cabe(20, ram_gb=64)


def test_ej2_contexto_maximo():
    maximo = ej2.contexto_maximo(8, "Q4_K_M", 32, 8, 128)
    assert maximo % 1024 == 0 and maximo > 8192
    assert ej2.cabe(ej2.memoria_total_gb(8, "Q4_K_M", 32, 8, 128, maximo))
    assert not ej2.cabe(ej2.memoria_total_gb(8, "Q4_K_M", 32, 8, 128, maximo + 1024))
    assert ej2.contexto_maximo(70, "F16", 80, 8, 128) == 0


# ---------------------------------------------------------------- Ejercicio 3
def test_ej3_pajar_posiciones():
    inicio = ej3.construir_pajar(10, "AGUJA", 0.0)
    final = ej3.construir_pajar(10, "AGUJA", 1.0)
    medio = ej3.construir_pajar(10, "AGUJA", 0.5)
    assert inicio.startswith("AGUJA") and final.endswith("AGUJA")
    assert medio.split(". ")[5].startswith("AGUJA") or "AGUJA" in medio.split(". ")[5]
    assert medio.count("AGUJA") == 1


def test_ej3_pajar_repite_frases():
    texto = ej3.construir_pajar(len(ej3.FRASES) + 1, "X", 1.0)
    assert texto.startswith(ej3.FRASES[0]) and texto.count(ej3.FRASES[0]) == 2


def test_ej3_posicion_invalida():
    with pytest.raises(ValueError):
        ej3.construir_pajar(5, "X", 1.5)


@pytest.mark.parametrize("respuesta, esperado", [("7342", True), ("El código es 7.342.", True), ("7 342", True), ("No lo sé", False)])
def test_ej3_encontrada(respuesta, esperado):
    assert ej3.encontrada(respuesta) is esperado


def test_ej3_tabla():
    fila = {"frases": 50, "posicion": 0.5, "num_ctx": 2048, "tokens_entrada": 900, "encontrada": False, "segundos": 1.2}
    lineas = ej3.tabla([fila]).splitlines()
    assert lineas[2] == "| 50 | 0.5 | 2048 | 900 | no | 1.2 |"


# ---------------------------------------------------------------- Ejercicio 4
def test_ej4_diversidad():
    assert ej4.diversidad(["A", "a ", "B", "c"]) == 0.75
    assert ej4.diversidad([]) == 0.0


def test_ej4_generar_varias_y_experimento():
    llm.usar_llm_falso(["Faro", "Faro", "Brújula", "Ancla"])
    assert ej4.generar_varias("p", 1.0, 2) == ["Faro", "Faro"]
    llm.usar_llm_falso(["X", "X", "Y", "Z"])
    assert ej4.experimento_temperatura("p", [0.0, 1.0], n=2) == {0.0: 0.5, 1.0: 1.0}


def test_ej4_resumen():
    assert ej4.resumen([10, 20, 30.04]) == {"media": 20.0, "minimo": 10.0, "maximo": 30.0}
    assert ej4.resumen([]) == {"media": 0.0, "minimo": 0.0, "maximo": 0.0}
