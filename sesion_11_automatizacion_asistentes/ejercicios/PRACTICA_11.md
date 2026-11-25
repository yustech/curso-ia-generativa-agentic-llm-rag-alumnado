# Práctica 11. Proceso AS-IS / TO-BE, backlog priorizado y primer incremento del asistente

Entregables del equipo: `docs/proceso_as_is_to_be.md`, `docs/backlog_asistente.md` y `app.py`.

## Parte 1. Mapa AS-IS / TO-BE del proceso del reto (laboratorio de M5, 60 min)

1. **AS-IS (25 min).** Modelad con `Proceso` y `Paso` el proceso actual que vuestro asistente va a cambiar. Usad la información de los documentos de Atlántica y, si podéis, la experiencia de alguien del grupo que haya hecho una tarea parecida.

| Reto | Proceso |
| --- | --- |
| R1 · DevAssist | Revisión de una merge request y escritura de sus pruebas |
| R2 · InfraPilot | Desde la petición de un entorno hasta la solicitud aprobada en el CAB |
| R3 · PMO Copilot | Desde las actas de la semana hasta el informe de estado enviado |

2. **TO-BE (20 min).** El proceso con vuestro asistente: pasos de IA, pasos automáticos y controles humanos. `avisos(to_be)` debe devolver una lista vacía.
3. **Comparación (15 min).** Tabla de `comparar`, diagramas Mermaid de los dos procesos y tres líneas sobre qué supuestos hay detrás de los tiempos del TO-BE (en especial, el tiempo de revisión).

## Parte 2. Reto: primer incremento del asistente y backlog priorizado (80 min)

### 1. Backlog (20 min)

Escribid entre 10 y 15 historias para vuestro asistente, con valor, esfuerzo y MoSCoW, e incluid obligatoriamente historias de evaluación y de seguridad. Priorizadlas con el ejercicio 4 y planificad los sprints que quedan hasta el Demo Day (capacidad: lo que el equipo puede hacer en las sesiones 12 a 14). El resultado va a `docs/backlog_asistente.md`.

### 2. Primer incremento (60 min)

Construid `app.py` en el repositorio del equipo: una interfaz Streamlit para **vuestro** asistente, a partir del ejercicio 3, con:

- bienvenida transparente adaptada al reto;
- vuestro RAG (sesiones 5-7) y al menos una herramienta del reto (sesión 9);
- fuentes visibles en cada respuesta;
- un botón o diálogo de **confirmación humana** para las acciones con efectos (InfraPilot: registrar la solicitud; PMO Copilot: actualizar el backlog). Pista: guardad la acción pendiente en `st.session_state` y mostrad «Aprobar» y «Rechazar» con `st.button`;
- un pequeño panel lateral con el número de mensajes en memoria y las herramientas usadas en el último turno.

## Cierre: demo rápida (3 minutos por equipo)

Cada equipo enseña su aplicación con una pregunta de su conjunto dorado y una acción con confirmación.

## Entrega

1. `docs/proceso_as_is_to_be.md` con los dos diagramas y la comparación.
2. `docs/backlog_asistente.md` priorizado y planificado.
3. `app.py` funcionando con `streamlit run app.py`.
4. Commit: `Sesión 11: proceso, backlog y primer incremento del asistente`.

## Criterios de evaluación (0 a 3 puntos cada uno)

| Criterio | 3 puntos |
| --- | --- |
| Análisis del proceso | AS-IS realista, TO-BE sin avisos y supuestos explicitados |
| Backlog | Historias con criterios, priorizadas y con evaluación y seguridad como *Must* |
| Prototipo | Interfaz con RAG, herramienta, fuentes y transparencia |
| Supervisión humana | Confirmación con información suficiente para decidir |
