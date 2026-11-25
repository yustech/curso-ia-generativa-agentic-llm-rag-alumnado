"""Tests de los ejercicios de la sesión 9."""

import json

import httpx
import pytest
from pydantic import BaseModel, Field

import s09_ej1_herramientas as ej1
import s09_ej2_cliente_api as ej2
import s09_ej3_agente_backlog as ej3
from comun import llm


# ---------------------------------------------------------------- Ejercicio 1
class ArgsSuma(BaseModel):
    a: int = Field(description="Primer sumando")
    b: int = Field(ge=0, description="Segundo sumando")


def registro():
    r = ej1.Registro()

    @r.herramienta(ArgsSuma, "Suma dos enteros.")
    def sumar(a, b):
        return a + b

    @r.herramienta(ArgsSuma, "Divide.", con_efectos=True)
    def dividir(a, b):
        return a / b

    return r


def test_ej1_resultado_como_texto():
    assert ej1.ResultadoHerramienta(True, datos={"ñ": 1}).como_texto() == '{"ok": true, "datos": {"ñ": 1}}'
    assert ej1.ResultadoHerramienta(False, error="x").como_texto() == '{"ok": false, "error": "x"}'


def test_ej1_esquemas():
    esquemas = registro().esquemas()
    assert [e["function"]["name"] for e in esquemas] == ["sumar", "dividir"]
    parametros = esquemas[0]["function"]["parameters"]
    assert "title" not in parametros and parametros["required"] == ["a", "b"]
    assert parametros["properties"]["b"]["minimum"] == 0
    assert esquemas[1]["function"]["description"].endswith("Acción con efectos: requiere confirmación humana.")
    assert registro().con_efectos() == {"dividir"}


def test_ej1_ejecutar_ok_y_errores():
    r = registro()
    ok = r.ejecutar("sumar", '{"a": 2, "b": 3}')
    assert ok.ok and ok.datos == 5 and ok.segundos >= 0
    assert r.ejecutar("restar", "{}").error == "Herramienta desconocida: restar"
    assert r.ejecutar("sumar", "{a: 1").error == "Los argumentos no son JSON válido"
    validacion = r.ejecutar("sumar", '{"a": "dos", "b": -1}').error
    assert validacion.startswith("Argumentos no válidos: ") and "a:" in validacion and "b:" in validacion
    assert r.ejecutar("dividir", '{"a": 1, "b": 0}').error.startswith("ZeroDivisionError:")


def test_ej1_ejecutor_devuelve_texto():
    assert json.loads(registro().ejecutor()("sumar", '{"a": 1, "b": 1}')) == {"ok": True, "datos": 2}


# ---------------------------------------------------------------- Ejercicio 2
def cliente_con(manejador, reintentos=3):
    esperas = []
    cliente = ej2.ClienteBacklog("http://api", transporte=httpx.MockTransport(manejador), reintentos=reintentos, dormir=esperas.append)
    return cliente, esperas


def test_ej2_espera_exponencial():
    assert [ej2.espera_exponencial(i) for i in (1, 2, 3, 4, 5, 6)] == [0.5, 1.0, 2.0, 4.0, 8.0, 8.0]


def test_ej2_listar_con_filtros():
    def manejador(peticion):
        assert peticion.url.path == "/historias" and dict(peticion.url.params) == {"sprint": "23"}
        assert peticion.headers["X-Api-Key"] == "clave-curso"
        return httpx.Response(200, json=[{"id": "FARO-142"}])

    cliente, _ = cliente_con(manejador)
    assert cliente.listar(sprint=23) == [{"id": "FARO-142"}]


def test_ej2_reintenta_errores_transitorios():
    respuestas = iter([httpx.Response(503, json={"error": "ocupado"}), httpx.Response(503, json={"error": "ocupado"}),
                       httpx.Response(200, json={"id": "FARO-1"})])
    cliente, esperas = cliente_con(lambda p: next(respuestas))
    assert cliente.obtener("FARO-1") == {"id": "FARO-1"}
    assert esperas == [0.5, 1.0] and cliente.intentos_realizados == 3


def test_ej2_agota_reintentos():
    cliente, esperas = cliente_con(lambda p: httpx.Response(503, json={"error": "ocupado"}), reintentos=2)
    with pytest.raises(ej2.ErrorAPI) as error:
        cliente.obtener("FARO-1")
    assert error.value.codigo == 503 and cliente.intentos_realizados == 3 and len(esperas) == 2


def test_ej2_errores_de_transporte():
    def manejador(peticion):
        raise httpx.ConnectTimeout("sin respuesta")

    cliente, _ = cliente_con(manejador, reintentos=1)
    with pytest.raises(ej2.ErrorAPI) as error:
        cliente.listar()
    assert error.value.codigo is None and cliente.intentos_realizados == 2


def test_ej2_error_definitivo_sin_reintentar():
    cliente, esperas = cliente_con(lambda p: httpx.Response(404, json={"error": "No existe FARO-9"}))
    with pytest.raises(ej2.ErrorAPI) as error:
        cliente.obtener("FARO-9")
    assert (error.value.codigo, error.value.detalle) == (404, "No existe FARO-9") and esperas == []


def test_ej2_actualizar_estado():
    def manejador(peticion):
        assert peticion.method == "PATCH" and json.loads(peticion.content) == {"estado": "En curso"}
        return httpx.Response(200, json={"id": "FARO-142", "estado": "En curso"})

    cliente, _ = cliente_con(manejador)
    assert cliente.actualizar_estado("FARO-142", "En curso")["estado"] == "En curso"


# ---------------------------------------------------------------- Ejercicio 3
HISTORIAS = [{"id": "FARO-142", "titulo": "Aviso", "estado": "Por hacer", "puntos": 5, "sprint": 23, "responsable": "Marta Ríos"}]


def api_falsa(peticion):
    if peticion.url.path == "/salud":
        return httpx.Response(200, json={"estado": "ok"})
    if peticion.url.path == "/historias":
        return httpx.Response(200, json=HISTORIAS)
    if peticion.url.path == "/historias/FARO-142":
        return httpx.Response(200, json=HISTORIAS[0])
    return httpx.Response(404, json={"error": "No existe"})


def test_ej3_registro_con_dos_herramientas():
    cliente, _ = cliente_con(api_falsa)
    r = ej3.crear_registro(cliente)
    assert {e["function"]["name"] for e in r.esquemas()} == {"listar_historias", "consultar_historia"}
    assert r.con_efectos() == set()
    assert r.ejecutar("listar_historias", '{"sprint": 23}').datos == [{"id": "FARO-142", "titulo": "Aviso", "estado": "Por hacer", "puntos": 5}]
    assert "pattern" in r.ejecutar("consultar_historia", '{"identificador": "142"}').error or "match" in r.ejecutar("consultar_historia", '{"identificador": "142"}').error
    assert r.ejecutar("consultar_historia", '{"identificador": "FARO-999"}').error.startswith("ErrorAPI")


def test_ej3_responde_con_el_agente():
    cliente, _ = cliente_con(api_falsa)
    falso = llm.usar_llm_falso([{"herramienta": "consultar_historia", "argumentos": {"identificador": "FARO-142"}},
                                "FARO-142 está Por hacer y la lleva Marta Ríos."])
    assert ej3.responder("¿Cómo va FARO-142?", cliente) == "FARO-142 está Por hacer y la lleva Marta Ríos."
    assert '"ok": true' in falso.recibidos[1][-1]["content"]


def test_ej3_modo_degradado_sin_llamar_al_modelo():
    cliente, _ = cliente_con(lambda p: httpx.Response(503, json={"error": "caído"}), reintentos=1)
    falso = llm.usar_llm_falso(["no debería usarse"])
    assert ej3.responder("¿Cómo va el sprint?", cliente) == ej3.MENSAJE_DEGRADADO
    assert falso.recibidos == []
