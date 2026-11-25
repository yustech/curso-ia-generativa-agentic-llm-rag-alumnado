"""Comprueba que tu entorno está listo para el curso.

Ejecútalo desde la raíz del repositorio, con el entorno virtual activado:

    python comprobar_entorno.py

Cada línea termina en OK, AVISO o ERROR, con la indicación de cómo resolverlo.
"""

from __future__ import annotations

import importlib
import platform
import shutil
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))

PAQUETES = ["openai", "dotenv", "numpy", "pydantic", "pytest", "tiktoken", "chromadb", "rank_bm25", "mcp",
            "langchain_core", "langgraph", "llama_index.core", "streamlit"]
resultados: list[tuple[str, str, str]] = []


def anotar(estado: str, que: str, como: str = "") -> None:
    resultados.append((estado, que, como))
    marca = {"OK": "OK   ", "AVISO": "AVISO", "ERROR": "ERROR"}[estado]
    print(f"[{marca}] {que}" + (f"\n         -> {como}" if como else ""))


def memoria_gb() -> float | None:
    try:
        if platform.system() == "Windows":
            import ctypes

            class Estado(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("sullAvailExtendedVirtual", ctypes.c_ulonglong)]

            estado = Estado()
            estado.dwLength = ctypes.sizeof(Estado)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(estado))
            return estado.ullTotalPhys / 1024 ** 3
        import os

        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 1024 ** 3
    except Exception:
        return None


def main() -> int:
    print("Comprobación del entorno del curso\n")

    # 1. Python y entorno virtual
    version = sys.version_info
    if version >= (3, 11):
        anotar("OK", f"Python {platform.python_version()}")
    else:
        anotar("ERROR", f"Python {platform.python_version()}", "Instala Python 3.11 o superior (recomendado 3.12).")
    if sys.prefix != sys.base_prefix:
        anotar("OK", "Entorno virtual activo")
    else:
        anotar("AVISO", "No estás en un entorno virtual", "Actívalo: .venv\\Scripts\\Activate.ps1 (Windows) o source .venv/bin/activate")

    # 2. Memoria y disco
    ram = memoria_gb()
    if ram:
        anotar("OK" if ram >= 15 else "AVISO", f"Memoria RAM: {ram:.1f} GB",
               "" if ram >= 15 else "Con menos de 16 GB usa modelos de 1-3B y el servidor compartido.")
    libre = shutil.disk_usage(RAIZ).free / 1024 ** 3
    anotar("OK" if libre >= 30 else "AVISO", f"Disco libre: {libre:.0f} GB",
           "" if libre >= 30 else "Libera espacio: los modelos ocupan entre 2 y 5 GB cada uno.")

    # 3. Paquetes
    faltan = []
    for paquete in PAQUETES:
        try:
            importlib.import_module(paquete)
        except Exception:
            faltan.append(paquete)
    if faltan:
        anotar("ERROR", "Faltan paquetes: " + ", ".join(faltan), "pip install -r requirements.txt")
    else:
        anotar("OK", f"Paquetes de Python ({len(PAQUETES)})")

    # 4. Configuración y servidor
    if (RAIZ / ".env").exists():
        anotar("OK", "Fichero .env encontrado")
    else:
        anotar("AVISO", "No hay fichero .env (se usan los valores por defecto)", "Copia .env.example como .env")
    try:
        from comun import llm
    except Exception as error:
        anotar("ERROR", f"No se puede importar comun.llm: {error}", "Revisa la instalación de los paquetes.")
        return resumen()
    print("\n" + llm.describir_configuracion() + "\n")
    try:
        disponibles = llm.modelos_disponibles()
        anotar("OK", f"Servidor accesible ({len(disponibles)} modelos)")
    except Exception as error:
        anotar("ERROR", f"No se puede conectar con {llm.URL_BASE}: {type(error).__name__}",
               "Arranca Ollama (o el servidor de LM Studio) y comprueba LLM_BASE_URL en .env")
        return resumen()
    for nombre, modelo in (("chat", llm.MODELO_CHAT), ("embeddings", llm.MODELO_EMBEDDINGS)):
        if any(d == modelo or d.split(":")[0] == modelo.split(":")[0] for d in disponibles):
            anotar("OK", f"Modelo de {nombre} disponible: {modelo}")
        else:
            anotar("ERROR", f"Falta el modelo de {nombre}: {modelo}", f"ollama pull {modelo}")

    # 5. Llamadas reales
    try:
        inicio = time.perf_counter()
        texto = llm.chat("Responde únicamente con la palabra: listo", max_tokens=20, temperatura=0)
        anotar("OK", f"Chat responde en {time.perf_counter() - inicio:.1f} s: «{texto[:40]}»")
    except Exception as error:
        anotar("ERROR", f"Fallo al llamar al chat: {error}", "Prueba en una terminal: ollama run " + llm.MODELO_CHAT)
    try:
        vector = llm.embeddings("prueba")[0]
        anotar("OK", f"Embeddings funcionan (dimensión {len(vector)})")
    except Exception as error:
        anotar("ERROR", f"Fallo al calcular embeddings: {error}", f"ollama pull {llm.MODELO_EMBEDDINGS}")
    return resumen()


def resumen() -> int:
    errores = sum(1 for r in resultados if r[0] == "ERROR")
    avisos = sum(1 for r in resultados if r[0] == "AVISO")
    print(f"\nResultado: {errores} errores, {avisos} avisos.")
    print("Entorno listo para el curso." if not errores else "Corrige los errores antes de continuar.")
    return 1 if errores else 0


if __name__ == "__main__":
    raise SystemExit(main())
