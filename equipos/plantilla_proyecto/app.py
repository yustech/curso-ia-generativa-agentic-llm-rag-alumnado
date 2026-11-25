"""Interfaz del asistente del equipo: ``streamlit run app.py``.

Muestra la respuesta, las fuentes y los pasos del agente. Las acciones con
efectos solo se ejecutan si la persona activa la casilla de autorización
(en la sesión 11 podéis sustituirlo por una confirmación acción a acción).
"""

from __future__ import annotations

import streamlit as st

import entorno  # noqa: F401
from agente.asistente import responder
from comun import llm

st.set_page_config(page_title="Asistente <reto>", page_icon="🤖")
st.title("Asistente <reto>")
st.caption("Atlántica Logística · respuestas generadas por IA con modelos locales: revisa las fuentes antes de actuar.")

with st.sidebar:
    st.subheader("Configuración")
    st.write(llm.describir_configuracion())
    autorizar = st.checkbox("Autorizo las acciones con efectos de la próxima consulta", value=False)
    if st.button("Nueva conversación"):
        st.session_state.historial = []

st.session_state.setdefault("historial", [])

for turno in st.session_state.historial:
    with st.chat_message(turno["rol"]):
        st.markdown(turno["texto"])

pregunta = st.chat_input("Escribe tu consulta")
if pregunta:
    st.session_state.historial.append({"rol": "user", "texto": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)
    with st.chat_message("assistant"):
        with st.spinner("Consultando..."):
            resultado = responder(pregunta, confirmador=lambda nombre, argumentos: autorizar)
        st.markdown(resultado.respuesta)
        if resultado.pasos:
            with st.expander(f"Pasos del agente ({len(resultado.pasos)}) · {resultado.segundos:.1f} s"):
                for paso in resultado.pasos:
                    st.markdown(f"**{paso['herramienta']}** `{paso['argumentos']}`")
                    st.code(paso["resultado"][:1500])
    st.session_state.historial.append({"rol": "assistant", "texto": resultado.respuesta})
