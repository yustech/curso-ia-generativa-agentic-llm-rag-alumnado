"""Ejemplo 1: tool calling paso a paso, imprimiendo cada mensaje del intercambio.

    python sesion_07_indexacion_agentes/ejemplos/01_tool_calling_paso_a_paso.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402

HERRAMIENTA = {"type": "function", "function": {
    "name": "coste_modulo", "description": "Coste mensual estimado en euros de un tipo de instancia de Atlántica.",
    "parameters": {"type": "object", "properties": {"tipo": {"type": "string"}}, "required": ["tipo"]}}}
COSTES = {"t3.micro": 9, "t3.small": 18, "t3.medium": 36, "m6i.large": 85, "m6i.xlarge": 170}

mensajes = [{"role": "user", "content": "¿Cuánto cuesta al mes una máquina m6i.large?"}]
print("1. USUARIO:", mensajes[0]["content"])

r = llm.chat_completo(mensajes, herramientas=[HERRAMIENTA], temperatura=0).choices[0].message
llamada = r.tool_calls[0]
print("2. MODELO pide herramienta:", llamada.function.name, llamada.function.arguments)

argumentos = json.loads(llamada.function.arguments)
resultado = json.dumps({"tipo": argumentos["tipo"], "euros_mes": COSTES.get(argumentos["tipo"])})
print("3. PROGRAMA ejecuta y devuelve:", resultado)

mensajes += [r.model_dump(exclude_none=True), {"role": "tool", "tool_call_id": llamada.id, "content": resultado}]
final = llm.chat_completo(mensajes, herramientas=[HERRAMIENTA], temperatura=0).choices[0].message
print("4. MODELO responde:", final.content)
