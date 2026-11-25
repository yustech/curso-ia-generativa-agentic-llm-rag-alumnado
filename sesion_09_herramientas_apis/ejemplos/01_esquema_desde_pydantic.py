"""Ejemplo 1: del modelo Pydantic al esquema que ve el LLM, y validación de lo que propone.

    python sesion_09_herramientas_apis/ejemplos/01_esquema_desde_pydantic.py
"""

import json
from typing import Literal

from pydantic import BaseModel, Field, ValidationError


class ArgsListar(BaseModel):
    estado: Literal["Por hacer", "En curso", "En revisión", "Hecho"] | None = Field(default=None, description="Filtrar por estado")
    sprint: int | None = Field(default=None, ge=1, description="Número de sprint, por ejemplo 23")


print("Esquema que recibe el modelo:")
print(json.dumps(ArgsListar.model_json_schema(), indent=2, ensure_ascii=False))

for propuesta in ['{"sprint": 23}', '{"estado": "Terminado"}', '{"sprint": 0}', '{"sprint": "veintitrés"}']:
    try:
        print(f"\n{propuesta} → válido: {ArgsListar.model_validate_json(propuesta).model_dump()}")
    except ValidationError as error:
        print(f"\n{propuesta} → NO válido:")
        for e in error.errors():
            print(f"   {'.'.join(map(str, e['loc']))}: {e['msg']}")
