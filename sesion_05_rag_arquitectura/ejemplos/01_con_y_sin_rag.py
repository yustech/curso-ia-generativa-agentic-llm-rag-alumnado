"""Ejemplo 1: la misma pregunta sin RAG y con RAG (buscador de referencia de comun/).

    python sesion_05_rag_arquitectura/ejemplos/01_con_y_sin_rag.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402
from comun.buscador import BuscadorSemantico, contexto_numerado  # noqa: E402

SISTEMA_RAG = ("Responde SOLO con la información de los fragmentos y cita cada dato con [n]. "
               "Si no está, responde «No consta en la documentación».")
buscador = BuscadorSemantico.de_documentos()

for pregunta in ["¿Con cuánta antelación tengo que pedir las vacaciones?",
                 "¿Qué tipos de instancia puedo usar en la nube?",
                 "¿Cuál es el presupuesto anual de Tecnología?"]:
    print(f"\n### {pregunta}")
    print("Sin RAG:", llm.chat(pregunta, temperatura=0)[:300])
    resultados = buscador.buscar(pregunta, k=3)
    print("Fragmentos:", [t.referencia for t, _ in resultados])
    print("Con RAG:", llm.chat(f"{contexto_numerado(resultados)}\n\nPregunta: {pregunta}", sistema=SISTEMA_RAG, temperatura=0))
