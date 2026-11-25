"""Tests del ejercicio de la sesión 14."""

import json

import s14_ej1_verificar_entrega as ej1


def crear_repositorio(raiz, casos=30, pruebas=10, tipos=None, secreto=False, env=False):
    for relativo in ej1.DOCUMENTOS:
        ruta = raiz / relativo
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text("# Documento\n\n" + "Contenido del documento. " * 20, encoding="utf-8")
    tipos = tipos or sorted(ej1.TIPOS_GOLDEN)
    (raiz / "evals").mkdir()
    lineas = [json.dumps({"id": f"C{i}", "entrada": "e", "esperado": "x", "tipo": tipos[i % len(tipos)]}) for i in range(casos)]
    (raiz / "evals" / "golden_set.jsonl").write_text("\n".join(lineas + ["no json", "{}"]), encoding="utf-8")
    (raiz / "tests").mkdir()
    (raiz / "tests" / "test_a.py").write_text("\n".join(f"def test_{i}():\n    assert True\n" for i in range(pruebas)) + "\ndef ayuda():\n    pass\n", encoding="utf-8")
    (raiz / "app.py").write_text("import streamlit\n", encoding="utf-8")
    (raiz / "requirements.txt").write_text("openai\n", encoding="utf-8")
    (raiz / "rag").mkdir()
    if secreto:
        (raiz / "rag" / "config.py").write_text('api_key = "abcdefghijk123"\n', encoding="utf-8")
    if env:
        (raiz / ".env").write_text("LLM_API_KEY=x\n", encoding="utf-8")
    return raiz


def test_entrega_completa(tmp_path):
    filas = ej1.verificar(crear_repositorio(tmp_path))
    assert all(f["ok"] for f in filas), [f for f in filas if not f["ok"]]
    assert ej1.informe(filas).endswith("Entrega completa: sí")
    assert {f["comprobacion"] for f in filas} >= {"conjunto dorado", "pruebas automáticas", "sin secretos", "existe app.py"}


def test_documento_corto_o_ausente(tmp_path):
    crear_repositorio(tmp_path)
    (tmp_path / "docs" / "canvas_caso_uso.md").write_text("corto", encoding="utf-8")
    (tmp_path / "docs" / "plan_validacion.md").unlink()
    filas = {f["comprobacion"]: f for f in ej1.comprobar_documentos(tmp_path)}
    assert not filas["documento docs/canvas_caso_uso.md"]["ok"] and filas["documento docs/canvas_caso_uso.md"]["detalle"] == "5 caracteres"
    assert filas["documento docs/plan_validacion.md"]["detalle"] == "no existe"


def test_golden_insuficiente_y_tipos(tmp_path):
    crear_repositorio(tmp_path, casos=12, tipos=["normativa", "tarea"])
    r = ej1.comprobar_golden(tmp_path)
    assert not r["ok"] and r["detalle"] == "12 casos válidos; faltan tipos: ambigua, fuera_de_alcance, seguridad"


def test_pruebas_y_secretos(tmp_path):
    crear_repositorio(tmp_path, pruebas=4, secreto=True, env=True)
    assert ej1.contar_pruebas(tmp_path) == {"comprobacion": "pruebas automáticas", "ok": False, "detalle": "4 pruebas"}
    assert ej1.buscar_secretos(tmp_path) == {"comprobacion": "sin secretos", "ok": False, "detalle": ".env, rag/config.py"}


def test_informe_pendientes(tmp_path):
    filas = ej1.verificar(tmp_path)  # repositorio vacío
    texto = ej1.informe(filas)
    assert texto.splitlines()[0] == "| Comprobación | Resultado | Detalle |"
    assert texto.endswith(f"Entrega completa: no ({sum(1 for f in filas if not f['ok'])} pendientes)")
