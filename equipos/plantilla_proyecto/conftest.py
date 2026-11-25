"""Hace importables los módulos del proyecto y del curso en las pruebas y activa el LLM falso."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import entorno  # noqa: E402,F401


@pytest.fixture(autouse=True)
def _llm_falso():
    from comun import llm

    llm.usar_llm_falso()
    yield
    llm.usar_llm_real()
