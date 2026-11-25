"""Tests de las herramientas de los tres retos (sistemas simulados de Atlántica)."""

import pytest

from equipos.e1_devassist import herramientas as dev
from equipos.e2_infrapilot import herramientas as infra
from equipos.e3_pmo_copilot import herramientas as pmo


# ---------------------------------------------------------------- R1 · DevAssist
def test_dev_listar_y_leer():
    assert "tarifas/calculo.py" in dev.listar_ficheros()
    assert "def calc(" in dev.leer_fichero("tarifas/calculo.py")


def test_dev_no_sale_del_repositorio():
    with pytest.raises(PermissionError):
        dev.leer_fichero("../../../.env")


def test_dev_comprobar_estilo_del_codigo_heredado():
    reglas = {p["regla"] for p in dev.comprobar_estilo(dev.leer_fichero("tarifas/calculo.py"))}
    assert {"import_asterisco", "print", "comparacion_constante", "docstring", "tipos", "float_importe"} <= reglas


def test_dev_comprobar_estilo_codigo_correcto():
    codigo = 'from decimal import Decimal\n\n\ndef doble(x: Decimal) -> Decimal:\n    """Dobla."""\n    return x * 2\n'
    assert dev.comprobar_estilo(codigo) == []


def test_dev_ejecutar_pruebas():
    bien = "from tarifas.calculo import calc\n\ndef test_minimo():\n    assert calc('furgoneta', 10, 100) == 48.38\n"
    mal = "from tarifas.calculo import calc\n\ndef test_falla():\n    assert calc('furgoneta', 10, 100) == 1\n"
    assert dev.ejecutar_pruebas(bien)["exito"] is True
    resultado = dev.ejecutar_pruebas(mal)
    assert resultado["exito"] is False and "failed" in resultado["resumen"]


def test_dev_calcular_tarifa():
    assert dev.calcular_tarifa("rigido", 120, 1500, "Nortia", urgente=True) == 149.0


# ---------------------------------------------------------------- R2 · InfraPilot
PETICION = {"proyecto": "faro", "entorno": "pre", "etiquetas": {"proyecto": "faro", "entorno": "pre", "centro_coste": "4120",
                                                                 "responsable": "ivan.seoane@atlantica.example"},
            "recursos": [{"modulo": "red_base"}, {"modulo": "vm_linux", "tipo_instancia": "t3.medium"},
                         {"modulo": "vm_linux", "tipo_instancia": "t3.medium"},
                         {"modulo": "postgres_gestionado", "clase": "db.t3.medium", "multi_az": False, "dias_copia": 7}]}


def test_infra_peticion_valida():
    r = infra.validar_peticion(PETICION)
    assert r["conforme"] and r["coste"]["total"] == 177 and not r["requiere_cab"] and r["avisos"] == []


def test_infra_incumplimientos():
    mala = {"proyecto": "faro", "entorno": "pro", "region": "us-east-1", "etiquetas": {"proyecto": "faro"},
            "recursos": [{"modulo": "bucket_privado", "publico": True}, {"modulo": "vm_linux", "tipo_instancia": "g5.xlarge"},
                         {"modulo": "postgres_gestionado", "clase": "db.t3.medium", "multi_az": False, "dias_copia": 7}]}
    r = infra.validar_peticion(mala)
    texto = " | ".join(r["incumplimientos"])
    assert not r["conforme"] and r["requiere_cab"]
    for fragmento in ["Región no permitida", "Faltan etiquetas", "acceso público", "g5.xlarge", "Multi-AZ", "deben ser 30"]:
        assert fragmento in texto


def test_infra_aviso_de_coste():
    cara = dict(PETICION, recursos=[{"modulo": "cluster_k8s", "nodos": 5, "tipo_nodo": "m6i.xlarge"}])
    r = infra.validar_peticion(cara)
    assert r["conforme"] and any("supera el límite de 800" in a for a in r["avisos"])
    assert r["coste"]["total"] == 75 + 5 * 170


def test_infra_terraform_y_catalogo():
    hcl = infra.generar_terraform(PETICION)
    assert hcl.count("module ") == 4 and "postgres_gestionado?ref=v3.1.0" in hcl and 'centro_coste = "4120"' in hcl
    with pytest.raises(KeyError):
        infra.consultar_catalogo("lambda")


def test_infra_solicitud_cambio(tmp_path, monkeypatch):
    monkeypatch.setattr(infra, "REGISTRO_CAMBIOS", tmp_path / "cambios.jsonl")
    with pytest.raises(ValueError):
        infra.registrar_solicitud_cambio("x", "hcl", "  ", "yo")
    assert infra.registrar_solicitud_cambio("x", "hcl", "terraform destroy", "yo") == {"id": "CHG-1001", "estado": "pendiente_aprobacion"}
    assert infra.registrar_solicitud_cambio("y", "hcl", "revertir", "yo")["id"] == "CHG-1002"


# ---------------------------------------------------------------- R3 · PMO Copilot
@pytest.fixture
def backlog(tmp_path):
    return pmo.Backlog(tmp_path / "backlog.json", reiniciar=True)


def test_pmo_listar_y_metricas(backlog):
    assert len(backlog.listar()) == 13
    assert {e["id"] for e in backlog.listar(sprint=23)} == {"FARO-142", "FARO-147", "FARO-148", "FARO-149"}
    assert backlog.metricas_sprint(22) == {"sprint": 22, "elementos": 4, "comprometidos": 18, "completados": 3, "porcentaje": 16.7}


def test_pmo_no_preparadas(backlog):
    ids = {h["id"] for h in pmo.historias_no_preparadas(backlog)}
    assert {"FARO-145", "FARO-146", "FARO-138"} <= ids


def test_pmo_actualizar_y_crear(backlog):
    assert backlog.actualizar_estado("FARO-142", "En curso")["estado"] == "En curso"
    with pytest.raises(ValueError):
        backlog.actualizar_estado("FARO-142", "Terminado")
    with pytest.raises(ValueError):
        backlog.crear_historia("Login", ["a"], 4)
    nueva = backlog.crear_historia("Como tienda quiero descargar el albarán para archivarlo", ["Dado... cuando... entonces...", "Dado..."], 3)
    assert nueva["id"] == "FARO-150" and backlog.obtener("FARO-150")["puntos"] == 3


def test_pmo_actas_riesgos_semaforo():
    assert len(pmo.listar_actas()) == 4 and "Nortia" in pmo.leer_acta("2026-11-03_seguimiento_faro2.md")
    with pytest.raises(FileNotFoundError):
        pmo.leer_acta("../backlog.json")
    assert pmo.exposicion_riesgo(4, 4) == {"exposicion": 16, "escalar": True}
    assert [pmo.semaforo(3), pmo.semaforo(8), pmo.semaforo(20), pmo.semaforo(2, True)] == ["Verde", "Ámbar", "Rojo", "Rojo"]
