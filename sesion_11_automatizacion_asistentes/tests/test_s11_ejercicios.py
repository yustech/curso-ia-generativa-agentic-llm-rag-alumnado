"""Tests de los ejercicios de la sesión 11."""

from pathlib import Path
from types import SimpleNamespace

import pytest

import s11_ej1_proceso as ej1
import s11_ej2_asistente as ej2
import s11_ej4_backlog as ej4
from comun import llm


# ---------------------------------------------------------------- Ejercicio 1
def test_ej1_tiempos_y_automatizacion():
    assert ej1.tiempo_total(ej1.AS_IS) == 145 and ej1.tiempo_total(ej1.TO_BE) == 26
    assert ej1.porcentaje_automatizado(ej1.AS_IS) == 0.0
    assert ej1.porcentaje_automatizado(ej1.TO_BE) == round(100 * 6 / 26, 1)
    assert ej1.porcentaje_automatizado(ej1.Proceso("vacío")) == 0.0


def test_ej1_comparar():
    assert ej1.comparar(ej1.AS_IS, ej1.TO_BE) == {"antes": 145, "despues": 26, "ahorro_minutos": 119,
                                                  "ahorro_porcentaje": 82.1, "pasos_ia": 2, "controles_humanos": 1}


def test_ej1_avisos():
    assert ej1.avisos(ej1.TO_BE) == []
    malo = ej1.Proceso("x", [ej1.Paso("Revisar", "Bot", "automatico", 1, control_humano=True),
                             ej1.Paso("Generar", "IA", "ia", 1)])
    assert ej1.avisos(malo) == ["Revisar: control humano sin actor humano", "Generar: paso de IA sin control humano posterior"]


def test_ej1_mermaid():
    p = ej1.Proceso("p", [ej1.Paso("A", "Ana", "manual", 5, True), ej1.Paso("B", "Bot", "automatico", 1.5), ej1.Paso("C", "IA", "ia", 2)])
    assert ej1.a_mermaid(p).splitlines() == ["flowchart LR", '    P1["A · Ana · 5 min ✋"]', '    P2[["B · Bot · 1.5 min"]]',
                                             '    P3(["C · IA · 2 min"])', "    P1 --> P2", "    P2 --> P3"]


# ---------------------------------------------------------------- Ejercicio 2
TROZOS = [SimpleNamespace(referencia="vacaciones.md › 1. Vacaciones", texto="25 días laborables"),
          SimpleNamespace(referencia="vacaciones.md › 3. Teletrabajo", texto="3 días por semana")]


def buscar_falso(pregunta, k):
    return [(t, 0.9) for t in TROZOS[:k]]


@pytest.mark.parametrize("texto, esperado", [("Quiero hablar con una persona", True), ("Tengo una RECLAMACIÓN", True),
                                             ("¿Cuántos días de vacaciones tengo?", False)])
def test_ej2_necesita_humano(texto, esperado):
    assert ej2.necesita_humano(texto) is esperado


def test_ej2_bienvenida_transparente():
    texto = ej2.Asistente("Faro-IA", "S").bienvenida()
    assert texto.startswith("Hola, soy Faro-IA, un asistente de inteligencia artificial de Atlántica Logística.")


def test_ej2_responde_con_contexto_y_fuentes():
    falso = llm.usar_llm_falso(["Tienes 25 días laborables [1]."])
    a = ej2.Asistente("A", "SISTEMA", buscar=buscar_falso, k=2)
    r = a.responder("¿Cuántos días de vacaciones tengo?")
    assert r.texto == "Tienes 25 días laborables [1]." and r.fuentes == ["vacaciones.md › 1. Vacaciones"] and not r.escalado
    enviados = falso.recibidos[0]
    assert enviados[0] == {"role": "system", "content": "SISTEMA"}
    assert enviados[-1]["content"].startswith("[1] vacaciones.md › 1. Vacaciones\n25 días")
    assert enviados[-1]["content"].endswith("Pregunta: ¿Cuántos días de vacaciones tengo?")
    assert a.historial[0] == {"role": "user", "content": "¿Cuántos días de vacaciones tengo?"}


def test_ej2_memoria_de_ventana():
    falso = llm.usar_llm_falso(["r1", "r2", "r3"])
    a = ej2.Asistente("A", "S", max_mensajes=2)
    for pregunta in ("p1", "p2", "p3"):
        a.responder(pregunta)
    assert [m["content"] for m in falso.recibidos[2]] == ["S", "p2", "r2", "p3"]


def test_ej2_escala_sin_llamar_al_modelo():
    falso = llm.usar_llm_falso(["no"])
    r = ej2.Asistente("A", "S").responder("Esto es urgente, quiero hablar con una persona")
    assert r.escalado and r.texto == ej2.MENSAJE_ESCALADO and falso.recibidos == []


# ---------------------------------------------------------------- Ejercicio 3 (interfaz)
def test_ej3_app_de_chat(monkeypatch):
    from streamlit.testing.v1 import AppTest

    llm.usar_llm_falso(["Son 25 días laborables [1]."])
    import s11_ej2_asistente

    monkeypatch.setattr(s11_ej2_asistente, "asistente_atlantica", lambda: ej2.Asistente("Faro-IA", "S", buscar=buscar_falso))
    import s11_ej3_app  # noqa: F401  (comprueba que el módulo se puede importar)

    ruta = Path(s11_ej3_app.__file__)
    app = AppTest.from_file(str(ruta)).run()
    assert "inteligencia artificial" in app.chat_message[0].markdown[0].value
    app.chat_input[0].set_value("¿Cuántos días de vacaciones tengo?").run()
    assert app.chat_message[-1].markdown[0].value == "Son 25 días laborables [1]."
    assert "vacaciones.md › 1. Vacaciones" in app.chat_message[-1].caption[0].value


# ---------------------------------------------------------------- Ejercicio 4
HISTORIAS = [ej4.Historia("H1", "Bienvenida", 8, 2, "M"), ej4.Historia("H2", "Citas", 9, 3, "M"),
             ej4.Historia("H3", "Exportar", 4, 5, "C"), ej4.Historia("H4", "Voz", 6, 13, "S"),
             ej4.Historia("H5", "Modo oscuro", 2, 1, "W"), ej4.Historia("H6", "Historial", 6, 3, "S")]


def test_ej4_puntuacion_y_prioridad():
    assert ej4.puntuacion(HISTORIAS[0]) == 4.0
    assert [h.id for h in ej4.priorizar(HISTORIAS)] == ["H1", "H2", "H6", "H4", "H3", "H5"]


def test_ej4_planificar_sprints():
    assert ej4.planificar_sprints(HISTORIAS, capacidad=8) == [["H1", "H2", "H6"], ["H3"]]
    assert ej4.planificar_sprints(HISTORIAS, capacidad=5, max_sprints=2) == [["H1", "H2"], ["H6"]]


def test_ej4_tabla():
    lineas = ej4.a_markdown(HISTORIAS[:2]).splitlines()
    assert lineas[2] == "| 1 | H1 | Bienvenida | M | 8 | 2 | 4.00 |" and lineas[3] == "| 2 | H2 | Citas | M | 9 | 3 | 3.00 |"
