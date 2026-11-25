"""Ejemplo 2: generar docstrings para el código heredado y validar que el resultado sigue siendo Python.

    python sesion_12_documentacion/ejemplos/02_docstrings.py
"""

import ast
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import DATOS, llm  # noqa: E402

codigo = (DATOS / "codigo" / "tarifas" / "calculo.py").read_text(encoding="utf-8")
arbol = ast.parse(codigo)
for funcion in [n for n in arbol.body if isinstance(n, ast.FunctionDef)]:
    fuente = ast.get_source_segment(codigo, funcion)
    docstring = llm.chat(f"```python\n{fuente}\n```", temperatura=0, sistema=(
        "Escribe SOLO el docstring (sin comillas triples ni código) en español con estilo Google para esta función: "
        "una línea de resumen, Args y Returns. Describe lo que hace el código, no lo que debería hacer."))
    propuesta = f'def f():\n    """{docstring.strip()}"""\n'
    valido = True
    try:
        ast.parse(propuesta)
    except SyntaxError:
        valido = False
    print(f"\n### {funcion.name} (¿Python válido? {valido})\n{docstring.strip()}")
