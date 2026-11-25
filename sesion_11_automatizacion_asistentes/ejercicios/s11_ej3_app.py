"""Sesión 11 - Ejercicio 3: interfaz de chat con Streamlit.

    streamlit run sesion_11_automatizacion_asistentes/ejercicios/s11_ej3_app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from s11_ej2_asistente import Asistente, asistente_atlantica  # noqa: E402


def obtener_asistente() -> Asistente:
    """Un asistente por sesión del navegador, guardado en ``st.session_state["asistente"]``.
    Los mensajes que se muestran se guardan en ``st.session_state["mensajes"]`` como
    ``{"rol", "texto", "fuentes"}``; al crearlo, el primero es la bienvenida."""
    raise NotImplementedError("Completa este bloque")


def dibujar_mensaje(mensaje: dict) -> None:
    """Dibuja un mensaje con ``st.chat_message`` y, si tiene fuentes, un ``st.caption`` «Fuentes: a · b»."""
    raise NotImplementedError("Completa este bloque")


st.set_page_config(page_title="Faro-IA · Atlántica", page_icon="🧭")
st.title("Faro-IA")
st.caption("Asistente de IA de Atlántica Logística · datos ficticios del curso")

asistente = obtener_asistente()
with st.sidebar:
    st.subheader("Sesión")
    if st.button("Nueva conversación"):
        asistente.reiniciar()
        st.session_state["mensajes"] = [{"rol": "assistant", "texto": asistente.bienvenida(), "fuentes": []}]
    st.write(f"Mensajes en memoria: {len(asistente.historial)}")

for mensaje in st.session_state["mensajes"]:
    dibujar_mensaje(mensaje)

pregunta = st.chat_input("Escribe tu pregunta")
if pregunta:
    st.session_state["mensajes"].append({"rol": "user", "texto": pregunta, "fuentes": []})
    dibujar_mensaje(st.session_state["mensajes"][-1])
    with st.spinner("Pensando…"):
        respuesta = asistente.responder(pregunta)
    nuevo = {"rol": "assistant", "texto": respuesta.texto, "fuentes": respuesta.fuentes}
    st.session_state["mensajes"].append(nuevo)
    dibujar_mensaje(nuevo)
    if respuesta.escalado:
        st.warning("Conversación derivada a una persona.")
