"""Configuración común de los tests del curso.

Por defecto los tests importan el código de la carpeta ``ejercicios`` de cada
sesión, es decir, tu trabajo. Si existe la variable de entorno
``CURSO_SOLUCIONES`` (uso del profesor), se importan las soluciones de esa
carpeta en su lugar: ``CURSO_SOLUCIONES=.`` en el repositorio docente.

Los tests no necesitan ningún modelo: usan un LLM falso y determinista
(``comun.llm.LLMFalso``). Así comprueban tu lógica (similitudes, troceado,
validación, bucles de agente) sin depender de la velocidad ni del azar del
modelo. Para lanzar además las pruebas que llaman al modelo real, define
``CURSO_LLM_REAL=1``.
"""

import os
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).parent
CARPETA_SOLUCIONES = os.environ.get("CURSO_SOLUCIONES")

sys.path.insert(0, str(RAIZ))
for sesion in sorted(RAIZ.glob("sesion_*")):
    if CARPETA_SOLUCIONES:
        origen = Path(CARPETA_SOLUCIONES).resolve() / sesion.name / "soluciones"
    else:
        origen = sesion / "ejercicios"
    if origen.is_dir():
        sys.path.insert(0, str(origen))


def pytest_configure(config):
    config.addinivalue_line("markers", "llm_real: prueba que llama al modelo real (requiere CURSO_LLM_REAL=1)")


def pytest_collection_modifyitems(config, items):
    if os.environ.get("CURSO_LLM_REAL"):
        return
    saltar = pytest.mark.skip(reason="Necesita el modelo real: define CURSO_LLM_REAL=1")
    for item in items:
        if "llm_real" in item.keywords:
            item.add_marker(saltar)


@pytest.fixture(autouse=True)
def _llm_falso_por_defecto(request):
    """Cada test empieza con el LLM falso activo (salvo los marcados como llm_real)."""
    from comun import llm

    if "llm_real" in request.keywords:
        llm.usar_llm_real()
    else:
        llm.usar_llm_falso()
    yield
    llm.usar_llm_real()
