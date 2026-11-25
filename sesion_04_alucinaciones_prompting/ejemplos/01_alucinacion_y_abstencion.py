"""Ejemplo 1: la misma pregunta sin contexto, con permiso para abstenerse y con el documento.

    python sesion_04_alucinaciones_prompting/ejemplos/01_alucinacion_y_abstencion.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402

PREGUNTA = "¿Cuántos días de vacaciones tiene la plantilla de Atlántica Logística y cómo se piden?"
DOCUMENTO = (Path(__file__).resolve().parents[2] / "datos" / "atlantica" / "documentos"
             / "11_politica_vacaciones_teletrabajo.md").read_text(encoding="utf-8")

print("1) Sin nada:\n", llm.chat(PREGUNTA, temperatura=0), "\n")
print("2) Permitiendo abstenerse:\n", llm.chat(
    PREGUNTA, temperatura=0, sistema="Si no conoces el dato con seguridad, responde «No lo sé»."), "\n")
print("3) Con el documento en el contexto:\n", llm.chat(
    f"<documento>\n{DOCUMENTO}\n</documento>\n\n{PREGUNTA}", temperatura=0,
    sistema="Responde solo con la información del documento y cita la sección."))
