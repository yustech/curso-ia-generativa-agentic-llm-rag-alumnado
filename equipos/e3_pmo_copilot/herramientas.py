"""Herramientas del reto R3 · PMO Copilot (sistemas simulados de Atlántica).

Simulan la herramienta de seguimiento de proyectos (backlog) y el repositorio
de actas. El backlog de trabajo es una copia en ``salidas/`` para que los
cambios no toquen los datos originales del curso.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any

RAIZ = Path(__file__).resolve().parents[2]
ORIGEN = RAIZ / "datos" / "atlantica" / "proyectos" / "backlog.json"
CARPETA_ACTAS = RAIZ / "datos" / "atlantica" / "proyectos" / "actas"
ESTADOS = ("Por hacer", "En curso", "En revisión", "Hecho")
PUNTOS_VALIDOS = (1, 2, 3, 5, 8, 13)
FORMATO_HISTORIA = re.compile(r"^Como .+ quiero .+ para .+", re.IGNORECASE)


class Backlog:
    """Backlog de trabajo persistido en JSON."""

    def __init__(self, ruta: Path | str = RAIZ / "salidas" / "backlog_trabajo.json", reiniciar: bool = False) -> None:
        self.ruta = Path(ruta)
        if reiniciar or not self.ruta.exists():
            self.ruta.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(ORIGEN, self.ruta)

    def _leer(self) -> list[dict[str, Any]]:
        return json.loads(self.ruta.read_text(encoding="utf-8"))

    def _guardar(self, elementos: list[dict[str, Any]]) -> None:
        self.ruta.write_text(json.dumps(elementos, ensure_ascii=False, indent=2), encoding="utf-8")

    def listar(self, estado: str | None = None, sprint: int | None = None) -> list[dict[str, Any]]:
        return [e for e in self._leer() if (estado is None or e["estado"] == estado) and (sprint is None or e["sprint"] == sprint)]

    def obtener(self, identificador: str) -> dict[str, Any]:
        for e in self._leer():
            if e["id"] == identificador:
                return e
        raise KeyError(f"No existe {identificador}")

    def actualizar_estado(self, identificador: str, estado: str) -> dict[str, Any]:
        """Cambia el estado de un elemento. Es una acción CON EFECTOS: exige confirmación humana."""
        if estado not in ESTADOS:
            raise ValueError(f"Estado no válido: {estado} ({', '.join(ESTADOS)})")
        elementos = self._leer()
        for e in elementos:
            if e["id"] == identificador:
                e["estado"] = estado
                self._guardar(elementos)
                return e
        raise KeyError(f"No existe {identificador}")

    def crear_historia(self, titulo: str, criterios: list[str], puntos: int, prioridad: str = "Media",
                       sprint: int | None = None) -> dict[str, Any]:
        """Crea una historia validando la definición de preparado. Acción CON EFECTOS."""
        problemas = problemas_preparacion({"titulo": titulo, "criterios": criterios, "puntos": puntos})
        if problemas:
            raise ValueError("La historia no cumple la definición de preparado: " + "; ".join(problemas))
        elementos = self._leer()
        numero = max(int(e["id"].split("-")[1]) for e in elementos) + 1
        historia = {"id": f"FARO-{numero}", "tipo": "historia", "titulo": titulo, "estado": "Por hacer", "prioridad": prioridad,
                    "puntos": puntos, "sprint": sprint, "responsable": None, "criterios": criterios}
        elementos.append(historia)
        self._guardar(elementos)
        return historia

    def metricas_sprint(self, sprint: int) -> dict[str, Any]:
        elementos = self.listar(sprint=sprint)
        comprometidos = sum(e["puntos"] or 0 for e in elementos)
        completados = sum(e["puntos"] or 0 for e in elementos if e["estado"] == "Hecho")
        return {"sprint": sprint, "elementos": len(elementos), "comprometidos": comprometidos, "completados": completados,
                "porcentaje": round(100 * completados / comprometidos, 1) if comprometidos else 0.0}


def problemas_preparacion(historia: dict[str, Any]) -> list[str]:
    """Incumplimientos de la definición de preparado (ATL-PMO-009) de una historia."""
    problemas = []
    if not FORMATO_HISTORIA.match(historia.get("titulo") or ""):
        problemas.append("El título no sigue «Como <rol> quiero <objetivo> para <beneficio>»")
    if len(historia.get("criterios") or []) < 2:
        problemas.append("Necesita al menos dos criterios de aceptación")
    if historia.get("puntos") not in PUNTOS_VALIDOS:
        problemas.append("La estimación debe ser 1, 2, 3, 5, 8 o 13 puntos")
    return problemas


def historias_no_preparadas(backlog: Backlog) -> list[dict[str, Any]]:
    """Historias del backlog que no están hechas y no cumplen la definición de preparado."""
    return [{"id": e["id"], "titulo": e["titulo"], "problemas": problemas_preparacion(e)}
            for e in backlog.listar() if e["tipo"] == "historia" and e["estado"] != "Hecho" and problemas_preparacion(e)]


def listar_actas() -> list[str]:
    return sorted(p.name for p in CARPETA_ACTAS.glob("*.md"))


def leer_acta(nombre: str) -> str:
    ruta = (CARPETA_ACTAS / nombre).resolve()
    if ruta.parent != CARPETA_ACTAS.resolve() or not ruta.exists():
        raise FileNotFoundError(f"No existe el acta {nombre}")
    return ruta.read_text(encoding="utf-8")


def exposicion_riesgo(probabilidad: int, impacto: int) -> dict[str, Any]:
    """Exposición = P × I y si hay que escalarlo a dirección (≥ 15)."""
    if not (1 <= probabilidad <= 5 and 1 <= impacto <= 5):
        raise ValueError("Probabilidad e impacto van de 1 a 5")
    exposicion = probabilidad * impacto
    return {"exposicion": exposicion, "escalar": exposicion >= 15}


def semaforo(desviacion_porcentaje: float, hito_critico_en_peligro: bool = False) -> str:
    """Color del semáforo de la metodología (verde ≤ 5 %, ámbar ≤ 15 %, rojo > 15 % o hito crítico en peligro)."""
    if hito_critico_en_peligro or desviacion_porcentaje > 15:
        return "Rojo"
    return "Ámbar" if desviacion_porcentaje > 5 else "Verde"


HERRAMIENTAS_SOLO_LECTURA = {"listar", "obtener", "metricas_sprint", "historias_no_preparadas", "listar_actas",
                             "leer_acta", "exposicion_riesgo", "semaforo"}
HERRAMIENTAS_CON_EFECTOS = {"actualizar_estado", "crear_historia"}
