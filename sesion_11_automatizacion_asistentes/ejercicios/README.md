# Sesión 11. Laboratorio guiado

Completa cada fichero sustituyendo los `raise NotImplementedError` por tu código. Comprueba tu trabajo con:

```bash
pytest sesion_11_automatizacion_asistentes -v
```

## Ejercicio 1. Proceso AS-IS / TO-BE (laboratorio de M5, 35 min)

Fichero: `s11_ej1_proceso.py`

1. `tiempo_total(proceso)` y `porcentaje_automatizado(proceso)`.
2. `avisos(proceso)`: las dos reglas de diseño del TO-BE.
3. `comparar(as_is, to_be)`.
4. `a_mermaid(proceso)`: con la forma de cada tipo de paso.

El fichero incluye el ejemplo del informe semanal. Ejecútalo y pega el diagrama en un `.md` para verlo en VS Code o en GitHub.

## Ejercicio 2. El núcleo de un asistente (laboratorio de M6, 35 min)

Fichero: `s11_ej2_asistente.py`

1. `necesita_humano(mensaje)`.
2. `Asistente.bienvenida()`: transparente.
3. `Asistente._contexto(pregunta)`.
4. `Asistente.responder(mensaje)`: escalado, memoria de ventana, contexto y fuentes citadas. En el historial se guarda el mensaje **original** del usuario, no el que lleva los fragmentos (si no, la memoria se llenaría de documentos).

Prueba el asistente en la consola: `python sesion_11_automatizacion_asistentes/ejemplos/01_chat_consola.py`.

## Ejercicio 3. Interfaz con Streamlit (laboratorio de M6, 31 min)

Fichero: `s11_ej3_app.py`

1. `obtener_asistente()`: un asistente por sesión del navegador, en `st.session_state`.
2. `dibujar_mensaje(mensaje)`.

Lanza la aplicación:

```bash
streamlit run sesion_11_automatizacion_asistentes/ejercicios/s11_ej3_app.py
```

Haz tres preguntas, una de ellas sin respuesta en la documentación, y pide «hablar con una persona». Pulsa «Nueva conversación».

## Ejercicio 4. Priorizar el backlog del asistente (reto, 15 min)

Fichero: `s11_ej4_backlog.py`

1. `puntuacion(h)` y `priorizar(historias)`.
2. `planificar_sprints(historias, capacidad, max_sprints)`.
3. `a_markdown(historias)`.

Úsalo en la práctica con el backlog de tu asistente.

## Práctica de equipo

El enunciado está en [`PRACTICA_11.md`](PRACTICA_11.md).
