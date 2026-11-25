"""Construye los materiales derivados del curso a partir de ``curso.json`` y los Markdown.

    python herramientas/construir.py                 # repositorio actual
    python herramientas/construir.py --raiz DESTINO  # otro árbol (lo usa exportar_alumnado.py)
    python herramientas/construir.py --comprobar     # solo valida el calendario y las guías

Qué hace:

1. Valida el calendario: 360 minutos por sesión, horas por módulo, 84 horas en total y
   que el guion de cada guía docente coincide con los bloques de ``curso.json``.
2. Inyecta en los README las tablas generadas (cabecera y agenda de cada sesión;
   resumen, calendario, módulos, equipos y evaluación en el README raíz y la guía docente).
3. Genera ``docs/``: apuntes, ejercicios y práctica de cada sesión en HTML, páginas de
   proyecto, equipos y plantillas, y el índice.
4. Genera ``docs/presentacion/``: una presentación reveal.js por sesión y la del curso.

Si existe ``GUIA_DOCENTE.md`` en la raíz se construye la **versión del profesor**
(guías en HTML, diapositivas «Solo profesor», notas del orador y materiales de
``docente/``). En el repositorio del alumnado no existe y se construye la versión del alumnado.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import re
import shutil
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path

import markdown
from markdown.extensions.toc import slugify
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name
from pygments.util import ClassNotFound

HERRAMIENTAS = Path(__file__).resolve().parent
PLANTILLA = HERRAMIENTAS / "plantilla"
# Copia local de mermaid 11.4.1 (licencia MIT) en plantilla/presentacion_recursos, para que los
# diagramas se dibujen sin conexión. Es la versión clásica (no ESM): un módulo ES no se puede
# cargar desde file:// y los HTML se abren con doble clic. Rutas relativas a docs/ y a docs/presentacion/.
MERMAID_DOCS = "presentacion/recursos/mermaid.min.js"
MERMAID_JS = "recursos/mermaid.min.js"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
         "noviembre", "diciembre"]
TIPOS = {"T": "Teoría", "P": "Práctica", "pausa": "Pausa"}
LENGUAJES = {"python": "Python", "bash": "terminal", "powershell": "PowerShell", "json": "JSON", "ini": ".env",
             "hcl": "Terraform", "caddyfile": "Caddy", "markdown": "Markdown", "mermaid": "diagrama", "yaml": "YAML"}

# ---------------------------------------------------------------------------------------- contexto


@dataclass
class Contexto:
    raiz: Path
    curso: dict
    profesor: bool
    docs: Path = field(init=False)
    repositorio: str = field(init=False)
    paginas: dict[Path, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.docs = self.raiz / "docs"
        repos = self.curso.get("repositorios", {})
        self.repositorio = (repos.get("profesor") if self.profesor else repos.get("alumnado")) or ""

    def carpeta_sesion(self, n: int) -> Path:
        return next(self.raiz.glob(f"sesion_{n:02d}_*"))

    @property
    def sesiones(self) -> list[dict]:
        return self.curso["sesiones"]

    def modulo(self, ident: str) -> dict:
        return next(m for m in self.curso["modulos"] if m["id"] == ident)

    def hito(self, ident: str) -> dict:
        return next(h for h in self.curso["hitos"] if h["id"] == ident)


def leer(ruta: Path) -> str:
    return ruta.read_text(encoding="utf-8")


def escribir(ruta: Path, texto: str) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8", newline="\n")


# ---------------------------------------------------------------------------------------- fechas y horas


def fecha_de(sesion: dict) -> date:
    return date.fromisoformat(sesion["fecha"])


def fecha_larga(sesion: dict) -> str:
    f = fecha_de(sesion)
    return f"{sesion['dia']} {f.day} de {MESES[f.month - 1]} de {f.year}"


def fecha_corta(sesion: dict) -> str:
    f = fecha_de(sesion)
    return f"{sesion['dia'][:3]} {f.day:02d}/{f.month:02d}"


def sumar(hora: str, minutos: int) -> str:
    inicio = datetime.strptime(hora, "%H:%M")
    return (inicio + timedelta(minutes=minutos)).strftime("%H:%M")


def horario(sesion: dict) -> str:
    total = sum(b["min"] for b in sesion["bloques"])
    return f"{sesion['inicio']}-{sumar(sesion['inicio'], total)}"


def horas_texto(minutos: int) -> str:
    h, m = divmod(minutos, 60)
    return f"{h} h" + (f" {m} min" if m else "") if h else f"{m} min"


def modulos_texto(ctx: Contexto, sesion: dict, corto: bool = False) -> str:
    partes = []
    for ident, horas in sesion["modulos"]:
        partes.append(f"{ident} ({horas} h)" if corto else f"{ident} · {ctx.modulo(ident)['nombre']} ({horas} h)")
    return " + ".join(partes)


# ---------------------------------------------------------------------------------------- validación


def validar(ctx: Contexto) -> list[str]:
    avisos: list[str] = []
    horas_modulo: dict[str, float] = {}
    for s in ctx.sesiones:
        total = sum(b["min"] for b in s["bloques"])
        if total != 360:
            avisos.append(f"Sesión {s['n']}: los bloques suman {total} min (deben ser 360)")
        por_modulo: dict[str, int] = {}
        for b in s["bloques"]:
            por_modulo[b["mod"]] = por_modulo.get(b["mod"], 0) + b["min"]
        for ident, horas in s["modulos"]:
            horas_modulo[ident] = horas_modulo.get(ident, 0) + horas
            if por_modulo.get(ident, 0) != horas * 60:
                avisos.append(f"Sesión {s['n']}: {ident} tiene {por_modulo.get(ident, 0)} min en bloques y {horas} h en el programa")
        guia = ctx.carpeta_sesion(s["n"]) / "GUIA_DOCENTE.md"
        if guia.exists():
            avisos.extend(validar_guion(s, leer(guia)))
    for m in ctx.curso["modulos"]:
        if horas_modulo.get(m["id"], 0) != m["horas"]:
            avisos.append(f"{m['id']}: {horas_modulo.get(m['id'], 0)} h en el calendario y {m['horas']} h en el programa")
    total = sum(horas_modulo.values())
    if total != ctx.curso["horas"]:
        avisos.append(f"El calendario suma {total} h y el curso tiene {ctx.curso['horas']} h")
    return avisos


def validar_guion(sesion: dict, guia: str) -> list[str]:
    """El guion minuto a minuto de la guía debe coincidir con los bloques de curso.json."""
    filas = re.findall(r"^\|\s*(\d{2}:\d{2})\s*\|\s*(\d+)\s*\|", guia, flags=re.MULTILINE)
    if not filas:
        return [f"Sesión {sesion['n']}: la guía docente no tiene guion minuto a minuto"]
    esperado, hora = [], sesion["inicio"]
    for b in sesion["bloques"]:
        esperado.append((hora, str(b["min"])))
        hora = sumar(hora, b["min"])
    if filas != esperado:
        return [f"Sesión {sesion['n']}: el guion de la guía ({filas}) no coincide con curso.json ({esperado})"]
    return []


# ---------------------------------------------------------------------------------------- tablas en Markdown


def tabla_md(cabecera: list[str], filas: list[list[str]]) -> str:
    lineas = ["| " + " | ".join(cabecera) + " |", "| " + " | ".join("---" for _ in cabecera) + " |"]
    lineas += ["| " + " | ".join(str(c).replace("|", "\\|") for c in fila) + " |" for fila in filas]
    return "\n".join(lineas)


def md_cabecera_sesion(ctx: Contexto, s: dict) -> str:
    hito = ctx.hito(s["hito"])
    tabla = tabla_md(["Fecha", "Horario", "Modalidad", "Módulos", "Hito"],
                     [[fecha_larga(s), horario(s), s["modalidad"], modulos_texto(ctx, s), f"{hito['id']} · {hito['nombre']}"]])
    return f"{tabla}\n\n**Objetivo:** {s['objetivo']}"


def md_agenda_sesion(ctx: Contexto, s: dict) -> str:
    varios = len(s["modulos"]) > 1
    filas, hora = [], s["inicio"]
    teoria = practica = 0
    for b in s["bloques"]:
        fila = [hora, str(b["min"]), TIPOS[b["tipo"]], b["titulo"]]
        if varios:
            fila.insert(3, b["mod"])
        filas.append(fila)
        hora = sumar(hora, b["min"])
        if b["tipo"] == "T":
            teoria += b["min"]
        else:
            practica += b["min"]
    cabecera = ["Hora", "Min", "Tipo"] + (["Módulo"] if varios else []) + ["Bloque"]
    return (f"### Agenda de la sesión\n\n{tabla_md(cabecera, filas)}\n\n"
            f"Teoría: {horas_texto(teoria)} · práctica: {horas_texto(practica)} (las pausas computan en el bloque práctico).")


def md_resumen(ctx: Contexto) -> str:
    c = ctx.curso
    presenciales = [fecha_corta(s) for s in ctx.sesiones if s["modalidad"] == "Presencial"]
    pendientes = [fecha_corta(s) for s in ctx.sesiones if s["modalidad"] not in ("Presencial", "Remoto")]
    modalidad = f"Presencial: {', '.join(presenciales)}. Resto en remoto"
    if pendientes:
        modalidad += f" (por confirmar: {', '.join(pendientes)})"
    return tabla_md(["", ""], [
        ["Duración", f"{c['horas']} horas en {len(ctx.sesiones)} sesiones de 6 horas"],
        ["Fechas", c["fechas"]],
        ["Modalidad", modalidad],
        ["Participantes", f"{c['participantes']} personas en {len(c['equipos'])} equipos de {c['participantes'] // len(c['equipos'])}"],
        ["Metodología", c["metodologia"]],
        ["Cliente del curso", f"{c['cliente_ficticio']} (ficticio)"],
    ])


def md_calendario(ctx: Contexto, docente: bool = False) -> str:
    filas = []
    for s in ctx.sesiones:
        carpeta = ctx.carpeta_sesion(s["n"]).name
        enlace = f"[{s['titulo']}]({carpeta}/{'GUIA_DOCENTE.md' if docente else 'README.md'})"
        filas.append([str(s["n"]), fecha_corta(s), horario(s), s["modalidad"], modulos_texto(ctx, s, corto=True), enlace])
    return tabla_md(["Sesión", "Fecha", "Horario", "Modalidad", "Módulos", "Contenido" + (" (guía docente)" if docente else "")], filas)


def md_modulos(ctx: Contexto) -> str:
    filas = []
    for m in ctx.curso["modulos"]:
        sesiones = [str(s["n"]) for s in ctx.sesiones if any(i == m["id"] for i, _ in s["modulos"])]
        filas.append([m["id"], m["nombre"], f"{m['horas']} h", ", ".join(sesiones), "; ".join(m["temas"])])
    return tabla_md(["Módulo", "Nombre", "Horas", "Sesiones", "Temas"], filas)


def md_equipos(ctx: Contexto) -> str:
    return tabla_md(["Equipo", "Reto", "Qué construye", "Fuentes del RAG", "Herramientas"],
                    [[e["nombre"], f"**{e['reto']}**", e["descripcion"], e["rag"], e["herramientas"]] for e in ctx.curso["equipos"]])


def md_evaluacion(ctx: Contexto) -> str:
    pesos = tabla_md(["Componente", "Peso", "Evidencias"],
                     [[e["componente"], f"{e['peso']} %", e["evidencia"]] for e in ctx.curso["evaluacion"]])
    hitos = tabla_md(["Hito", "Sesiones", "Entregables", "Resultado"],
                     [[f"{h['id']} · {h['nombre']}", h["sesiones"], h["entregables"], h["resultado"]] for h in ctx.curso["hitos"]])
    return f"{pesos}\n\n**Hitos del proyecto**\n\n{hitos}"


def inyectar(texto: str, nombre: str, contenido: str) -> str:
    patron = re.compile(rf"(<!-- {nombre}:inicio -->)(.*?)(<!-- {nombre}:fin -->)", re.DOTALL)
    if not patron.search(texto):
        return texto
    return patron.sub(lambda m: f"{m.group(1)}\n{contenido}\n{m.group(3)}", texto)


def quitar_inyectado(texto: str) -> str:
    return re.sub(r"<!-- (\w+):inicio -->.*?<!-- \1:fin -->", "", texto, flags=re.DOTALL)


def actualizar_readmes(ctx: Contexto) -> int:
    cambios = 0
    for s in ctx.sesiones:
        ruta = ctx.carpeta_sesion(s["n"]) / "README.md"
        texto = leer(ruta)
        nuevo = inyectar(inyectar(texto, "cabecera", md_cabecera_sesion(ctx, s)), "agenda", md_agenda_sesion(ctx, s))
        if nuevo != texto:
            escribir(ruta, nuevo)
            cambios += 1
    for nombre, docente in (("README.md", False), ("GUIA_DOCENTE.md", True)):
        ruta = ctx.raiz / nombre
        if not ruta.exists():
            continue
        texto = leer(ruta)
        nuevo = texto
        for marca, contenido in (("resumen", md_resumen(ctx)), ("calendario", md_calendario(ctx, docente)),
                                 ("modulos", md_modulos(ctx)), ("equipos", md_equipos(ctx)),
                                 ("evaluacion", md_evaluacion(ctx))):
            nuevo = inyectar(nuevo, marca, contenido)
        if nuevo != texto:
            escribir(ruta, nuevo)
            cambios += 1
    return cambios


# ---------------------------------------------------------------------------------------- Markdown a HTML

FORMATEADOR = HtmlFormatter(nowrap=True)


def resaltar(codigo: str, lenguaje: str) -> str:
    try:
        lexer = get_lexer_by_name(lenguaje) if lenguaje else TextLexer()
    except ClassNotFound:
        lexer = TextLexer()
    return highlight(codigo, lexer, FORMATEADOR).rstrip("\n")


def extraer_mermaid(texto: str) -> tuple[str, bool]:
    """Sustituye los bloques ```mermaid por HTML que dibuja mermaid.js en el navegador."""
    hay = False

    def cambiar(m: re.Match) -> str:
        nonlocal hay
        hay = True
        return f'\n<pre class="mermaid">{html.escape(m.group(1).strip())}</pre>\n'

    return re.sub(r"^```mermaid\n(.*?)^```", cambiar, texto, flags=re.MULTILINE | re.DOTALL), hay


def convertidor(toc: bool = True) -> markdown.Markdown:
    extensiones = ["tables", "fenced_code", "codehilite", "sane_lists", "attr_list"] + (["toc"] if toc else [])
    return markdown.Markdown(extensions=extensiones, extension_configs={
        "codehilite": {"guess_lang": False, "css_class": "codehilite"},
        "toc": {"slugify": slugify, "toc_depth": "2-3"},
    })


def envolver_tablas(fragmento: str) -> str:
    return fragmento.replace("<table>", '<div class="tabla"><table>').replace("</table>", "</table></div>")


def reescribir_enlaces(ctx: Contexto, fragmento: str, origen: Path, prefijo: str = "") -> str:
    """Convierte los enlaces relativos de los Markdown en enlaces a las páginas HTML o al repositorio."""

    def cambiar(m: re.Match) -> str:
        destino = html.unescape(m.group(1))
        if re.match(r"^(https?:|mailto:|#)", destino):
            extra = ' target="_blank" rel="noopener"' if destino.startswith("http") else ""
            return f'href="{html.escape(destino)}"{extra}'
        ruta, _, ancla = destino.partition("#")
        absoluta = (origen.parent / ruta).resolve()
        if absoluta in ctx.paginas:
            return f'href="{prefijo}{ctx.paginas[absoluta]}{"#" + ancla if ancla else ""}"'
        try:
            relativa = absoluta.relative_to(ctx.raiz.resolve()).as_posix()
        except ValueError:
            return f'href="{html.escape(destino)}"'
        if relativa.startswith("docs/"):
            return f'href="{prefijo}{relativa[5:]}"'
        if ctx.repositorio:
            tipo = "tree" if absoluta.is_dir() else "blob"
            return f'href="{ctx.repositorio}/{tipo}/main/{relativa}" target="_blank" rel="noopener"'
        return f'href="{html.escape(destino)}"'

    return re.sub(r'href="([^"]+)"', cambiar, fragmento)


def md_a_html(ctx: Contexto, texto: str, origen: Path, prefijo: str = "") -> tuple[str, str, bool]:
    """Devuelve (cuerpo, índice, usa_mermaid)."""
    texto, mermaid = extraer_mermaid(quitar_comentarios(texto))
    conv = convertidor()
    cuerpo = envolver_tablas(conv.convert(texto))
    return reescribir_enlaces(ctx, cuerpo, origen, prefijo), conv.toc, mermaid


def quitar_comentarios(texto: str) -> str:
    return re.sub(r"<!--.*?-->\n?", "", texto, flags=re.DOTALL)


def en_linea(texto: str) -> str:
    """Markdown de una línea (títulos) sin el párrafo."""
    texto = re.sub(r"^(\d+)\.(\s)", r"\1\\.\2", texto.strip())  # «1. Especificación» no es una lista
    salida = markdown.markdown(texto)
    return re.sub(r"^<p>(.*)</p>$", r"\1", salida, flags=re.DOTALL)


def texto_plano(texto: str) -> str:
    return re.sub(r"[*_`]", "", texto).strip()


# ---------------------------------------------------------------------------------------- páginas de apuntes

SCRIPT_TEMA = """<script>
(function () {
  var raiz = document.documentElement, guardado = null;
  try { guardado = localStorage.getItem("tema"); } catch (e) {}
  if (guardado) raiz.setAttribute("data-theme", guardado);
  document.addEventListener("click", function (ev) {
    if (!ev.target.matches("[data-cambiar-tema]")) return;
    var oscuro = raiz.getAttribute("data-theme") === "dark" ||
      (!raiz.getAttribute("data-theme") && matchMedia("(prefers-color-scheme: dark)").matches);
    var nuevo = oscuro ? "light" : "dark";
    raiz.setAttribute("data-theme", nuevo);
    try { localStorage.setItem("tema", nuevo); } catch (e) {}
  });
})();
</script>"""

CSS_EXTRA = """
.aviso-profe { border-left: 4px solid #c98a12; background: var(--acento-suave); padding: .6rem 1rem; border-radius: 6px; margin: 0 0 1.4rem; font-size: .95rem; }
.ficha { display: flex; flex-wrap: wrap; gap: .4rem .8rem; margin: -.4rem 0 1.4rem; font-size: .9rem; color: var(--suave); }
.ficha span { background: var(--acento-suave); padding: .1rem .6rem; border-radius: 20px; }
.tarjeta .num.profe { color: #c98a12; }
.seccion-indice { margin-top: 3rem; }
pre.mermaid { background: var(--panel); text-align: center; }
"""


def pagina_doc(ctx: Contexto, titulo: str, cuerpo: str, toc: str, nav: str = "", pie: str = "",
               mermaid: bool = False, ficha: str = "", solo_profesor: bool = False) -> str:
    css = leer(PLANTILLA / "docs.css") + CSS_EXTRA
    script_mermaid = ""
    if mermaid:
        script_mermaid = (f'<script src="{MERMAID_DOCS}"></script>'
                          '<script>var oscuro = document.documentElement.getAttribute("data-theme") === "dark" || '
                          '(!document.documentElement.getAttribute("data-theme") && matchMedia("(prefers-color-scheme: dark)").matches);'
                          'mermaid.initialize({ startOnLoad: true, theme: oscuro ? "dark" : "default" });</script>')
    aviso = ('<div class="aviso-profe">Versión del profesor: contiene material que no se publica en el repositorio del alumnado.</div>'
             if solo_profesor else "")
    indice = f'<aside class="indice"><div class="rotulo">En esta página</div>{toc}</aside>' if toc else "<aside class=\"indice\"></aside>"
    if ficha:
        cuerpo = re.sub(r"(</h1>)", rf"\1{ficha}", cuerpo, count=1)
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(texto_plano(titulo))} · {html.escape(ctx.curso['titulo'])}</title>
<style>{css}</style>
{script_mermaid}
</head>
<body>
<header class="barra">
  <a class="curso" href="index.html">{html.escape(ctx.curso['titulo'])}</a>
  <nav>{nav}</nav>
  <button type="button" data-cambiar-tema>Claro / oscuro</button>
</header>
<div class="pagina">
{indice}
<main>
{aviso}{cuerpo}
<div class="pie">{pie}</div>
</main>
</div>
{SCRIPT_TEMA}
</body>
</html>
"""


def nav_sesion(ctx: Contexto, n: int) -> str:
    enlaces = [(f"sesion_{n:02d}.html", "Apuntes"), (f"sesion_{n:02d}_ejercicios.html", "Ejercicios"),
               (f"sesion_{n:02d}_practica.html", "Práctica"), (f"presentacion/sesion_{n:02d}.html", "Presentación")]
    if ctx.profesor:
        enlaces.append((f"sesion_{n:02d}_guia.html", "Guía docente"))
    return " ".join(f'<a href="{h}">{t}</a>' for h, t in enlaces)


def pie_sesion(ctx: Contexto, n: int, sufijo: str = "") -> str:
    anterior = f"sesion_{n - 1:02d}{sufijo}.html" if n > 1 else "index.html"
    siguiente = f"sesion_{n + 1:02d}{sufijo}.html" if n < len(ctx.sesiones) else "index.html"
    return (f'<a href="{anterior}">&larr; Anterior</a><a href="index.html">Índice del curso</a>'
            f'<a href="{siguiente}">Siguiente &rarr;</a>')


def ficha_sesion(ctx: Contexto, s: dict) -> str:
    partes = [f"Sesión {s['n']}", fecha_larga(s), horario(s), s["modalidad"], modulos_texto(ctx, s, corto=True)]
    return '<div class="ficha">' + "".join(f"<span>{html.escape(p)}</span>" for p in partes) + "</div>"


@dataclass
class Pagina:
    origen: Path
    destino: str
    titulo: str
    nav: str = ""
    pie: str = ""
    ficha: str = ""
    profesor: bool = False
    transformar: object = None  # función opcional sobre el texto Markdown


def paginas(ctx: Contexto) -> list[Pagina]:
    lista: list[Pagina] = []
    for s in ctx.sesiones:
        n, carpeta = s["n"], ctx.carpeta_sesion(s["n"])
        nav = nav_sesion(ctx, n)
        ficha = ficha_sesion(ctx, s)
        # Los apuntes ya llevan la cabecera con fecha, horario y módulos: sin ficha para no repetirla.
        lista.append(Pagina(carpeta / "README.md", f"sesion_{n:02d}.html", s["titulo"], nav, pie_sesion(ctx, n)))
        lista.append(Pagina(carpeta / "ejercicios" / "README.md", f"sesion_{n:02d}_ejercicios.html", f"Sesión {n}. Ejercicios",
                            nav, pie_sesion(ctx, n, "_ejercicios"), ficha))
        practica = next((carpeta / "ejercicios").glob("PRACTICA_*.md"), None)
        if practica:
            lista.append(Pagina(practica, f"sesion_{n:02d}_practica.html", f"Sesión {n}. Práctica", nav,
                                pie_sesion(ctx, n, "_practica"), ficha))
        lista.append(Pagina(carpeta / "GUIA_DOCENTE.md", f"sesion_{n:02d}_guia.html", f"Sesión {n}. Guía docente", nav,
                            pie_sesion(ctx, n, "_guia"), ficha, profesor=True))
    generales = [
        ("README.md", "curso.html", "El curso"),
        ("proyecto_final/README.md", "proyecto_final.html", "Proyecto final"),
        ("equipos/README.md", "equipos.html", "Equipos y retos"),
        ("equipos/plantilla_proyecto/README.md", "plantilla_proyecto.html", "Plantilla del proyecto"),
        ("datos/atlantica/README.md", "datos_atlantica.html", "Datos de Atlántica Logística"),
    ]
    for origen, destino, titulo in generales:
        lista.append(Pagina(ctx.raiz / origen, destino, titulo, pie='<a href="index.html">Índice del curso</a>'))
    for origen, destino, titulo in [
        ("GUIA_DOCENTE.md", "guia_docente.html", "Guía docente del curso"),
        ("evaluacion/README.md", "evaluacion.html", "Evaluación"),
    ] + [(f"docente/{p.name}", f"docente_{p.stem}.html", texto_plano(primer_titulo(leer(p)) or p.stem))
         for p in sorted((ctx.raiz / "docente").glob("*.md"))]:
        lista.append(Pagina(ctx.raiz / origen, destino, titulo, pie='<a href="index.html">Índice del curso</a>', profesor=True))
    if (ctx.raiz / "docente" / "prueba_individual.md").exists():
        lista.append(Pagina(ctx.raiz / "docente" / "prueba_individual.md", "docente_prueba_individual_enunciado.html",
                            "Prueba individual (enunciado para imprimir)", pie='<a href="index.html">Índice del curso</a>',
                            profesor=True, transformar=lambda t: t.split("<!-- SOLUCIONES -->")[0]))
    return [p for p in lista if p.origen.exists() and (ctx.profesor or not p.profesor)]


def primer_titulo(texto: str) -> str:
    m = re.search(r"^# (.+)$", texto, flags=re.MULTILINE)
    return m.group(1).strip() if m else ""


def pagina_plantillas(ctx: Contexto) -> tuple[str, str, bool]:
    partes, hay_mermaid = [], False
    for ruta in sorted((ctx.raiz / "plantillas").glob("*.md")):
        texto = leer(ruta)
        texto = re.sub(r"^(#{1,5}) ", lambda m: "#" + m.group(1) + " ", texto, flags=re.MULTILINE)  # baja un nivel
        partes.append(texto + f"\n\n*Fichero: `plantillas/{ruta.name}`*\n")
    texto = "# Plantillas de los entregables\n\nCopia cada plantilla en la carpeta `docs/` del repositorio de tu equipo y rellénala. " \
            "La plantilla del proyecto (`equipos/plantilla_proyecto/docs/`) ya las incluye.\n\n" + "\n\n".join(partes)
    texto, hay_mermaid = extraer_mermaid(texto)
    conv = convertidor()
    cuerpo = envolver_tablas(conv.convert(texto))
    return cuerpo, conv.toc, hay_mermaid


# ---------------------------------------------------------------------------------------- índice de los apuntes


def tarjeta(num: str, titulo: str, enlaces: list[tuple[str, str]], clase_num: str = "") -> str:
    a = "".join(f'<a href="{h}">{html.escape(t)}</a>' for h, t in enlaces)
    return (f'<div class="tarjeta"><div class="num{(" " + clase_num) if clase_num else ""}">{html.escape(num)}</div>'
            f'<h3>{html.escape(titulo)}</h3><div class="enlaces">{a}</div></div>')


def pagina_indice(ctx: Contexto) -> str:
    c = ctx.curso
    calendario = envolver_tablas(markdown.markdown(md_calendario(ctx), extensions=["tables"]))
    calendario = re.sub(r'href="(sesion_\d\d)_[^"/]+/README\.md"', lambda m: f'href="{m.group(1)}.html"', calendario)
    tarjetas = []
    for s in ctx.sesiones:
        n = s["n"]
        enlaces = [(f"sesion_{n:02d}.html", "Apuntes"), (f"sesion_{n:02d}_ejercicios.html", "Ejercicios"),
                   (f"sesion_{n:02d}_practica.html", "Práctica"), (f"presentacion/sesion_{n:02d}.html", "Presentación")]
        if ctx.profesor:
            enlaces.append((f"sesion_{n:02d}_guia.html", "Guía"))
        tarjetas.append(tarjeta(f"Sesión {n} · {fecha_corta(s)} · {s['modalidad']}", s["titulo"], enlaces))
    recursos = [
        tarjeta("Curso", "Puesta en marcha y organización", [("curso.html", "Leer")]),
        tarjeta("Proyecto", "Proyecto final y rúbrica", [("proyecto_final.html", "Leer")]),
        tarjeta("Equipos", "Equipos, retos y roles", [("equipos.html", "Leer"), ("plantilla_proyecto.html", "Plantilla del proyecto")]),
        tarjeta("Plantillas", "Plantillas de los entregables", [("plantillas.html", "Ver")]),
        tarjeta("Cliente", "Datos de Atlántica Logística", [("datos_atlantica.html", "Leer")]),
    ]
    docente = ""
    if ctx.profesor:
        enlaces_docente = [tarjeta("Docente", "Guía docente del curso", [("guia_docente.html", "Leer")], "profe"),
                           tarjeta("Docente", "Evaluación y calificaciones", [("evaluacion.html", "Leer")], "profe")]
        for ruta in sorted((ctx.raiz / "docente").glob("*.md")):
            enlaces = [(f"docente_{ruta.stem}.html", "Leer")]
            if ruta.stem == "prueba_individual":
                enlaces.append(("docente_prueba_individual_enunciado.html", "Enunciado para imprimir"))
            enlaces_docente.append(tarjeta("Docente", texto_plano(primer_titulo(leer(ruta)) or ruta.stem), enlaces, "profe"))
        docente = ('<h2 class="seccion-indice">Material del docente</h2><p class="entrada">Solo en el repositorio docente.</p>'
                   f'<div class="tarjetas">{"".join(enlaces_docente)}</div>')
    version = " · versión del profesor" if ctx.profesor else ""
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(c['titulo'])}</title>
<style>{leer(PLANTILLA / 'docs.css') + CSS_EXTRA}</style>
</head>
<body>
<header class="barra">
  <a class="curso" href="index.html">{html.escape(c['titulo'])}</a>
  <nav><a href="curso.html">El curso</a> <a href="proyecto_final.html">Proyecto final</a> <a href="presentacion/index.html">Presentación</a></nav>
  <button type="button" data-cambiar-tema>Claro / oscuro</button>
</header>
<div class="portada">
<h1>{html.escape(c['titulo'])}</h1>
<p class="entrada">{c['horas']} horas · {html.escape(c['fechas'])} · {c['participantes']} participantes en {len(c['equipos'])} equipos{version}.</p>
<p class="entrada">{html.escape(c['metodologia'])} Cada sesión tiene apuntes, ejemplos ejecutables, ejercicios con pruebas automáticas, una práctica de equipo sobre el cliente ficticio {html.escape(c['cliente_ficticio'])} y su presentación.</p>
<p class="entrada"><a href="presentacion/index.html"><strong>Abrir la presentación del curso</strong></a>: calendario, módulos, equipos y evaluación en diapositivas.</p>
<h2 class="seccion-indice">Calendario</h2>
{calendario}
<h2 class="seccion-indice">Sesiones</h2>
<div class="tarjetas">{''.join(tarjetas)}</div>
<h2 class="seccion-indice">Proyecto y recursos</h2>
<div class="tarjetas">{''.join(recursos)}</div>
{docente}
</div>
{SCRIPT_TEMA}
</body>
</html>
"""


# ---------------------------------------------------------------------------------------- presentaciones


@dataclass
class Apartado:
    titulo: str
    nivel: int
    bloques: list[str] = field(default_factory=list)
    hijos: list["Apartado"] = field(default_factory=list)

    @property
    def numero(self) -> str:
        m = re.match(r"^(\d+\.\d+)\s+(.*)$", self.titulo)
        return m.group(1) if m else ""

    @property
    def nombre(self) -> str:
        m = re.match(r"^(\d+\.\d+)\s+(.*)$", self.titulo)
        return m.group(2) if m else self.titulo


def es_lista(bloque: str) -> bool:
    return bool(re.match(r"^\s*([-*+]|\d+\.)\s", bloque))


def partir_bloques(texto: str) -> list[str]:
    """Divide un Markdown en bloques: párrafos, listas, tablas, código y títulos."""
    bloques: list[str] = []
    actual: list[str] = []
    en_codigo = False

    def cerrar() -> None:
        if actual:
            bloques.append("\n".join(actual))
            actual.clear()

    for linea in texto.splitlines():
        if linea.startswith("```"):
            if not en_codigo:
                cerrar()
                en_codigo = True
                actual.append(linea)
            else:
                actual.append(linea)
                cerrar()
                en_codigo = False
            continue
        if en_codigo:
            actual.append(linea)
            continue
        if not linea.strip():
            cerrar()
            continue
        if linea.startswith("#"):
            cerrar()
            bloques.append(linea)
            continue
        actual.append(linea)
    cerrar()
    # Une los elementos de una lista separados por líneas en blanco y las continuaciones sangradas.
    unidos: list[str] = []
    for b in bloques:
        if unidos and ((es_lista(b) and es_lista(unidos[-1]) and not unidos[-1].startswith("```"))
                       or (b.startswith("   ") and not b.lstrip().startswith("```") and es_lista(unidos[-1]))):
            unidos[-1] += "\n\n" + b
        elif unidos and b.lstrip().startswith("```") and b.startswith("   ") and es_lista(unidos[-1]):
            unidos[-1] += "\n\n" + b
        else:
            unidos.append(b)
    return unidos


def estructurar(texto: str) -> tuple[str, list[str], list[Apartado]]:
    titulo, intro, apartados = "", [], []
    for bloque in partir_bloques(quitar_comentarios(quitar_inyectado(texto))):
        m = re.match(r"^(#{1,6})\s+(.*)$", bloque) if "\n" not in bloque else None
        if m:
            nivel, texto_titulo = len(m.group(1)), m.group(2).strip()
            if nivel == 1:
                titulo = texto_titulo
            elif nivel == 2:
                apartados.append(Apartado(texto_titulo, 2))
            elif nivel == 3 and apartados:
                apartados[-1].hijos.append(Apartado(texto_titulo, 3))
            else:
                destino = (apartados[-1].hijos[-1] if apartados and apartados[-1].hijos else apartados[-1]) if apartados else None
                (destino.bloques if destino else intro).append(f"**{texto_titulo}**")
            continue
        if bloque.strip() == "---":
            continue
        if not apartados:
            intro.append(bloque)
        elif apartados[-1].hijos:
            apartados[-1].hijos[-1].bloques.append(bloque)
        else:
            apartados[-1].bloques.append(bloque)
    return titulo, intro, apartados


def peso(bloque: str) -> float:
    if bloque.startswith("```mermaid"):
        return 9
    if bloque.lstrip().startswith("```"):
        return max(2.5, (bloque.count("\n") - 1) * 0.8 + 1.6)
    if bloque.startswith("|"):
        filas = [f for f in bloque.splitlines() if f.startswith("|")][2:]
        return 1.4 + sum(max(1.0, math.ceil(len(f) / 120)) * 1.05 for f in filas)
    if es_lista(bloque):
        elementos = re.split(r"\n(?=\s*(?:[-*+]|\d+\.)\s)", bloque)
        return 0.4 + sum(max(1, math.ceil(len(e) / 95)) for e in elementos) + 0.8 * bloque.count("```")
    return 0.5 + max(1, math.ceil(len(bloque) / 105))


def trocear_tabla(bloque: str, limite: float = 10.5) -> list[str]:
    """Parte las tablas largas en trozos que caben en una diapositiva, repitiendo la cabecera."""
    lineas = bloque.splitlines()
    cabecera, filas = lineas[:2], lineas[2:]
    if peso(bloque) <= limite + 1.5:
        return [bloque]
    trozos, actual, usado = [], [], 1.4
    for fila in filas:
        p = max(1.0, math.ceil(len(fila) / 120)) * 1.05
        if actual and usado + p > limite:
            trozos.append("\n".join(cabecera + actual))
            actual, usado = [], 1.4
        actual.append(fila)
        usado += p
    if actual:
        trozos.append("\n".join(cabecera + actual))
    return trozos


def trocear_codigo(bloque: str, lineas_max: int = 22) -> list[str]:
    lineas = bloque.splitlines()
    apertura, cuerpo = lineas[0], lineas[1:-1]
    if len(cuerpo) <= lineas_max + 4:
        return [bloque]
    return [f"{apertura}\n" + "\n".join(cuerpo[i:i + lineas_max]) + "\n```" for i in range(0, len(cuerpo), lineas_max)]


def paginar(bloques: list[str], limite: float = 12.5) -> list[list[str]]:
    piezas: list[str] = []
    for b in bloques:
        if b.startswith("|"):
            piezas.extend(trocear_tabla(b))
        elif b.startswith("```") and not b.startswith("```mermaid"):
            piezas.extend(trocear_codigo(b))
        else:
            piezas.append(b)
    paginas_: list[list[str]] = []
    actual: list[str] = []
    usado = 0.0
    for b in piezas:
        p = peso(b)
        # Un párrafo corto que presenta el bloque siguiente se queda con él.
        if actual and usado + p > limite:
            if len(actual) > 1 and not actual[-1].startswith(("|", "```")) and peso(actual[-1]) <= 2.5 and p + peso(actual[-1]) <= limite:
                arrastre = actual.pop()
                paginas_.append(actual)
                actual, usado = [arrastre], peso(arrastre)
            else:
                paginas_.append(actual)
                actual, usado = [], 0.0
        actual.append(b)
        usado += p
    if actual:
        paginas_.append(actual)
    return paginas_


def bloque_codigo(bloque: str) -> str:
    lineas = bloque.strip().splitlines()
    lenguaje = lineas[0].strip("`").strip().lower()
    codigo = "\n".join(lineas[1:-1] if lineas[-1].startswith("```") else lineas[1:])
    codigo = re.sub(r"^ {3}", "", codigo, flags=re.MULTILINE) if bloque.startswith("   ") else codigo
    etiqueta = LENGUAJES.get(lenguaje, lenguaje)
    clase = "codigo" if lenguaje else "codigo plano"
    rotulo = f'<span class="lenguaje">{html.escape(etiqueta)}</span>' if etiqueta else ""
    return (f'<div class="{clase}"><div class="barra-codigo">{rotulo}<button class="copiar" type="button" '
            f'title="Copiar el código">Copiar</button></div><pre><code>{resaltar(codigo, lenguaje)}</code></pre></div>')


def bloque_html(ctx: Contexto, bloque: str, origen: Path) -> str:
    if bloque.startswith("```mermaid"):
        fuente = "\n".join(bloque.splitlines()[1:-1])
        return f'<pre class="mermaid">{html.escape(fuente)}</pre>'
    if bloque.startswith("```"):
        return bloque_codigo(bloque)
    if es_lista(bloque) and "```" in bloque:
        # Lista con código dentro: el código se pinta con el estilo de las diapositivas.
        partes = re.split(r"(\n\s*```[\s\S]*?```)", bloque)
        salida = []
        for parte in partes:
            if parte.strip().startswith("```"):
                salida.append(bloque_codigo(re.sub(r"^\n", "", parte)))
            elif parte.strip():
                salida.append(markdown.markdown(parte, extensions=["tables", "sane_lists"]))
        return reescribir_enlaces(ctx, "".join(salida), origen, "../")
    fragmento = markdown.markdown(bloque, extensions=["tables", "sane_lists", "attr_list"])
    return reescribir_enlaces(ctx, envolver_tablas(fragmento), origen, "../")


def diapositiva(ctx: Contexto, antetitulo: str, titulo: str, bloques: list[str], origen: Path, clase: str = "",
                menu: str = "", ident: str = "", notas: str = "", parte: str = "") -> str:
    atributos = (f' class="{clase}"' if clase else "") + (f' id="{ident}"' if ident else "") + \
                (f' data-menu="{html.escape(texto_plano(menu))}"' if menu else "")
    cuerpo = "".join(bloque_html(ctx, b, origen) for b in bloques)
    span_parte = f' <span class="parte">{parte}</span>' if parte else ""
    aside = f'<aside class="notes">{notas}</aside>' if notas else ""
    return (f'<section{atributos}><header class="cabecera"><p class="antetitulo">{en_linea(antetitulo)}</p>'
            f'<h2>{en_linea(titulo)}{span_parte}</h2></header><div class="cuerpo">{cuerpo}</div>{aside}</section>')


def grupo(ctx: Contexto, antetitulo: str, titulo: str, bloques: list[str], origen: Path, clase: str = "",
          menu: str = "", ident: str = "", notas: str = "") -> list[str]:
    paginas_ = paginar(bloques) if bloques else []
    total = len(paginas_)
    return [diapositiva(ctx, antetitulo, titulo, p, origen, clase, menu if i == 0 else "", ident if i == 0 else "",
                        notas if i == 0 else "", f"{i + 1}/{total}" if total > 1 else "")
            for i, p in enumerate(paginas_)]


def divisor(numero: str, titulo: str, puntos: list[str], ident: str, clase: str = "especial seccion",
            notas: str = "", menu: str = "") -> str:
    lista = "".join(f"<li>{en_linea(p)}</li>" for p in puntos[:7])
    aside = f'<aside class="notes">{notas}</aside>' if notas else ""
    return (f'<section class="{clase}" id="{ident}" data-menu="{html.escape(texto_plano(menu or (numero + " " + titulo)))}" '
            f'data-transition="fade"><div class="divisor"><span class="numero">{html.escape(numero)}</span>'
            f'<h2>{en_linea(titulo)}</h2>{"<ul class=puntos>" + lista + "</ul>" if lista else ""}</div>{aside}</section>')


def notas_por_unidad(guia: str) -> dict[str, str]:
    """Extrae de la guía los párrafos «**1.1** ...» de la sección «Notas por unidad»."""
    m = re.search(r"^## Notas por unidad\n(.*?)(?=^## )", guia + "\n## ", flags=re.MULTILINE | re.DOTALL)
    if not m:
        return {}
    notas = {}
    for bloque in partir_bloques(m.group(1)):
        n = re.match(r"^\*\*(\d+\.\d+)\*\*\s*(.*)$", bloque, flags=re.DOTALL)
        if n:
            notas[n.group(1)] = markdown.markdown(n.group(2))
    return notas


def tarjetas_repaso(bloques: list[str]) -> str:
    preguntas = []
    for bloque in bloques:
        for elemento in re.split(r"\n(?=\d+\.\s)", bloque):
            m = re.match(r"^\d+\.\s+\*\*(.+?)\*\*\s*(.*)$", elemento.strip(), flags=re.DOTALL)
            if m:
                preguntas.append((m.group(1), m.group(2)))
    celdas = "".join(
        f'<button type="button" class="pregunta"><span class="n">{i}</span><span class="cara"><span class="frente">{en_linea(p)}</span>'
        f'<span class="dorso">{en_linea(r)}</span></span></button>' for i, (p, r) in enumerate(preguntas, 1))
    return f'<p class="ayuda">Piensa la respuesta y haz clic en la tarjeta para comprobarla.</p><div class="preguntas">{celdas}</div>'


def portada(ctx: Contexto, s: dict, titulo: str, objetivo: str, unidades: int, ficheros: int) -> str:
    insignia = '<span class="insignia">Versión del profesor</span>' if ctx.profesor else ""
    return (f'<section class="especial inicio" id="portada" data-menu="Portada" data-transition="fade"><div class="portada">'
            f'<div class="formas" aria-hidden="true"><i></i><i></i><i></i></div>'
            f'<p class="curso">{html.escape(ctx.curso["titulo_corto"])}</p>'
            f'<p class="modulo">Sesión {s["n"]} · {html.escape(fecha_larga(s))} · {horario(s)} · {html.escape(s["modalidad"])}</p>'
            f'<h1>{en_linea(titulo)}</h1><div class="objetivo"><p>{html.escape(texto_plano(objetivo))}</p></div>'
            f'<div class="cifras"><div class="cifra"><b data-cuenta="6">6</b><span>horas</span></div>'
            f'<div class="cifra"><b data-cuenta="{unidades}">{unidades}</b><span>unidades</span></div>'
            f'<div class="cifra"><b data-cuenta="{ficheros}">{ficheros}</b><span>ejercicios</span></div></div>'
            f'<p class="navega">Avanza con <kbd>→</kbd> o <kbd>Espacio</kbd> · <kbd>M</kbd> índice · <kbd>Esc</kbd> vista general'
            f'{" · <kbd>S</kbd> notas del orador" if ctx.profesor else ""}</p></div>{insignia}</section>')


def presentacion_sesion(ctx: Contexto, s: dict) -> str:
    n, carpeta = s["n"], ctx.carpeta_sesion(s["n"])
    readme = carpeta / "README.md"
    titulo, intro, apartados = estructurar(leer(readme))
    titulo_corto = re.sub(r"^Sesión \d+\.\s*", "", titulo)
    objetivo = next((b for b in intro if not b.startswith(("|", "<", "#"))), s["objetivo"])
    unidades = [a for a in apartados if a.numero]
    ejercicios = [p for p in (carpeta / "ejercicios").glob("s*_ej*.py")]
    secciones = [portada(ctx, s, titulo_corto, objetivo, len(unidades), len(ejercicios))]

    guia_texto = leer(carpeta / "GUIA_DOCENTE.md") if ctx.profesor and (carpeta / "GUIA_DOCENTE.md").exists() else ""
    _, _, guia = estructurar(guia_texto) if guia_texto else ("", [], [])
    notas = notas_por_unidad(guia_texto) if guia_texto else {}
    guia_inicio = [a for a in guia if re.match(r"^(Preparación|Guion|Mensajes clave)", a.titulo)]
    guia_repaso = [a for a in guia if a.titulo.startswith("Preguntas de repaso")]
    guia_final = [a for a in guia if a not in guia_inicio and a not in guia_repaso and a.titulo != "Notas por unidad"]

    for a in guia_inicio:
        secciones += grupo(ctx, f"Guía docente · sesión {n}", a.titulo, a.bloques + sum(([f"**{h.titulo}**"] + h.bloques for h in a.hijos), []),
                           carpeta / "GUIA_DOCENTE.md", clase="profe", menu=f"Profesor: {a.titulo}")

    # Agenda: unidades y horario
    tarjetas_ = "".join(f'<a class="tarjeta" href="#/u{a.numero.replace(".", "-")}"><span class="n">{a.numero}</span>'
                        f'<span class="t">{en_linea(a.nombre)}</span></a>' for a in unidades)
    secciones.append(f'<section class="agenda" id="agenda" data-menu="Contenido de la sesión"><header class="cabecera">'
                     f'<p class="antetitulo">Sesión {n} · {html.escape(modulos_texto(ctx, s))}</p><h2>Contenido de la sesión</h2></header>'
                     f'<div class="cuerpo"><div class="tarjetas n{len(unidades)}">{tarjetas_}</div></div></section>')
    agenda_md = md_agenda_sesion(ctx, s).split("\n\n", 1)[1]
    secciones += grupo(ctx, f"Sesión {n} · {fecha_larga(s)}", "Agenda del día", partir_bloques(agenda_md), readme, menu="Agenda del día", ident="horario")

    for a in apartados:
        if a.numero:
            ident = f"u{a.numero.replace('.', '-')}"
            nota = notas.get(a.numero, "")
            secciones.append(divisor(a.numero, a.nombre, [h.titulo for h in a.hijos], ident, notas=nota))
            if nota:
                secciones.append(diapositiva(ctx, f"Guía docente · {a.numero}", f"Notas para {a.numero}", [], readme, clase="profe")
                                 .replace('<div class="cuerpo"></div>', f'<div class="cuerpo">{nota}</div>'))
            secciones += grupo(ctx, a.titulo, a.nombre, a.bloques, readme)
            for h in a.hijos:
                secciones += grupo(ctx, a.titulo, h.titulo, h.bloques, readme)
        else:
            bloques = a.bloques + sum(([f"**{h.titulo}**"] + h.bloques for h in a.hijos), [])
            secciones += grupo(ctx, f"Sesión {n}", a.titulo, bloques, readme, menu=a.titulo)

    # Laboratorio guiado
    ej_readme = carpeta / "ejercicios" / "README.md"
    if ej_readme.exists():
        t, intro_ej, ap_ej = estructurar(leer(ej_readme))
        ap_ej = [a for a in ap_ej if not a.titulo.startswith("Práctica de equipo")]
        secciones.append(divisor("Lab", "Laboratorio guiado", [a.titulo for a in ap_ej], "laboratorio",
                                 clase="especial seccion practica", menu="Laboratorio guiado"))
        if intro_ej:
            secciones += grupo(ctx, "Laboratorio guiado", "Cómo se trabaja", intro_ej, ej_readme, clase="ejercicio")
        for a in ap_ej:
            bloques = a.bloques + sum(([f"**{h.titulo}**"] + h.bloques for h in a.hijos), [])
            secciones += grupo(ctx, "Laboratorio guiado", a.titulo, bloques, ej_readme, clase="ejercicio", menu=a.titulo)

    # Práctica de equipo
    practica = next((carpeta / "ejercicios").glob("PRACTICA_*.md"), None)
    if practica:
        t, intro_p, ap_p = estructurar(leer(practica))
        secciones.append(divisor("Equipo", re.sub(r"^Práctica \d+\.\s*", "", t), [a.titulo for a in ap_p], "practica",
                                 clase="especial seccion practica", menu="Práctica de equipo"))
        if intro_p:
            secciones += grupo(ctx, t, "Entregables de hoy", intro_p, practica, clase="ejercicio")
        for a in ap_p:
            secciones += grupo(ctx, t, a.titulo, a.bloques, practica, clase="ejercicio", menu=a.titulo)
            for h in a.hijos:
                secciones += grupo(ctx, f"{t} · {a.titulo}", h.titulo, h.bloques, practica, clase="ejercicio")

    # Repaso y material del profesor
    for a in guia_repaso:
        secciones.append(f'<section id="repaso" data-menu="Preguntas de repaso"><header class="cabecera"><p class="antetitulo">'
                         f'Cierre · sesión {n}</p><h2>Preguntas de repaso</h2></header><div class="cuerpo">'
                         f'{tarjetas_repaso(a.bloques)}</div></section>')
    for a in guia_final:
        bloques = a.bloques + sum(([f"**{h.titulo}**"] + h.bloques for h in a.hijos), [])
        secciones += grupo(ctx, f"Guía docente · sesión {n}", a.titulo, bloques, carpeta / "GUIA_DOCENTE.md",
                           clase="profe", menu=f"Profesor: {a.titulo}")

    # Fin
    if n < len(ctx.sesiones):
        sig = ctx.sesiones[n]
        boton = (f'<a class="boton" href="sesion_{n + 1:02d}.html">Sesión {n + 1}. {html.escape(sig["titulo"])} '
                 f'<span aria-hidden="true">→</span></a>')
    else:
        boton = '<a class="boton" href="index.html">Volver a la presentación del curso <span aria-hidden="true">→</span></a>'
    secciones.append(f'<section class="especial inicio" id="fin" data-menu="Fin de la sesión" data-transition="fade">'
                     f'<div class="portada final"><div class="formas" aria-hidden="true"><i></i><i></i><i></i></div>'
                     f'<p class="modulo">Fin de la sesión {n}</p><h1>{en_linea(titulo_corto)}</h1><div class="acciones">{boton}'
                     f'<a class="boton secundario" href="index.html">Índice del curso</a>'
                     f'<a class="boton secundario" href="#/agenda">Volver al contenido</a></div></div></section>')
    otros = '<a href="index.html">Índice del curso</a>' + (f' · <a href="sesion_{n + 1:02d}.html">Sesión {n + 1} →</a>'
                                                            if n < len(ctx.sesiones) else "")
    return documento_presentacion(ctx, f"Sesión {n}. {titulo_corto}", secciones, otros)


def documento_presentacion(ctx: Contexto, titulo: str, secciones: list[str], otros: str) -> str:
    usa_mermaid = any('class="mermaid"' in s for s in secciones)
    clase = "profesor" if ctx.profesor else "alumnos"
    boton_modo = '<button type="button" data-accion="modo" title="Ocultar o mostrar las diapositivas del profesor">Modo clase</button>\n' \
        if ctx.profesor else ""
    mermaid = ""
    if usa_mermaid:
        mermaid = f"""<script src="{MERMAID_JS}"></script>
<script>
(function () {{
  // Los diagramas se dibujan fuera de la diapositiva (sin la escala de reveal.js) para que
  // mermaid mida bien los textos, y después se insertan ya dibujados.
  if (!window.mermaid) {{ return; }}
  var fuente = getComputedStyle(document.querySelector(".reveal")).fontFamily;
  mermaid.initialize({{ startOnLoad: false, theme: "default", fontFamily: fuente, themeVariables: {{ fontFamily: fuente, fontSize: "16px" }} }});
  document.querySelectorAll("pre.mermaid").forEach(function (pre, i) {{
    mermaid.render("diagrama-" + i, pre.textContent).then(function (r) {{
      var div = document.createElement("div");
      div.className = "diagrama";
      div.innerHTML = r.svg;
      pre.replaceWith(div);
      var seccion = div.closest("section");
      if (window.cursoAjustar && seccion) {{ window.cursoAjustar(seccion); }}
    }});
  }});
}}());
</script>
<style>.reveal .diagrama {{ text-align: center; margin: 8px 0 14px; }} .reveal .diagrama svg {{ width: 100%; max-width: 100% !important; height: 370px; }}</style>"""
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(texto_plano(titulo))}</title>
<link rel="stylesheet" href="recursos/reset.css">
<link rel="stylesheet" href="recursos/reveal.css">
<link rel="stylesheet" href="recursos/tema.css">
</head>
<body class="{clase}">
<div class="reveal">
<div class="slides">
{chr(10).join(secciones)}
</div>
<div class="pie-curso"><a href="index.html" title="Índice del curso">{html.escape(texto_plano(titulo))}</a><span class="donde"></span></div>
<div class="herramientas">
{boton_modo}<button type="button" data-accion="menu" title="Índice de la presentación (M)">☰ Índice</button>
<button type="button" data-accion="general" title="Vista general (Esc)">▦</button>
<button type="button" data-accion="pantalla" title="Pantalla completa (F)">⛶</button>
</div>
<nav class="menu" aria-label="Índice de la presentación"><p class="rotulo">{html.escape(texto_plano(titulo))}</p><ol></ol>
<p class="otros">{otros}</p></nav>
</div>
<script src="recursos/reveal.js"></script>
<script src="recursos/notes.js"></script>
<script src="recursos/search.js"></script>
<script src="recursos/zoom.js"></script>
<script src="recursos/curso.js"></script>
{mermaid}
</body>
</html>
"""


def presentacion_curso(ctx: Contexto) -> str:
    c = ctx.curso
    sesiones = ctx.sesiones
    secciones = [
        f'<section class="especial inicio" id="portada" data-menu="Portada" data-transition="fade"><div class="portada">'
        f'<div class="formas" aria-hidden="true"><i></i><i></i><i></i></div><p class="curso">Curso · {c["horas"]} horas</p>'
        f'<p class="modulo">{html.escape(c["fechas"])}</p><h1>{html.escape(c["titulo"])}</h1>'
        f'<div class="objetivo"><p>Modelos de lenguaje en local, RAG y agentes con herramientas, trazas y supervisión humana. '
        f'{c["participantes"]} personas, {len(c["equipos"])} equipos y un cliente: {html.escape(c["cliente_ficticio"])}.</p></div>'
        f'<p class="navega">Avanza con <kbd>→</kbd> o <kbd>Espacio</kbd> · <kbd>M</kbd> índice · <kbd>F</kbd> pantalla completa · '
        f'<kbd>Esc</kbd> vista general</p></div></section>'
    ]
    ficheros = len(list(ctx.raiz.glob("sesion_*/ejercicios/s*_ej*.py")))
    pruebas = sum(len(re.findall(r"^def test_", leer(p), flags=re.MULTILINE)) for p in ctx.raiz.glob("sesion_*/tests/test_*.py"))
    cifras = [(c["horas"], "horas", ""), (len(sesiones), "sesiones de 6 horas", ""), (60, "práctica", "%"),
              (len(c["equipos"]), "equipos y retos", ""), (ficheros, "ejercicios con pruebas", ""), (pruebas, "pruebas automáticas", "")]
    secciones.append('<section id="cifras" data-menu="El curso en cifras"><header class="cabecera"><p class="antetitulo">Presentación</p>'
                     '<h2>El curso en cifras</h2></header><div class="cuerpo"><div class="cifras grandes">' +
                     "".join(f'<div class="cifra"><b><span data-cuenta="{v}">{v}</span>{suf}</b><span>{t}</span></div>' for v, t, suf in cifras) +
                     "</div></div></section>")
    dias = []
    for s in sesiones:
        barras = "".join(f"<i class={m.lower()}>{m}</i>" for m, _ in s["modulos"])
        detalle = f"{s['titulo']} · {horario(s)} · {s['modalidad']}"
        dias.append(f'<button type="button" class="dia" data-detalle="{html.escape(detalle)}"><span class="s">Sesión {s["n"]}</span>'
                    f'<span class="f">{fecha_corta(s)}</span><span class="barras">{barras}</span></button>')
    secciones.append(f'<section id="calendario" data-menu="Calendario"><header class="cabecera"><p class="antetitulo">{html.escape(c["fechas"])}</p>'
                     f'<h2>Calendario</h2></header><div class="cuerpo"><p class="ayuda">Pasa el ratón o haz clic en una sesión para ver su contenido.</p>'
                     f'<div class="calendario">{"".join(dias)}</div><div class="detalle-dia" aria-live="polite">'
                     f'Catorce sesiones de seis horas. Presenciales: {", ".join(fecha_corta(s) for s in sesiones if s["modalidad"] == "Presencial")}.'
                     f'</div></div></section>')
    modulos = "".join(f'<a class="tarjeta" href="sesion_{next(s["n"] for s in sesiones if any(i == m["id"] for i, _ in s["modulos"])):02d}.html">'
                      f'<span class="n">{m["id"]}</span><span class="t">{html.escape(m["nombre"])}</span><span class="tiempo">{m["horas"]} h</span></a>'
                      for m in c["modulos"])
    secciones.append(f'<section class="agenda" id="modulos" data-menu="Módulos"><header class="cabecera"><p class="antetitulo">Programa oficial</p>'
                     f'<h2>Módulos</h2></header><div class="cuerpo"><p class="ayuda">Haz clic en un módulo para abrir su primera sesión.</p>'
                     f'<div class="tarjetas n{len(c["modulos"])}">{modulos}</div></div></section>')
    mitad = (len(sesiones) + 1) // 2
    for parte, tramo in enumerate((sesiones[:mitad], sesiones[mitad:]), 1):
        tarj_sesiones = "".join(f'<a class="tarjeta" href="sesion_{s["n"]:02d}.html"><span class="n">{s["n"]}</span>'
                                f'<span class="t">{html.escape(s["titulo"])}</span><span class="tiempo">{fecha_corta(s)} · {s["modalidad"]}</span></a>'
                                for s in tramo)
        ident = ' id="sesiones" data-menu="Sesiones"' if parte == 1 else ""
        secciones.append(f'<section class="agenda"{ident}><header class="cabecera"><p class="antetitulo">Presentaciones · haz clic para abrir</p>'
                         f'<h2>Sesiones {tramo[0]["n"]} a {tramo[-1]["n"]} <span class="parte">{parte}/2</span></h2></header>'
                         f'<div class="cuerpo"><div class="tarjetas n{len(tramo)}">{tarj_sesiones}</div></div></section>')
    equipos = "".join(f'<div class="tarjeta"><span class="n">{html.escape(e["id"])}</span><span class="t"><b>{html.escape(e["reto"])}</b><br>'
                      f'{html.escape(e["descripcion"])}</span></div>' for e in c["equipos"])
    secciones.append(f'<section id="equipos" data-menu="Equipos y retos"><header class="cabecera"><p class="antetitulo">{html.escape(c["cliente_ficticio"])}</p>'
                     f'<h2>Tres equipos, tres retos</h2></header><div class="cuerpo"><div class="tarjetas n3">{equipos}</div></div></section>')
    secciones += grupo(ctx, "Proyecto", "Hitos", partir_bloques(tabla_md(["Hito", "Sesiones", "Entregables"],
                       [[f"{h['id']} · {h['nombre']}", h["sesiones"], h["entregables"]] for h in c["hitos"]])),
                       ctx.raiz / "README.md", menu="Hitos")
    pesos = "".join(f'<div class="peso"><span class="r">{html.escape(e["componente"])}</span><span class="pista-barra">'
                    f'<i style="--valor:{e["peso"]}%"></i></span><b><span data-cuenta="{e["peso"]}">{e["peso"]}</span> %</b></div>'
                    for e in c["evaluacion"])
    secciones.append(f'<section id="evaluacion" data-menu="Evaluación"><header class="cabecera"><p class="antetitulo">Cómo se califica</p>'
                     f'<h2>Evaluación</h2></header><div class="cuerpo"><div class="pesos">{pesos}</div>'
                     f'<p>Cada práctica de equipo se puntúa con cuatro criterios de 0 a 3. El proyecto final se defiende ante un comité el 23 de diciembre.</p>'
                     f'</div></section>')
    secciones.append('<section class="especial inicio" id="fin" data-menu="Empezamos" data-transition="fade"><div class="portada final">'
                     '<div class="formas" aria-hidden="true"><i></i><i></i><i></i></div><p class="modulo">Empezamos</p>'
                     f'<h1>Sesión 1. {html.escape(sesiones[0]["titulo"])}</h1><div class="acciones">'
                     '<a class="boton" href="sesion_01.html">Abrir la sesión 1 <span aria-hidden="true">→</span></a>'
                     '<a class="boton secundario" href="#/sesiones">Ver todas las sesiones</a></div></div></section>')
    return documento_presentacion(ctx, c["titulo"], secciones, '<a href="../index.html">Apuntes del curso</a>')


# ---------------------------------------------------------------------------------------- construcción


def construir(ctx: Contexto) -> None:
    if ctx.docs.exists():
        shutil.rmtree(ctx.docs)
    (ctx.docs / "presentacion").mkdir(parents=True)
    shutil.copytree(PLANTILLA / "presentacion_recursos", ctx.docs / "presentacion" / "recursos")

    lista = paginas(ctx)
    ctx.paginas = {p.origen.resolve(): p.destino for p in lista if p.transformar is None}
    ctx.paginas[(ctx.raiz / "plantillas").resolve()] = "plantillas.html"
    for p in lista:
        texto = leer(p.origen)
        if p.transformar:
            texto = p.transformar(texto)
        cuerpo, toc, mermaid = md_a_html(ctx, texto, p.origen)
        escribir(ctx.docs / p.destino, pagina_doc(ctx, p.titulo, cuerpo, toc, p.nav, p.pie, mermaid, p.ficha, p.profesor))
    cuerpo, toc, mermaid = pagina_plantillas(ctx)
    escribir(ctx.docs / "plantillas.html", pagina_doc(ctx, "Plantillas", reescribir_enlaces(ctx, cuerpo, ctx.raiz / "plantillas" / "x.md"),
                                                       toc, pie='<a href="index.html">Índice del curso</a>', mermaid=mermaid))
    escribir(ctx.docs / "index.html", pagina_indice(ctx))
    for s in ctx.sesiones:
        escribir(ctx.docs / "presentacion" / f"sesion_{s['n']:02d}.html", presentacion_sesion(ctx, s))
    escribir(ctx.docs / "presentacion" / "index.html", presentacion_curso(ctx))
    escribir(ctx.docs / ".nojekyll", "")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--raiz", type=Path, default=HERRAMIENTAS.parent)
    parser.add_argument("--comprobar", action="store_true", help="Solo valida el calendario y las guías")
    args = parser.parse_args()
    raiz = args.raiz.resolve()
    ctx = Contexto(raiz, json.loads(leer(raiz / "curso.json")), (raiz / "GUIA_DOCENTE.md").exists())
    avisos = validar(ctx)
    for aviso in avisos:
        print(f"AVISO: {aviso}")
    if args.comprobar:
        sys.exit(1 if avisos else 0)
    cambios = actualizar_readmes(ctx)
    construir(ctx)
    total = len(list(ctx.docs.rglob("*.html")))
    version = "profesor" if ctx.profesor else "alumnado"
    print(f"Versión {version}: {cambios} README actualizados, {total} páginas HTML en {ctx.docs}")
    print("Calendario correcto." if not avisos else f"{len(avisos)} avisos en el calendario: revísalos.")


if __name__ == "__main__":
    main()
