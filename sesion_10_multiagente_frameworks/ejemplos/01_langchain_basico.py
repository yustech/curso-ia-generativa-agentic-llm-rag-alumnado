"""Ejemplo 1: LangChain contra Ollama. Modelo, mensajes, plantilla y herramientas.

    python sesion_10_multiagente_frameworks/ejemplos/01_langchain_basico.py
"""

import sys
from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402

modelo = ChatOpenAI(model=llm.MODELO_CHAT, base_url=llm.URL_BASE, api_key=llm.CLAVE_API, temperature=0)

# 1. Mensajes
print(modelo.invoke([SystemMessage("Responde en una frase."), HumanMessage("¿Qué es un TMS?")]).content, "\n")

# 2. Plantilla + modelo encadenados con el operador |
plantilla = ChatPromptTemplate.from_messages([("system", "Eres el asistente de {empresa}."), ("human", "{pregunta}")])
cadena = plantilla | modelo
print(cadena.invoke({"empresa": "Atlántica Logística", "pregunta": "Saluda en una frase."}).content, "\n")


# 3. Herramientas: el decorador @tool genera el esquema a partir de la firma y el docstring
@tool
def coste_instancia(tipo: str) -> int:
    """Coste mensual en euros de un tipo de instancia del catálogo de Atlántica."""
    return {"t3.micro": 9, "t3.small": 18, "t3.medium": 36, "m6i.large": 85, "m6i.xlarge": 170}.get(tipo, -1)


con_herramientas = modelo.bind_tools([coste_instancia])
mensajes = [HumanMessage("¿Cuánto cuesta al mes una m6i.large?")]
respuesta = con_herramientas.invoke(mensajes)
print("Llamadas a herramientas:", respuesta.tool_calls)
mensajes.append(respuesta)
for llamada in respuesta.tool_calls:
    mensajes.append(ToolMessage(str(coste_instancia.invoke(llamada["args"])), tool_call_id=llamada["id"]))
print("Respuesta final:", con_herramientas.invoke(mensajes).content)
