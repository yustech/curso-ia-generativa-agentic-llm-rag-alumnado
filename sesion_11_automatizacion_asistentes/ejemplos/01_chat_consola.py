"""Ejemplo 1: el asistente de Atlántica en la consola (sin interfaz gráfica).

    python sesion_11_automatizacion_asistentes/ejemplos/01_chat_consola.py

Escribe «salir» para terminar y «reiniciar» para empezar de nuevo.
"""

import sys
from pathlib import Path

# Usa tu ejercicio; en el repositorio docente, si existe, la solución tiene prioridad.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ejercicios"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "soluciones"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from s11_ej2_asistente import asistente_atlantica  # noqa: E402

asistente = asistente_atlantica()
print(asistente.bienvenida(), "\n")
while (texto := input("Tú: ").strip()).lower() != "salir":
    if texto.lower() == "reiniciar":
        asistente.reiniciar()
        print("(conversación reiniciada)\n")
        continue
    r = asistente.responder(texto)
    print(f"\n{asistente.nombre}: {r.texto}")
    if r.fuentes:
        print("   Fuentes:", " · ".join(r.fuentes))
    print()
