"""Tests de los ejercicios de la sesión 5."""

import pytest

import s05_ej1_documentos as ej1
import s05_ej2_rag_minimo as ej2
from comun import llm

DOC = """---
titulo: Política de prueba
codigo: ATL-X-001
nota: valor: con dos puntos
---

# Política de prueba

Texto de introducción.

## 1. Primera

Contenido uno.

## 2. Vacía

## 3. Tercera

Contenido tres.
Segunda línea.
"""


# ---------------------------------------------------------------- Ejercicio 1
def test_ej1_front_matter():
    metadatos, cuerpo = ej1.leer_front_matter(DOC)
    assert metadatos == {"titulo": "Política de prueba", "codigo": "ATL-X-001", "nota": "valor: con dos puntos"}
    assert cuerpo.startswith("# Política de prueba")


def test_ej1_front_matter_ausente():
    assert ej1.leer_front_matter("# Hola\n") == ({}, "# Hola\n")


def test_ej1_cargar_documentos_reales():
    documentos = ej1.cargar_documentos()
    assert len(documentos) == 12
    assert documentos[0].nombre == "01_presentacion_empresa.md"
    assert documentos[0].titulo == "Presentación de Atlántica Logística"
    assert documentos[0].metadatos["codigo"] == "ATL-GEN-001"


def test_ej1_cargar_sin_titulo(tmp_path):
    (tmp_path / "b.md").write_text("Sin cabecera", encoding="utf-8")
    (tmp_path / "a.md").write_text("---\ntitulo: A\n---\nx", encoding="utf-8")
    documentos = ej1.cargar_documentos(tmp_path)
    assert [(d.nombre, d.titulo) for d in documentos] == [("a.md", "A"), ("b.md", "b")]


def test_ej1_trocear_por_caracteres():
    assert ej1.trocear_por_caracteres("abcdefghij", 4, 1) == ["abcd", "defg", "ghij"]
    assert ej1.trocear_por_caracteres("abcdefghijk", 4, 0) == ["abcd", "efgh", "ijk"]
    assert ej1.trocear_por_caracteres("", 4, 1) == []


@pytest.mark.parametrize("tamano, solape", [(0, 0), (4, 4), (4, -1), (4, 5)])
def test_ej1_trocear_por_caracteres_invalido(tamano, solape):
    with pytest.raises(ValueError):
        ej1.trocear_por_caracteres("texto", tamano, solape)


def test_ej1_trocear_por_secciones():
    metadatos, cuerpo = ej1.leer_front_matter(DOC)
    documento = ej1.Documento("p_politica.md", metadatos["titulo"], cuerpo, metadatos)
    trozos = ej1.trocear_por_secciones(documento)
    assert [t.seccion for t in trozos] == ["Introducción", "1. Primera", "3. Tercera"]
    assert [t.id for t in trozos] == ["p_politica#0", "p_politica#1", "p_politica#2"]
    assert trozos[2].texto == "Política de prueba — 3. Tercera\n\nContenido tres.\nSegunda línea."
    assert all(t.documento == "p_politica.md" for t in trozos)


def test_ej1_estadisticas():
    assert ej1.estadisticas(["ab", "abcd"]) == {"n": 2, "media": 3.0, "minimo": 2, "maximo": 4}
    assert ej1.estadisticas([])["n"] == 0


# ---------------------------------------------------------------- Ejercicio 2
def trozo(i, texto):
    return ej1.Trozo(f"d#{i}", "doc.md", f"Sección {i}", texto)


def test_ej2_coseno():
    assert ej2.coseno([1, 0], [1, 0]) == pytest.approx(1.0)
    assert ej2.coseno([1, 0], [0, 1]) == pytest.approx(0.0)
    assert ej2.coseno([1, 1], [-1, -1]) == pytest.approx(-1.0)
    assert ej2.coseno([0, 0], [1, 1]) == 0.0


def test_ej2_indice_recupera_el_trozo_relevante():
    indice = ej2.IndiceMemoria()
    indice.agregar([trozo(0, "vacaciones días laborables solicitud portal"),
                    trozo(1, "etiquetas obligatorias proyecto entorno nube"),
                    trozo(2, "comité de cambios jueves ventana")])
    resultados = indice.buscar("días de vacaciones", k=2)
    assert len(resultados) == 2
    assert resultados[0][0].id == "d#0"
    assert resultados[0][1] >= resultados[1][1]


def test_ej2_indice_vacio_y_agregar_una_sola_llamada(monkeypatch):
    indice = ej2.IndiceMemoria()
    assert indice.buscar("x") == []
    llamadas = []
    original = llm.embeddings
    monkeypatch.setattr(llm, "embeddings", lambda textos, **kw: llamadas.append(textos) or original(textos))
    indice.agregar([trozo(0, "a"), trozo(1, "b")])
    assert len(llamadas) == 1 and len(indice.vectores) == 2


def test_ej2_construir_mensajes():
    mensajes = ej2.construir_mensajes("¿Pregunta?", [(trozo(1, "Texto uno"), 0.9), (trozo(2, "Texto dos"), 0.5)])
    assert mensajes[0] == {"role": "system", "content": ej2.SISTEMA}
    assert mensajes[1]["content"] == "[1] doc.md › Sección 1\nTexto uno\n\n[2] doc.md › Sección 2\nTexto dos\n\nPregunta: ¿Pregunta?"


def test_ej2_fuentes_citadas():
    resultados = [(trozo(1, "a"), 0.9), (trozo(2, "b"), 0.8)]
    assert ej2.fuentes_citadas("Dato [2] y otro [1][2], fuera [7].", resultados) == ["doc.md › Sección 2", "doc.md › Sección 1"]
    assert ej2.fuentes_citadas("Sin citas", resultados) == []


def test_ej2_responder():
    indice = ej2.IndiceMemoria()
    indice.agregar([trozo(0, "vacaciones veinticinco días laborables"), trozo(1, "etiquetas nube")])
    falso = llm.usar_llm_falso(["Son 25 días laborables [1]."])
    r = ej2.responder("¿Cuántos días de vacaciones?", indice, k=2)
    assert r.fuentes == ["doc.md › Sección 0"]
    assert r.recuperados[0] == "doc.md › Sección 0" and not r.se_abstiene
    assert falso.recibidos[0][0]["content"] == ej2.SISTEMA


def test_ej2_abstencion():
    assert ej2.RespuestaRAG("No consta en la documentación.", [], []).se_abstiene
