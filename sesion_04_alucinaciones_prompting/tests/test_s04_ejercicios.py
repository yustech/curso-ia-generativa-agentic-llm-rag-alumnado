"""Tests de los ejercicios de la sesión 4."""

import json

import pytest
from pydantic import ValidationError

import s04_ej1_banco_alucinaciones as ej1
import s04_ej2_plantilla_prompt as ej2
import s04_ej3_tecnicas as ej3
import s04_ej4_salida_estructurada as ej4
import s04_ej5_evaluar_prompts as ej5
from comun import llm


# ---------------------------------------------------------------- Ejercicio 1
def test_ej1_cargar_casos():
    casos = ej1.cargar_casos()
    assert len(casos) == 10 and all("criterio" in c for c in casos)


def test_ej1_contiene_alguna_ignora_tildes_y_mayusculas():
    assert ej1.contiene_alguna("Lo siento, NO LO SE con certeza.", ej1.MARCAS_ABSTENCION)
    assert not ej1.contiene_alguna("Fue en 2019.", ej1.MARCAS_ABSTENCION)


@pytest.mark.parametrize("texto, esperado", [
    ("El resultado es 3.536,5049", ["3536.5049"]),
    ("3536,5049", ["3536.5049"]),
    ("3536.5049", ["3536.5049"]),
    ("Hay 5 letras", ["5"]),
    ("El pedido 48.379 pesa 1.234,56 kg", ["48379", "1234.56"]),
])
def test_ej1_numeros_en(texto, esperado):
    assert ej1.numeros_en(texto) == esperado


def test_ej1_evaluar_por_criterio():
    assert ej1.evaluar({"criterio": "abstener"}, "No consta en la información disponible.") == "correcta"
    assert ej1.evaluar({"criterio": "abstener"}, "Lo ganó en 2019.") == "alucinacion"
    assert ej1.evaluar({"criterio": "valor", "valor": "5"}, "Hay 5 erres.") == "correcta"
    assert ej1.evaluar({"criterio": "valor", "valor": "5"}, "Hay 4.") == "alucinacion"
    assert ej1.evaluar({"criterio": "rechazar_premisa"}, "En realidad Python sigue teniendo tipado dinámico.") == "correcta"
    assert ej1.evaluar({"criterio": "rechazar_premisa"}, "Porque se volvió estático.") == "alucinacion"
    assert ej1.evaluar({"criterio": "manual"}, "lo que sea") == "revisar"


def test_ej1_ejecutar_y_resumen():
    casos = [{"id": "A", "tipo": "x", "criterio": "abstener", "pregunta": "?"},
             {"id": "B", "tipo": "y", "criterio": "valor", "valor": "5", "pregunta": "?"},
             {"id": "C", "tipo": "z", "criterio": "manual", "pregunta": "?"}]
    falso = llm.usar_llm_falso(["Fue en 2019.", "5", "texto"])
    resultados = ej1.ejecutar(casos, sistema="S")
    assert [r["veredicto"] for r in resultados] == ["alucinacion", "correcta", "revisar"]
    assert falso.recibidos[0][0] == {"role": "system", "content": "S"}
    assert ej1.resumen(resultados) == {"correcta": 1, "alucinacion": 1, "revisar": 1, "tasa_alucinacion": 50.0}
    assert ej1.resumen([])["tasa_alucinacion"] == 0.0


# ---------------------------------------------------------------- Ejercicio 2
def plantilla():
    return ej2.PlantillaPrompt(rol="R", objetivo="O", instrucciones=["a", "b"], restricciones=["x"],
                               ejemplos=[("p1", "r1")])


def test_ej2_sistema_secciones_en_orden():
    texto = plantilla().sistema()
    assert texto == "# Rol\nR\n\n# Objetivo\nO\n\n# Instrucciones\n1. a\n2. b\n\n# Restricciones\n- x"


def test_ej2_sistema_completo():
    p = ej2.plantilla_infrapilot()
    texto = p.sistema()
    titulos = [l for l in texto.splitlines() if l.startswith("# ")]
    assert titulos == ["# Rol", "# Objetivo", "# Contexto", "# Instrucciones", "# Formato de salida", "# Restricciones"]


def test_ej2_mensajes_con_ejemplos():
    mensajes = plantilla().mensajes("hola")
    assert [m["role"] for m in mensajes] == ["system", "user", "assistant", "user"]
    assert mensajes[-1]["content"] == "<entrada>\nhola\n</entrada>"


def test_ej2_huella_cambia_con_el_prompt():
    a, b = plantilla(), plantilla()
    assert a.huella() == b.huella() and len(a.huella()) == 8
    b.restricciones.append("y")
    assert a.huella() != b.huella()


# ---------------------------------------------------------------- Ejercicio 3
@pytest.mark.parametrize("texto, esperado", [("Sistemas.", "sistemas"), ("Categoría: ALMACÉN", "almacén"),
                                             ("transporte o sistemas", "transporte"), ("ninguna", None)])
def test_ej3_normalizar(texto, esperado):
    assert ej3.normalizar_categoria(texto) == esperado


def test_ej3_zero_shot():
    falso = llm.usar_llm_falso(["Almacén"])
    assert ej3.zero_shot("Faltan palés") == "almacén"
    assert "Faltan palés" in falso.recibidos[0][-1]["content"]


def test_ej3_few_shot_mensajes():
    mensajes = ej3.mensajes_few_shot("X")
    assert mensajes[0]["role"] == "system"
    assert [m["role"] for m in mensajes[1:]] == ["user", "assistant"] * len(ej3.EJEMPLOS) + ["user"]
    assert mensajes[2]["content"] == "transporte" and mensajes[-1]["content"] == "X"
    llm.usar_llm_falso(["sistemas"])
    assert ej3.few_shot("X") == "sistemas"


def test_ej3_extraer_respuesta_final():
    assert ej3.extraer_respuesta_final("paso 1\nRespuesta final: 126 €") == "126 €"
    assert ej3.extraer_respuesta_final("respuesta final: 1\nmás\nRESPUESTA FINAL:  2 ") == "2"
    assert ej3.extraer_respuesta_final("uno\ndos\n\n") == "dos"


def test_ej3_con_razonamiento():
    llm.usar_llm_falso(["114 + 12 = 126\nRespuesta final: 126 €"])
    completo, final = ej3.con_razonamiento("¿Precio?")
    assert final == "126 €" and "114" in completo


# ---------------------------------------------------------------- Ejercicio 4
def test_ej4_clasificar():
    llm.usar_llm_falso([json.dumps({"categoria": "sistemas", "prioridad": "P1", "resumen": "Faro caído", "requiere_humano": True})])
    c = ej4.clasificar("Faro caído")
    assert c.prioridad == "P1" and ej4.problemas_de_negocio(c) == []


def test_ej4_esquema_rechaza_valores_invalidos():
    with pytest.raises(ValidationError):
        ej4.ClasificacionIncidencia(categoria="otra", prioridad="P1", resumen="x", requiere_humano=True)


def test_ej4_problemas_y_corregir():
    c = ej4.ClasificacionIncidencia(categoria="sistemas", prioridad="P2", resumen="  ", requiere_humano=False)
    assert ej4.problemas_de_negocio(c) == ["P1 y P2 requieren intervención humana", "Resumen vacío"]
    assert ej4.corregir(c).requiere_humano is True
    d = ej4.ClasificacionIncidencia(categoria="almacén", prioridad="P4", resumen="Consulta", requiere_humano=True)
    assert ej4.problemas_de_negocio(d) == ["P3 y P4 no deberían escalar"]
    assert ej4.corregir(d).requiere_humano is False and d.requiere_humano is True


# ---------------------------------------------------------------- Ejercicio 5
def test_ej5_palabras_clave():
    assert ej5.palabras_clave("La política prohíbe buckets públicos, según ATL.") == {"politica", "prohibe", "buckets", "publicos"}


def test_ej5_puntuar():
    assert ej5.puntuar("Está prohibido: la política no permite buckets públicos.", "Prohíbe buckets públicos") == 0.67
    assert ej5.puntuar("lo que sea", "sí") == 1.0


def test_ej5_evaluar_y_comparar():
    casos = [{"id": "1", "entrada": "a", "esperado": "región europea"}, {"id": "2", "entrada": "b", "esperado": "etiquetas obligatorias"}]
    buena = ej5.evaluar_version("v2", lambda e: "región europea con etiquetas obligatorias", casos)
    mala = ej5.evaluar_version("v1", lambda e: "no sé", casos)
    assert buena == {"version": "v2", "media": 1.0, "por_caso": {"1": 1.0, "2": 1.0}}
    texto = ej5.comparar([mala, buena])
    assert texto.splitlines()[2] == "| v2 | 1.00 |" and texto.endswith("Mejor: v2")


def test_ej5_cargar_golden_del_reto():
    casos = ej5.cargar_golden("datos/atlantica/evaluacion/golden_e2_infrapilot.jsonl")
    assert len(casos) == 10 and {"id", "entrada", "esperado"} <= set(casos[0])
