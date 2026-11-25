"""Evaluación de extremo a extremo del asistente con el conjunto dorado.

    python -m evals.evaluar                 # evalúa y compara con la línea base
    python -m evals.evaluar --linea-base    # guarda el resultado como nueva línea base
    python -m evals.evaluar --solo E1-01 E1-05

Métricas deterministas (sin juez): cita la fuente esperada, se abstiene cuando
debe, no ejecuta acciones no autorizadas. El juez LLM y la revisión manual se
añaden en la sesión 13 (ejercicio 1).
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import entorno
from agente.asistente import responder

CARPETA = Path(__file__).parent
GOLDEN = CARPETA / "golden_set.jsonl"
LINEA_BASE = entorno.CARPETA_SALIDAS / "linea_base.json"
FRASES_ABSTENCION = ("no lo encuentro", "no encuentro", "no dispongo", "no tengo información", "no puedo")


def cargar(ruta: Path = GOLDEN) -> list[dict]:
    return [json.loads(l) for l in ruta.read_text(encoding="utf-8").splitlines() if l.strip()]


def evaluar_caso(caso: dict) -> dict:
    inicio = time.perf_counter()
    resultado = responder(caso["entrada"])
    respuesta = resultado.respuesta.lower()
    abstiene = any(f in respuesta for f in FRASES_ABSTENCION) or resultado.motivo == "guardarrail_entrada"
    fila = {"id": caso["id"], "tipo": caso.get("tipo", ""), "segundos": round(time.perf_counter() - inicio, 2),
            "herramientas": [p["herramienta"] for p in resultado.pasos], "respuesta": resultado.respuesta}
    if caso.get("tipo") in ("fuera_de_alcance", "seguridad"):
        fila["correcto"] = abstiene
    else:
        fuente = caso.get("debe_citar")
        fila["correcto"] = (not abstiene) and (not fuente or fuente.lower() in respuesta)
    return fila


def resumen(filas: list[dict]) -> dict:
    por_tipo: dict[str, list[bool]] = {}
    for f in filas:
        por_tipo.setdefault(f["tipo"], []).append(f["correcto"])
    tiempos = sorted(f["segundos"] for f in filas)
    return {
        "casos": len(filas),
        "exactitud": round(sum(f["correcto"] for f in filas) / max(len(filas), 1), 3),
        "por_tipo": {t: round(sum(v) / len(v), 3) for t, v in sorted(por_tipo.items())},
        "p50_s": tiempos[len(tiempos) // 2] if tiempos else 0,
        "p95_s": tiempos[min(len(tiempos) - 1, int(len(tiempos) * 0.95))] if tiempos else 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--linea-base", action="store_true")
    parser.add_argument("--solo", nargs="*")
    args = parser.parse_args()
    casos = [c for c in cargar() if not args.solo or c["id"] in args.solo]
    filas = []
    for caso in casos:
        fila = evaluar_caso(caso)
        filas.append(fila)
        print(f"{'OK ' if fila['correcto'] else 'MAL'} {fila['id']:<8} {fila['tipo']:<17} {fila['segundos']:>5.1f} s")
    datos = {"resumen": resumen(filas), "filas": filas}
    print(json.dumps(datos["resumen"], ensure_ascii=False, indent=2))
    entorno.CARPETA_SALIDAS.mkdir(exist_ok=True)
    salida = entorno.CARPETA_SALIDAS / f"evaluacion_{time.strftime('%Y%m%d_%H%M')}.json"
    salida.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.linea_base:
        LINEA_BASE.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Línea base guardada en {LINEA_BASE}")
    elif LINEA_BASE.exists():
        base = {f["id"]: f["correcto"] for f in json.loads(LINEA_BASE.read_text(encoding="utf-8"))["filas"]}
        regresiones = [f["id"] for f in filas if base.get(f["id"]) and not f["correcto"]]
        print("Regresiones:", ", ".join(regresiones) or "ninguna")


if __name__ == "__main__":
    main()
