"""Tests de los ejercicios de la sesión 7."""

import json

import pytest

import s07_ej1_ingesta as ej1
import s07_ej2_evaluar_rag as ej2
import s07_ej3_bucle_agente as ej3
from comun import llm
from comun.documentos import Documento


# ---------------------------------------------------------------- Ejercicio 1
def test_ej1_huella():
    assert ej1.huella("hola") == ej1.huella("hola") and len(ej1.huella("hola")) == 16
    assert ej1.huella("hola") != ej1.huella("hola.")


def test_ej1_clasificar_cambios():
    docs = [Documento("a.md", "A", "uno"), Documento("b.md", "B", "dos cambiado"), Documento("d.md", "D", "nuevo")]
    manifiesto = {"a.md": ej1.huella("uno"), "b.md": ej1.huella("dos"), "c.md": ej1.huella("tres")}
    assert ej1.clasificar_cambios(docs, manifiesto) == {
        "nuevos": ["d.md"], "modificados": ["b.md"], "eliminados": ["c.md"], "sin_cambios": ["a.md"]}


def escribir(carpeta, nombre, titulo, secciones):
    cuerpo = "\n\n".join(f"## {s}\n\nContenido de {s}." for s in secciones)
    (carpeta / nombre).write_text(f"---\ntitulo: {titulo}\n---\n\n# {titulo}\n\n{cuerpo}\n", encoding="utf-8")


def test_ej1_ingesta_incremental(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    escribir(docs, "a.md", "Doc A", ["Uno", "Dos"])
    escribir(docs, "b.md", "Doc B", ["Tres"])
    pipeline = ej1.PipelineIngesta(tmp_path / "indice", "prueba")
    assert pipeline.procesar(docs) == {"nuevos": 2, "modificados": 0, "eliminados": 0, "sin_cambios": 0,
                                       "trozos_indexados": 3, "total": 3}
    assert pipeline.procesar(docs)["trozos_indexados"] == 0
    escribir(docs, "a.md", "Doc A", ["Uno"])  # se quita una sección
    (docs / "b.md").unlink()
    informe = pipeline.procesar(docs)
    assert informe == {"nuevos": 0, "modificados": 1, "eliminados": 1, "sin_cambios": 0, "trozos_indexados": 1, "total": 1}
    assert json.loads(pipeline.ruta_manifiesto.read_text(encoding="utf-8")) == {"a.md": ej1.huella((docs / "a.md").read_text(encoding="utf-8").split("---\n", 2)[2].lstrip("\n"))}


# ---------------------------------------------------------------- Ejercicio 2
def test_ej2_se_abstiene():
    assert ej2.se_abstiene("No consta en la documentación.")
    assert ej2.se_abstiene("NO CONSTA")
    assert not ej2.se_abstiene("Son 25 días [1].")


def test_ej2_documentos_citados():
    assert ej2.documentos_citados("Dato [2] y [1], fuera [9]", ["a.md", "b.md"]) == {"a.md", "b.md"}
    assert ej2.documentos_citados("sin citas", ["a.md"]) == set()


def test_ej2_cobertura():
    assert ej2.cobertura("Son 25 días laborables según la política.", "25 días laborables") == 1.0
    assert ej2.cobertura("Hasta 3 días.", "Hasta 3 días por semana en puestos elegibles") == 0.4
    assert ej2.cobertura("x", "sí") == 1.0


def test_ej2_evaluar_pregunta_con_y_sin_fuente():
    con = {"id": "Q1", "fuente": "v.md", "respuesta": "25 días laborables"}
    r = ej2.evaluar_pregunta(con, ej2.Resultado("Son 25 días laborables [2].", ["x.md", "v.md"]))
    assert r == {"id": "Q1", "recuperacion_hit": True, "cita_correcta": True, "cobertura_respuesta": 1.0}
    sin = {"id": "Q2", "fuente": None, "respuesta": "No consta"}
    assert ej2.evaluar_pregunta(sin, ej2.Resultado("Cuesta 300 €", ["x.md"])) == {"id": "Q2", "abstencion_correcta": False}


def test_ej2_agregar_y_checklist():
    filas = [{"id": "1", "recuperacion_hit": True, "cita_correcta": False, "cobertura_respuesta": 1.0},
             {"id": "2", "recuperacion_hit": True, "cita_correcta": True, "cobertura_respuesta": 0.5},
             {"id": "3", "abstencion_correcta": True}]
    agregado = ej2.agregar(filas)
    assert agregado == {"recuperacion_hit": 1.0, "cita_correcta": 0.5, "cobertura_respuesta": 0.75, "abstencion_correcta": 1.0}
    lista = {f["criterio"]: f for f in ej2.checklist(agregado)}
    assert lista["recuperacion_hit"]["cumple"] and not lista["cita_correcta"]["cumple"]
    assert ej2.checklist({}, {"x": 0.5}) == [{"criterio": "x", "valor": None, "umbral": 0.5, "cumple": False}]


# ---------------------------------------------------------------- Ejercicio 3
@pytest.mark.parametrize("expresion, esperado", [("2 + 3 * 4", 14), ("(2 * 36 + 70) * 1.1", pytest.approx(156.2)),
                                                 ("-5 + 2 ** 3", 3), ("7 % 3", 1), ("1,5 * 2", 3.0)])
def test_ej3_calcular(expresion, esperado):
    assert ej3.calcular(expresion) == esperado


@pytest.mark.parametrize("expresion", ["__import__('os').system('dir')", "abs(-1)", "x + 1", "2 +", "'a' * 3", "True + 1"])
def test_ej3_calcular_rechaza(expresion):
    with pytest.raises(ValueError):
        ej3.calcular(expresion)


def test_ej3_esquema():
    e = ej3.esquema("f", "hace algo", {"x": {"type": "string"}}, ["x"])
    assert e == {"type": "function", "function": {"name": "f", "description": "hace algo",
                                                  "parameters": {"type": "object", "properties": {"x": {"type": "string"}}, "required": ["x"]}}}


def test_ej3_ejecutar_herramienta():
    registro = {"sumar": lambda a, b: a + b, "eco": lambda texto: texto, "falla": lambda: 1 / 0}
    assert ej3.ejecutar_herramienta("sumar", '{"a": 2, "b": 3}', registro) == "5"
    assert ej3.ejecutar_herramienta("eco", '{"texto": "hola"}', registro) == "hola"
    assert ej3.ejecutar_herramienta("nada", "{}", registro).startswith("ERROR:")
    assert ej3.ejecutar_herramienta("sumar", "no es json", registro).startswith("ERROR:")
    assert "ZeroDivisionError" in ej3.ejecutar_herramienta("falla", "", registro)


def test_ej3_bucle_con_herramientas():
    falso = llm.usar_llm_falso([{"herramienta": "calcular", "argumentos": {"expresion": "25 - 9"}}, "Te quedan 16 días."])
    resultado = ej3.bucle("¿Cuántos me quedan?", {"calcular": ej3.calcular}, ej3.herramientas_de_ejemplo()[1:2], sistema="S")
    assert resultado == {"respuesta": "Te quedan 16 días.", "terminado": True,
                         "pasos": [{"herramienta": "calcular", "argumentos": '{"expresion": "25 - 9"}', "resultado": "16"}]}
    segunda = falso.recibidos[1]
    assert segunda[0] == {"role": "system", "content": "S"}
    assert segunda[2]["role"] == "assistant" and segunda[2]["tool_calls"][0]["function"]["name"] == "calcular"
    assert segunda[3] == {"role": "tool", "tool_call_id": "llamada_1", "content": "16"}


def test_ej3_bucle_respeta_max_pasos():
    llm.usar_llm_falso([{"herramienta": "eco", "argumentos": {"texto": "x"}}] * 5)
    resultado = ej3.bucle("objetivo", {"eco": lambda texto: texto}, [], max_pasos=3)
    assert not resultado["terminado"] and len(resultado["pasos"]) == 3
    assert resultado["respuesta"] == "No he podido completar la tarea en el número máximo de pasos"
