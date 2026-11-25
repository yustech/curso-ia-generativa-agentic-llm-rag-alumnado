"""Ejemplo 3: el mismo código contra Ollama y contra LM Studio.

Requisitos: Ollama abierto y, en LM Studio, un modelo cargado y el servidor arrancado
(pestaña Developer > Start Server, puerto 1234).

    python sesion_02_ia_responsable_genai/ejemplos/03_cambiar_de_motor.py
"""

import time

from openai import OpenAI

MOTORES = {
    "Ollama": ("http://localhost:11434/v1", "ollama", "granite4:micro"),
    "LM Studio": ("http://localhost:1234/v1", "lm-studio", None),  # None: el modelo cargado
}

for nombre, (url, clave, modelo) in MOTORES.items():
    cliente = OpenAI(base_url=url, api_key=clave, timeout=60)
    try:
        modelo = modelo or cliente.models.list().data[0].id
        inicio = time.perf_counter()
        r = cliente.chat.completions.create(
            model=modelo, messages=[{"role": "user", "content": "Di una ventaja de ejecutar modelos en local."}],
            temperature=0,
        )
        print(f"[{nombre} · {modelo} · {time.perf_counter() - inicio:.1f} s]\n{r.choices[0].message.content}\n")
    except Exception as error:
        print(f"[{nombre}] no disponible: {type(error).__name__}. ¿Está arrancado el servidor?\n")
