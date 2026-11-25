"""Ejemplo 4: salida estructurada con JSON Schema y Pydantic.

    python sesion_04_alucinaciones_prompting/ejemplos/04_json_schema.py
"""

import json
import sys
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402


class Peticion(BaseModel):
    proyecto: str
    entorno: Literal["dev", "pre", "pro"]
    centro_coste: str | None = Field(description="Código de 4 cifras o null si no aparece")
    recursos: list[str]


print("Esquema que recibe el servidor:")
print(json.dumps(llm.esquema_de(Peticion), indent=2, ensure_ascii=False)[:600], "...\n")

texto = "Necesito un entorno de preproducción para faro con dos máquinas t3.medium y una base de datos."
peticion = llm.estructurado(texto, Peticion, sistema="Extrae los datos de la petición. Si un dato no aparece, usa null.")
print(peticion)
print("¿Falta el centro de coste?", peticion.centro_coste is None)
