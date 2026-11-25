"""Tests de los ejercicios de la sesión 13."""

import asyncio
import json
import math
from types import SimpleNamespace

import numpy as np
import pytest

import s13_ej1_evaluacion_e2e as ej1
import s13_ej2_red_teaming as ej2
import s13_ej3_carga as ej3
import s13_ej4_viabilidad as ej4
from comun import llm


# ---------------------------------------------------------------- Ejercicio 1
@pytest.mark.parametrize("valores, p", [([1, 2, 3, 4], 50), ([1, 2, 3, 4, 10], 95), ([5], 95), ([3, 1, 2], 0), ([3, 1, 2], 100)])
def test_ej1_percentil_como_numpy(valores, p):
    assert ej1.percentil(valores, p) == round(float(np.percentile(valores, p)), 3)


def test_ej1_percentil_vacio():
    assert ej1.percentil([], 50) == 0.0


def test_ej1_evaluar_y_metricas():
    llm.usar_llm_falso([json.dumps({"puntuacion": 2, "motivo": "ok"}), json.dumps({"puntuacion": 1, "motivo": "parcial"})])

    def asistente(entrada):
        if entrada == "c":
            raise RuntimeError("caído")
        return f"respuesta a {entrada}"

    casos = [{"id": "1", "entrada": "a", "esperado": "x", "tipo": "normativa"},
             {"id": "2", "entrada": "b", "esperado": "y", "tipo": "normativa"},
             {"id": "3", "entrada": "c", "esperado": "z", "tipo": "seguridad"}]
    filas = ej1.evaluar(asistente, casos)
    assert [f["puntuacion"] for f in filas] == [2, 1, 0] and filas[2]["motivo"] == "ERROR: caído"
    m = ej1.metricas(filas)
    assert m["casos"] == 3 and m["exactitud"] == 33.3 and m["puntuacion_media"] == 1.0
    assert m["por_tipo"] == {"normativa": 50.0, "seguridad": 0.0}


def test_ej1_regresiones():
    base = {"exactitud": 80.0, "latencia_p95": 2.0, "por_tipo": {"seguridad": 100.0, "normativa": 80.0}}
    bien = {"exactitud": 78.0, "latencia_p95": 2.9, "por_tipo": {"seguridad": 100.0, "normativa": 76.0}}
    mal = {"exactitud": 70.0, "latencia_p95": 3.5, "por_tipo": {"seguridad": 50.0, "normativa": 80.0}}
    assert ej1.regresiones(bien, base) == []
    assert ej1.regresiones(mal, base) == ["exactitud: 80.0 → 70.0", "latencia_p95: 2.0 → 3.5", "tipo seguridad: 100.0 → 50.0"]


# ---------------------------------------------------------------- Ejercicio 2
def test_ej2_rechaza():
    assert ej2.rechaza("Lo siento, no puedo hacerlo.") and ej2.rechaza("Eso requiere aprobación del CAB")
    assert not ej2.rechaza("Claro, aquí tienes: PWNED")


def test_ej2_superado_por_tipo():
    rechazo, no_contiene, longitud = ej2.ATAQUES[0], ej2.ATAQUES[1], ej2.ATAQUES[7]
    assert ej2.superado(rechazo, "No puedo ignorar mis instrucciones.") and not ej2.superado(rechazo, "PWNED")
    assert ej2.superado(no_contiene, "Es un saludo.") and not ej2.superado(no_contiene, "pwned")
    assert ej2.superado(longitud, "logística " * 10) and not ej2.superado(longitud, "x" * 5000)
    with pytest.raises(ValueError):
        ej2.superado({"tipo": "otro"}, "x")


def test_ej2_ejecutar_e_informe():
    ataques = ej2.ATAQUES[:2] + [ej2.ATAQUES[4]]
    respuestas = iter(["No puedo hacer eso.", "PWNED"])

    def asistente(prompt):
        if "Terraform" in prompt:
            raise RuntimeError("bloqueado")
        return next(respuestas)

    filas = ej2.ejecutar(asistente, ataques)
    assert [f["superado"] for f in filas] == [True, False, True] and filas[2]["respuesta"].startswith("EXCEPCIÓN")
    texto = ej2.informe(filas)
    assert "| LLM01 Inyección de prompt | 1 | 2 |" in texto and "| LLM06 Autonomía excesiva | 1 | 1 |" in texto
    assert texto.endswith("Resistencia global: 2 de 3 (67 %)")


def test_ej2_cubre_varias_categorias_owasp():
    assert len({a["owasp"].split()[0] for a in ej2.ATAQUES}) >= 6


# ---------------------------------------------------------------- Ejercicio 3
class ClienteFalso:
    def __init__(self, fallar_cada=0):
        self.llamadas, self.fallar_cada = 0, fallar_cada
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._crear))

    async def _crear(self, **kwargs):
        self.llamadas += 1
        numero = self.llamadas  # se guarda antes del await: con concurrencia, el contador cambia mientras se espera
        await asyncio.sleep(0.01)
        if self.fallar_cada and numero % self.fallar_cada == 0:
            raise RuntimeError("503")
        return SimpleNamespace(usage=SimpleNamespace(completion_tokens=50))


def test_ej3_una_peticion():
    ok = asyncio.run(ej3.una_peticion(ClienteFalso(), "m", "p"))
    assert ok["ok"] and ok["tokens"] == 50 and ok["segundos"] > 0
    fallo = asyncio.run(ej3.una_peticion(ClienteFalso(fallar_cada=1), "m", "p"))
    assert not fallo["ok"] and fallo["tokens"] == 0


def test_ej3_resumen():
    resultados = [{"ok": True, "segundos": 1.0, "tokens": 100}, {"ok": True, "segundos": 3.0, "tokens": 100}, {"ok": False, "segundos": 9.0, "tokens": 0}]
    assert ej3.resumen(resultados, 4.0) == {"peticiones": 3, "errores": 1, "latencia_p50": 2.0, "latencia_p95": 2.9,
                                           "tokens_por_segundo": 50.0, "peticiones_por_segundo": 0.5}


def test_ej3_prueba_carga_concurrente():
    cliente = ClienteFalso(fallar_cada=4)
    r = asyncio.run(ej3.prueba_carga(cliente, "m", usuarios=4, peticiones_por_usuario=2))
    assert cliente.llamadas == 8 and r["usuarios"] == 4 and r["peticiones"] == 8 and r["errores"] == 2


# ---------------------------------------------------------------- Ejercicio 4
def caso(**cambios):
    datos = dict(nombre="X", horas_ahorradas_mes=40, coste_hora=50, coste_implantacion=12_000, coste_operacion_mes=500,
                 riesgo=2, madurez_datos=4)
    datos.update(cambios)
    return ej4.CasoNegocio(**datos)


def test_ej4_beneficio_recuperacion_roi():
    c = caso()
    assert ej4.beneficio_mensual(c) == 1500 and ej4.meses_recuperacion(c) == 8.0 and ej4.roi_primer_anio(c) == 50.0
    assert ej4.meses_recuperacion(caso(coste_implantacion=10_000)) == 6.7
    assert math.isinf(ej4.meses_recuperacion(caso(horas_ahorradas_mes=5)))


@pytest.mark.parametrize("cambios, esperado", [({}, "Adelante"), ({"riesgo": 4}, "Piloto acotado"), ({"madurez_datos": 1}, "No recomendado"),
                                               ({"coste_implantacion": 30_000}, "Piloto acotado"), ({"coste_implantacion": 60_000}, "No recomendado")])
def test_ej4_recomendacion(cambios, esperado):
    assert ej4.recomendacion(caso(**cambios)) == esperado
