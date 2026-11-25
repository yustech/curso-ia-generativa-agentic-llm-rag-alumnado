"""Tests de los ejercicios de la sesión 12."""

import json

import pytest

import s12_ej1_extraccion as ej1
import s12_ej2_generacion as ej2
import s12_ej3_validacion as ej3
from comun import llm

ACTA = """Reunión del 24/11/2026. Estuvimos Lucía, Andrés e Iván.
Acciones: Lucía pide el certificado de correo (25/11). Andrés fusiona las historias duplicadas (26/11).
Riesgo nuevo: ausencia de la diseñadora. Probabilidad 5, impacto 3."""


# ---------------------------------------------------------------- Ejercicio 1
@pytest.mark.parametrize("texto, esperado", [
    ("3 de noviembre de 2026", "2026-11-03"), ("10/11/2026", "2026-11-10"), ("25/11", "2026-11-25"),
    ("2026-11-03", "2026-11-03"), ("17 de Noviembre", "2026-11-17"), ("el jueves 12", None), (None, None), ("40/13", None)])
def test_ej1_normalizar_fecha(texto, esperado):
    assert ej1.normalizar_fecha(texto) == esperado


def test_ej1_aparece():
    assert ej1.aparece("Lucía Prieto", "Estuvimos Lucía y Andrés")
    assert ej1.aparece("Ivan Seoane", "Iván comenta")
    assert not ej1.aparece("Marta Iglesias", "Estuvimos Lucía y Andrés")
    assert not ej1.aparece("Al", "al final")


def test_ej1_extraer_normaliza_fechas():
    datos = {"fecha": "24/11/2026", "asistentes": ["Lucía", "Andrés", "Iván"], "decisiones": [],
             "acciones": [{"descripcion": "Pedir certificado", "responsable": "Lucía", "fecha": "25/11"},
                          {"descripcion": "Fusionar historias", "responsable": "Andrés", "fecha": "cuanto antes"}],
             "riesgos": [{"descripcion": "Ausencia de la diseñadora", "probabilidad": 5, "impacto": 3}]}
    falso = llm.usar_llm_falso([json.dumps(datos)])
    acta = ej1.extraer_acta(ACTA)
    assert acta.fecha == "2026-11-24" and acta.acciones[0].fecha == "2026-11-25" and acta.acciones[1].fecha == "cuanto antes"
    assert falso.recibidos[0][0]["content"] == ej1.SISTEMA


def test_ej1_trazabilidad():
    acta = ej1.Acta(fecha="2026-11-24", asistentes=["Lucía", "Marta Iglesias"], decisiones=[],
                    acciones=[ej1.Accion(descripcion="x", responsable="Andrés"), ej1.Accion(descripcion="y", responsable="Pedro Pérez")],
                    riesgos=[ej1.Riesgo(descripcion="Diseñadora", probabilidad=5, impacto=3), ej1.Riesgo(descripcion="Plazo")])
    assert ej1.problemas_trazabilidad(acta, ACTA) == ["Asistente no encontrado: Marta Iglesias", "Responsable no encontrado: Pedro Pérez",
                                                      "Riesgo sin probabilidad o impacto: Plazo"]


# ---------------------------------------------------------------- Ejercicio 2
@pytest.mark.parametrize("d, peligro, color", [(5, False, "Verde"), (5.1, False, "Ámbar"), (15, False, "Ámbar"), (15.1, False, "Rojo"), (0, True, "Rojo")])
def test_ej2_semaforo(d, peligro, color):
    assert ej2.semaforo(d, peligro) == color


def test_ej2_semaforo_general():
    assert ej2.semaforo_general(ej2.DATOS_EJEMPLO) == "Rojo"  # el piloto está «En riesgo»
    sin_riesgo = ej2.DatosInforme("P", "s", 1, 10, 5, desviacion_plazo=8, desviacion_coste=2)
    assert ej2.semaforo_general(sin_riesgo) == "Ámbar"


def test_ej2_generar_informe():
    informe = ej2.generar_informe(ej2.DATOS_EJEMPLO, "Línea 1\nLínea 2\nLínea 3")
    assert informe.startswith("# Informe de estado · Faro 2.0 · 23 al 27 de noviembre de 2026")
    assert [l[3:] for l in informe.splitlines() if l.startswith("## ")] == ej2.SECCIONES
    assert "| Rojo | Rojo | Verde |" in informe
    assert "30 de 34 puntos completados (88 %)." in informe
    riesgos = [l for l in informe.splitlines() if l.startswith("| ") and "| Sí |" in l or "| No |" in l]
    assert riesgos[0].startswith("| Plazo ajustado") and riesgos[0].endswith("| 16 | Sí |")
    assert "| 15 | Sí |" in informe and "| 6 | No |" in informe
    assert "- Confirmar el apoyo" in informe and informe.rstrip().endswith("informe_estado_2026-11-20.md.")


def test_ej2_informe_sin_decisiones_ni_puntos():
    datos = ej2.DatosInforme("P", "s", 1, 0, 0, 0, 0)
    informe = ej2.generar_informe(datos, "a\nb\nc")
    assert "0 de 0 puntos completados (0 %)." in informe and "Ninguna." in informe and "Fuentes:" not in informe


# ---------------------------------------------------------------- Ejercicio 3
def test_ej3_comprobaciones_ok_y_fallos():
    bueno = ej2.generar_informe(ej2.DATOS_EJEMPLO, "Línea 1\nLínea 2\nLínea 3")
    assert all(f["ok"] for f in ej3.comprobaciones(bueno, 30, 34))
    malo = bueno.replace("30 de 34", "31 de 34").replace("Línea 3", "").replace("## 4. Hitos próximos", "## Hitos")
    resultado = {f["comprobacion"]: f["ok"] for f in ej3.comprobaciones(malo, 30, 34)}
    assert resultado == {"secciones": False, "semaforo": True, "cifras": False, "resumen_tres_lineas": False}


def test_ej3_juzgar():
    llm.usar_llm_falso([json.dumps({"puntuacion": 4, "cumple": True, "motivos": ["Cifras correctas"]})])
    juicio = ej3.juzgar("informe", "datos")
    assert juicio.puntuacion == 4 and juicio.cumple


def test_ej3_muestra_revision():
    elementos = [f"a{i}" for i in range(12)]
    muestra = ej3.muestra_revision(elementos, 20)
    assert len(muestra) == 3 and muestra == ej3.muestra_revision(elementos, 20) and muestra == sorted(muestra, key=elementos.index)
    assert len(ej3.muestra_revision(elementos[:2], 1)) == 1 and ej3.muestra_revision([], 50, minimo=0) == []


def test_ej3_informe_validacion():
    filas = [{"comprobacion": "cifras", "ok": True, "detalle": "x"}]
    texto = ej3.informe_validacion("inf", filas, ej3.Juicio(puntuacion=2, cumple=False, motivos=["Inventa un dato"]))
    assert texto.splitlines()[0] == "## Validación de inf" and "| cifras | ✅ | x |" in texto
    assert "Juez: 2/5 · cumple: no" in texto and "- Inventa un dato" in texto and texto.endswith("Veredicto: REVISIÓN HUMANA")
    assert ej3.informe_validacion("inf", filas, None).endswith("Veredicto: APTO")
