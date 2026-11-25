"""Tests de los ejercicios de la sesión 10."""

import asyncio
from types import SimpleNamespace

import pytest

import s10_ej1_servidor_mcp as ej1
import s10_ej2_cliente_mcp as ej2
import s10_ej3_multiagente as ej3
import s10_ej4_matriz_decision as ej4
from comun import llm


# ---------------------------------------------------------------- Ejercicio 1
def test_ej1_listar_documentos():
    documentos = ej1.listar_documentos()
    assert len(documentos) == 12
    assert documentos[5] == {"nombre": "06_politica_infraestructura_cloud.md", "titulo": "Política de infraestructura en la nube", "codigo": "ATL-INF-006"}


def test_ej1_leer_documento_y_seguridad():
    assert "eu-south-2" in ej1.leer_documento("06_politica_infraestructura_cloud.md")
    for malo in ("../backlog.json", "..\\..\\.env", "/etc/passwd"):
        with pytest.raises(PermissionError):
            ej1.leer_documento(malo)
    with pytest.raises(FileNotFoundError):
        ej1.leer_documento("99_no_existe.md")


def test_ej1_indice():
    lineas = ej1.indice().splitlines()
    assert len(lineas) == 12 and lineas[0] == "- ATL-GEN-001 · Presentación de Atlántica Logística (01_presentacion_empresa.md)"


def test_ej1_herramientas_registradas_en_el_servidor():
    nombres = {h.name for h in asyncio.run(ej1.servidor.list_tools())}
    assert {"listar_documentos", "leer_documento", "buscar_documentacion"} <= nombres


def test_ej1_y_ej2_por_stdio():
    """Arranca el servidor de verdad y lo consulta por MCP (no necesita el modelo)."""
    assert {"listar_documentos", "leer_documento", "buscar_documentacion"} <= set(asyncio.run(ej2.listar_herramientas(ej1.__file__)))


# ---------------------------------------------------------------- Ejercicio 2
def test_ej2_mcp_a_openai():
    herramienta = SimpleNamespace(name="sumar", description="Suma.", input_schema={
        "title": "sumarArguments", "type": "object", "required": ["a"],
        "properties": {"a": {"title": "A", "type": "integer"}}})
    assert ej2.mcp_a_openai(herramienta) == {"type": "function", "function": {
        "name": "sumar", "description": "Suma.",
        "parameters": {"type": "object", "required": ["a"], "properties": {"a": {"type": "integer"}}}}}


def test_ej2_texto_resultado():
    ok = SimpleNamespace(content=[SimpleNamespace(text="uno"), SimpleNamespace(text="dos")], is_error=False)
    error = SimpleNamespace(content=[SimpleNamespace(text="No existe")], is_error=True)
    assert ej2.texto_resultado(ok) == "uno\ndos"
    assert ej2.texto_resultado(error) == "ERROR: No existe"


def test_ej2_agente_mcp_usa_el_servidor():
    llm.usar_llm_falso([{"herramienta": "leer_documento", "argumentos": {"nombre": "08_procedimiento_gestion_cambios.md"}},
                        "Lo regula ATL-OPS-008."])
    resultado = asyncio.run(ej2.agente_mcp("¿Qué documento regula los cambios?", ej1.__file__))
    assert resultado["terminado"] and resultado["respuesta"] == "Lo regula ATL-OPS-008."
    assert "Comité de Cambios" in resultado["pasos"][0]["resultado"]


# ---------------------------------------------------------------- Ejercicio 3
def test_ej3_siguiente():
    assert ej3.siguiente({"aprobado": True, "iteraciones": 1}) == ej3.END
    assert ej3.siguiente({"aprobado": False, "iteraciones": 1}) == "redactor"
    assert ej3.siguiente({"aprobado": False, "iteraciones": ej3.MAX_REVISIONES}) == ej3.END


def test_ej3_flujo_con_una_correccion():
    falso = llm.usar_llm_falso(["- Dato [cambios.md]", "Borrador 1", "Falta citar el documento.", "Borrador 2 (cambios.md)", "APROBADO"])
    buscados = []
    final = ej3.ejecutar("¿Cuándo es el CAB?", lambda p: buscados.append(p) or "[1] cambios.md › CAB")
    assert buscados == ["¿Cuándo es el CAB?"]
    assert final["borrador"] == "Borrador 2 (cambios.md)" and final["aprobado"] and final["iteraciones"] == 2
    assert "Correcciones del revisor: Falta citar el documento." in falso.recibidos[3][-1]["content"]


def test_ej3_para_en_el_maximo_de_revisiones():
    llm.usar_llm_falso(["notas", "b1", "mal", "b2", "mal otra vez", "b3", "no usado"])
    final = ej3.ejecutar("x", lambda p: "fragmentos")
    assert final["iteraciones"] == ej3.MAX_REVISIONES and not final["aprobado"] and final["borrador"] == "b2"


# ---------------------------------------------------------------- Ejercicio 4
def test_ej4_normalizar():
    assert ej4.normalizar_pesos({"a": 1, "b": 3}) == {"a": 0.25, "b": 0.75}
    for malo in ({"a": 0}, {"a": -1, "b": 2}):
        with pytest.raises(ValueError):
            ej4.normalizar_pesos(malo)


def test_ej4_puntuar_y_errores():
    o = ej4.Opcion("X", {"a": 5, "b": 1})
    assert ej4.puntuar(o, {"a": 1, "b": 1}) == 3.0
    with pytest.raises(ValueError):
        ej4.puntuar(o, {"a": 1, "c": 1})
    with pytest.raises(ValueError):
        ej4.puntuar(ej4.Opcion("Y", {"a": 6}), {"a": 1})


def test_ej4_ranking_y_tabla():
    opciones = [ej4.Opcion("B", {"a": 3}), ej4.Opcion("A", {"a": 3}), ej4.Opcion("C", {"a": 5})]
    assert ej4.ranking(opciones, {"a": 1}) == [("C", 5.0), ("A", 3.0), ("B", 3.0)]
    lineas = ej4.tabla(opciones[:2], {"a": 2}).splitlines()
    assert lineas[0] == "| Criterio | Peso | B | A |"
    assert lineas[2] == "| a | 1.00 | 3 | 3 |" and lineas[-1] == "| **Total** | 1.00 | 3.00 | 3.00 |"
