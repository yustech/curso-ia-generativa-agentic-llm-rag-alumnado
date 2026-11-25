"""Carga y troceado de los documentos de Atlántica (versión de referencia).

En la sesión 5 programas tu propia versión de estas funciones. A partir de la
sesión 6 los laboratorios usan esta, para que nadie dependa de haber terminado
la anterior.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from comun import DATOS

CARPETA_DOCUMENTOS = DATOS / "documentos"


@dataclass
class Documento:
    nombre: str
    titulo: str
    texto: str
    metadatos: dict[str, str] = field(default_factory=dict)


@dataclass
class Trozo:
    id: str
    documento: str
    seccion: str
    texto: str
    metadatos: dict[str, str] = field(default_factory=dict)

    @property
    def referencia(self) -> str:
        return f"{self.documento} › {self.seccion}"


def leer_front_matter(texto: str) -> tuple[dict[str, str], str]:
    """Separa la cabecera ``---`` con pares ``clave: valor`` del cuerpo del documento."""
    if not texto.startswith("---"):
        return {}, texto
    fin = texto.find("\n---", 3)
    if fin < 0:
        return {}, texto
    metadatos = {}
    for linea in texto[3:fin].strip().splitlines():
        if ":" in linea:
            clave, valor = linea.split(":", 1)
            metadatos[clave.strip()] = valor.strip()
    return metadatos, texto[fin + 4 :].lstrip("\n")


def cargar_documentos(carpeta: Path = CARPETA_DOCUMENTOS, patron: str = "*.md") -> list[Documento]:
    documentos = []
    for ruta in sorted(Path(carpeta).glob(patron)):
        metadatos, cuerpo = leer_front_matter(ruta.read_text(encoding="utf-8"))
        titulo = metadatos.get("titulo") or next((l[2:].strip() for l in cuerpo.splitlines() if l.startswith("# ")), ruta.stem)
        documentos.append(Documento(ruta.name, titulo, cuerpo, metadatos))
    return documentos


def trocear_por_secciones(documento: Documento, max_caracteres: int = 1500) -> list[Trozo]:
    """Un trozo por sección ``##``; las secciones largas se dividen por párrafos.

    Cada trozo empieza con el título del documento y de la sección, para que el
    trozo tenga sentido por sí solo cuando se recupera.
    """
    secciones: list[tuple[str, list[str]]] = [("Introducción", [])]
    for linea in documento.texto.splitlines():
        if linea.startswith("## "):
            secciones.append((linea[3:].strip(), []))
        elif not linea.startswith("# "):
            secciones[-1][1].append(linea)
    trozos: list[Trozo] = []
    for seccion, lineas in secciones:
        cuerpo = "\n".join(lineas).strip()
        if not cuerpo:
            continue
        partes, actual = [], ""
        for parrafo in cuerpo.split("\n\n"):
            if actual and len(actual) + len(parrafo) > max_caracteres:
                partes.append(actual)
                actual = parrafo
            else:
                actual = f"{actual}\n\n{parrafo}" if actual else parrafo
        partes.append(actual)
        for i, parte in enumerate(partes):
            trozos.append(Trozo(
                id=f"{Path(documento.nombre).stem}#{len(trozos)}",
                documento=documento.nombre,
                seccion=seccion if len(partes) == 1 else f"{seccion} ({i + 1}/{len(partes)})",
                texto=f"{documento.titulo} — {seccion}\n\n{parte.strip()}",
                metadatos={k: v for k, v in documento.metadatos.items() if k in ("codigo", "clasificacion", "version")},
            ))
    return trozos


def cargar_trozos(carpeta: Path = CARPETA_DOCUMENTOS, max_caracteres: int = 1500) -> list[Trozo]:
    """Todos los documentos de la carpeta, troceados por secciones."""
    return [t for d in cargar_documentos(carpeta) for t in trocear_por_secciones(d, max_caracteres)]
