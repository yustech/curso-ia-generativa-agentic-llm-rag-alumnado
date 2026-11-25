# Sesión 14. Proyecto final: demo, defensa y evaluación

<!-- cabecera:inicio -->
| Fecha | Horario | Modalidad | Módulos | Hito |
| --- | --- | --- | --- | --- |
| Miércoles 23 de diciembre de 2026 | 09:00-15:00 | Presencial | M7 · Proyecto final y evaluación (6 h) | H4 · Aplicación y proyecto |

**Objetivo:** Demostrar una solución funcional, argumentar decisiones y valorar calidad, riesgos y mejoras.
<!-- cabecera:fin -->

Último día del curso, presencial. Por la mañana terminas y pruebas el asistente de tu equipo y lo presentas ante un comité como si fuera un cliente. Por la tarde haces la prueba individual y una defensa breve de las decisiones técnicas. Cerramos con una retrospectiva del curso.

<!-- agenda:inicio -->
### Agenda de la sesión

| Hora | Min | Tipo | Bloque |
| --- | --- | --- | --- |
| 09:00 | 15 | Teoría | Activación: orden del día y criterios |
| 09:15 | 100 | Práctica | Finalización, pruebas y ensayo |
| 10:55 | 10 | Pausa | Pausa |
| 11:05 | 90 | Práctica | Demo Day: 3 equipos × (15 min de demo + 15 min de preguntas) |
| 12:35 | 16 | Práctica | Evaluación entre pares |
| 12:51 | 60 | Teoría | Prueba individual teórico-práctica |
| 13:51 | 45 | Teoría | Defensa individual de decisiones |
| 14:36 | 24 | Teoría | Retrospectiva y cierre del curso |

Teoría: 2 h 24 min · práctica: 3 h 36 min (las pausas computan en el bloque práctico).
<!-- agenda:fin -->

## Lo que entregas hoy

| Entregable | Dónde | Quién |
| --- | --- | --- |
| MVP del asistente | Repositorio del equipo, etiqueta `v1.0` | Equipo |
| Documentación reproducible | `README.md`, `docs/` | Equipo |
| Presentación | `docs/presentacion.md` (o el formato del equipo) | Equipo |
| Informe de evaluación | `docs/informe_evaluacion.md` | Equipo |
| Prueba individual | En papel o en el formulario que indique el docente | Cada persona |

El enunciado completo y la rúbrica del proyecto están en [`proyecto_final/README.md`](../proyecto_final/README.md).

---

## 14.1 Orden del día

| Hora | Qué | Detalle |
| --- | --- | --- |
| 09:00 | Activación | Orden del día, criterios y turnos de la demo |
| 09:15 | Finalización y pruebas | Último ciclo de evaluación, congelación del código, etiqueta `v1.0`, ensayo |
| 10:55 | Pausa | |
| 11:05 | Demo Day | Tres equipos × (15 min de demo + 15 min de preguntas del comité) |
| 12:35 | Evaluación entre pares | Cada persona valora a los otros dos equipos y a su propio equipo |
| 12:51 | Prueba individual | 60 minutos |
| 13:51 | Defensa individual | 3-4 minutos por persona: una pregunta sobre una decisión del proyecto |
| 14:36 | Retrospectiva y cierre | Qué te llevas, qué harías distinto, próximos pasos |

## 14.2 Checklist final del MVP (antes de las 10:45)

- [ ] `python comprobar_entorno.py` sin errores en el portátil de la demo.
- [ ] El asistente arranca con una sola orden documentada en el README (`streamlit run app.py`).
- [ ] El índice del RAG se reconstruye con una orden documentada.
- [ ] `pytest tests -v` en verde.
- [ ] Evaluación final ejecutada sobre el conjunto dorado (30 o más casos) y resultados en `docs/informe_evaluacion.md`, comparados con la línea base.
- [ ] Red teaming ejecutado y resultados en el informe.
- [ ] Las acciones con efectos piden confirmación humana.
- [ ] No hay `.env`, claves ni datos personales en el repositorio.
- [ ] `python sesion_14_proyecto_final/ejercicios/s14_ej1_verificar_entrega.py <repositorio>` devuelve «Entrega completa: sí».
- [ ] Commit final y etiqueta: `git tag v1.0 && git push --tags`.
- [ ] **Plan B de la demo**: capturas o un vídeo corto por si falla algo en directo, y el modelo descargado en local por si falla la red.

## 14.3 Estructura de la demo (15 minutos)

| Minutos | Contenido |
| --- | --- |
| 0-2 | El problema del cliente y a quién ayuda el asistente (con los números del AS-IS) |
| 2-4 | La solución en una diapositiva: arquitectura y decisiones clave |
| 4-10 | **Demo en directo**: un caso normal, un caso que requiere herramienta y confirmación humana, un caso sin respuesta (abstención) y un intento de ataque |
| 10-13 | Cómo sabemos que funciona: métricas de evaluación, seguridad y rendimiento, y sus límites |
| 13-15 | Valor de negocio, riesgos pendientes y siguientes pasos |

Consejos: empieza por el problema, no por la tecnología; enseña también lo que **no** funciona y cómo lo controláis; reparte la palabra entre las cuatro personas.

## 14.4 Preguntas típicas del comité

- ¿Qué pasa si el modelo se equivoca en este caso? ¿Quién lo detecta?
- ¿Por qué un agente y no un workflow (o al revés)?
- ¿Cómo sabéis que la versión de hoy es mejor que la de hace una semana?
- ¿Qué datos salen del portátil o del servidor? ¿Qué clasificación tienen?
- ¿Cuánto costaría en producción para 200 usuarios? ¿Qué motor usaríais?
- ¿Qué haríais con dos semanas más?
- ¿Qué decisión técnica cambiaríais si empezarais hoy?

## 14.5 Prueba individual

60 minutos, sin conexión al modelo. Consta de preguntas de respuesta corta y de casos prácticos sobre todo el temario (fundamentos, prompting, RAG, agentes, aplicaciones, seguridad y evaluación). Cuenta un 20 % de la nota del curso junto con la defensa individual.

Para prepararla: repasa las preguntas de repaso del cierre de cada sesión y las tablas de «Errores frecuentes» de los apuntes.

## 14.6 Defensa individual

El comité hace a cada persona una pregunta sobre una decisión del proyecto en la que haya participado («¿por qué elegisteis esa estrategia de troceado?», «¿qué hace vuestro agente si la herramienta falla?»). Se valora que la respuesta sea concreta, con datos, y que reconozca las alternativas.

## 14.7 Evaluación del curso

| Componente | Peso | Evidencias |
| --- | --- | --- |
| Laboratorios y entregables de sesión | 40 % | Los entregables de las 14 sesiones |
| Proyecto final integrador | 40 % | MVP, arquitectura, pruebas, trazabilidad y presentación |
| Evaluación individual | 20 % | Prueba teórico-práctica y defensa de decisiones |

## 14.8 Y después del curso

Lo que has construido es el esqueleto de muchos proyectos reales: un asistente con RAG, herramientas con contrato, guardarraíles, evaluación continua y una interfaz. Para seguir:

- Cambia el modelo por uno mayor del servidor y vuelve a ejecutar la evaluación: ¿cuánto mejora y cuánto cuesta?
- Sustituye la base vectorial embebida por pgvector o Qdrant.
- Despliega el asistente con Docker y vLLM.
- Añade observabilidad con OpenTelemetry o una herramienta como Langfuse.
- Lee las fichas de los modelos nuevos que vayan saliendo con los criterios de la sesión 3, y evalúa antes de cambiar.
