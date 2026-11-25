"""Herramientas del reto R1 · DevAssist (sistemas simulados de Atlántica).

Dan acceso de SOLO LECTURA al código de ``datos/atlantica/codigo`` y permiten
ejecutar pruebas en un directorio temporal aislado.
"""

from __future__ import annotations

import ast
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

RAIZ = Path(__file__).resolve().parents[2]
CARPETA_CODIGO = RAIZ / "datos" / "atlantica" / "codigo"


def _ruta_segura(ruta: str) -> Path:
    destino = (CARPETA_CODIGO / ruta).resolve()
    if CARPETA_CODIGO.resolve() not in destino.parents and destino != CARPETA_CODIGO.resolve():
        raise PermissionError(f"Acceso denegado fuera del repositorio: {ruta}")
    return destino


def listar_ficheros() -> list[str]:
    """Ficheros Python del repositorio, con rutas relativas."""
    return sorted(str(p.relative_to(CARPETA_CODIGO)).replace("\\", "/") for p in CARPETA_CODIGO.rglob("*.py"))


def leer_fichero(ruta: str) -> str:
    """Contenido de un fichero del repositorio (solo dentro de ``datos/atlantica/codigo``)."""
    destino = _ruta_segura(ruta)
    if not destino.is_file():
        raise FileNotFoundError(f"No existe {ruta}")
    return destino.read_text(encoding="utf-8")


def comprobar_estilo(codigo: str) -> list[dict[str, Any]]:
    """Comprobaciones deterministas de la guía de estilo ATL-DES-004 sobre un fragmento de código."""
    problemas: list[dict[str, Any]] = []
    try:
        arbol = ast.parse(codigo)
    except SyntaxError as error:
        return [{"linea": error.lineno, "regla": "sintaxis", "detalle": str(error)}]
    for numero, linea in enumerate(codigo.splitlines(), 1):
        if len(linea) > 100:
            problemas.append({"linea": numero, "regla": "longitud", "detalle": f"{len(linea)} caracteres (máximo 100)"})
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.ImportFrom) and any(a.name == "*" for a in nodo.names):
            problemas.append({"linea": nodo.lineno, "regla": "import_asterisco", "detalle": f"from {nodo.module} import *"})
        if isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name) and nodo.func.id == "print":
            problemas.append({"linea": nodo.lineno, "regla": "print", "detalle": "Usa logging en lugar de print"})
        if isinstance(nodo, ast.ExceptHandler) and nodo.type is None:
            problemas.append({"linea": nodo.lineno, "regla": "except_generico", "detalle": "except sin tipo"})
        if isinstance(nodo, ast.Compare) and any(isinstance(c, ast.Constant) and c.value in (True, False, None)
                                                 for c in nodo.comparators) and any(isinstance(o, (ast.Eq, ast.NotEq)) for o in nodo.ops):
            problemas.append({"linea": nodo.lineno, "regla": "comparacion_constante", "detalle": "Usa «is» / «is not» o la condición directa"})
        if isinstance(nodo, ast.FunctionDef) and not nodo.name.startswith("_"):
            if ast.get_docstring(nodo) is None:
                problemas.append({"linea": nodo.lineno, "regla": "docstring", "detalle": f"{nodo.name} sin docstring"})
            sin_tipo = [a.arg for a in nodo.args.args if a.annotation is None]
            if sin_tipo or nodo.returns is None:
                problemas.append({"linea": nodo.lineno, "regla": "tipos", "detalle": f"{nodo.name}: faltan anotaciones de tipo"})
        if isinstance(nodo, ast.Constant) and isinstance(nodo.value, float):
            problemas.append({"linea": nodo.lineno, "regla": "float_importe", "detalle": f"Literal float {nodo.value}: revisa si es un importe (usa Decimal)"})
    return sorted(problemas, key=lambda p: (p["linea"], p["regla"]))


def ejecutar_pruebas(codigo_pruebas: str, tiempo_maximo: int = 60) -> dict[str, Any]:
    """Ejecuta un fichero de pruebas pytest contra una COPIA del repositorio en un directorio temporal.

    Devuelve ``{"exito": bool, "resumen": última línea de pytest, "salida": texto recortado}``.
    """
    with tempfile.TemporaryDirectory() as temporal:
        copia = Path(temporal) / "repo"
        shutil.copytree(CARPETA_CODIGO, copia)
        (copia / "test_generado.py").write_text(codigo_pruebas, encoding="utf-8")
        proceso = subprocess.run([sys.executable, "-m", "pytest", "-q", "test_generado.py", "-p", "no:cacheprovider"],
                                 cwd=copia, capture_output=True, text=True, timeout=tiempo_maximo)
    salida = (proceso.stdout + proceso.stderr).strip()
    lineas = [l for l in salida.splitlines() if l.strip()]
    return {"exito": proceso.returncode == 0, "resumen": lineas[-1] if lineas else "", "salida": salida[-2000:]}


def calcular_tarifa(tipo: str, km: float, kg: float, cliente: str | None = None, urgente: bool = False) -> float | None:
    """Ejecuta el cálculo de tarifas actual (código heredado) para comprobar comportamientos."""
    sys.path.insert(0, str(CARPETA_CODIGO))
    try:
        from tarifas.calculo import calc

        return calc(tipo, km, kg, cliente, urgente)
    finally:
        sys.path.remove(str(CARPETA_CODIGO))


HERRAMIENTAS_SOLO_LECTURA = {"listar_ficheros", "leer_fichero", "comprobar_estilo", "ejecutar_pruebas", "calcular_tarifa"}
HERRAMIENTAS_CON_EFECTOS: set[str] = set()
