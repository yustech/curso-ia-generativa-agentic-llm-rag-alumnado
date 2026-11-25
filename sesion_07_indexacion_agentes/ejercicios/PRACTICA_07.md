# Práctica 7. Índice consultable, checklist de calidad y ficha de patrón del agente

Entregables del equipo: `rag/ingesta.py`, `docs/checklist_rag.md`, `docs/ficha_patron_agente.md` y la presentación de la revisión intermedia.

## Parte 1. Índice consultable con checklist (laboratorio de M4)

1. Adaptad el pipeline del ejercicio 1 a las fuentes de vuestro reto en `rag/ingesta.py`, con la configuración ganadora de la sesión 6.
2. Evaluad vuestro RAG con vuestro conjunto de preguntas (`evals/preguntas_recuperacion.jsonl`, más al menos 3 preguntas sin fuente) usando el código del ejercicio 2.
3. Escribid `docs/checklist_rag.md` con la tabla del checklist (criterio, valor, umbral, ¿cumple?) y, para cada criterio que no se cumpla, la causa y la acción prevista.

## Parte 2. Reto: clasificación de soluciones y ficha de patrón (80 min)

### 1. Clasificación de soluciones (25 min)

Para cada una de estas ocho situaciones, decidid si es mejor un **chatbot con RAG**, un **workflow** o un **agente**, y qué patrón de los apuntes (7.4) aplicaríais. Justificadlo en una línea.

| N.º | Situación |
| --- | --- |
| 1 | Responder a la plantilla dudas sobre la política de teletrabajo |
| 2 | Cada viernes, a partir de las actas de la semana, generar el informe de estado con la estructura fija de la metodología |
| 3 | Investigar por qué el pipeline de Faro falla de forma intermitente, consultando registros, cambios recientes y documentación |
| 4 | Clasificar los correos de clientes y enviar cada uno al equipo correspondiente |
| 5 | Atender una petición de entorno que puede venir incompleta, incumplir la política o requerir aprobación del CAB |
| 6 | Traducir al inglés la guía de estilo |
| 7 | Revisar una merge request desde tres puntos de vista (estilo, seguridad y pruebas) y combinar las observaciones |
| 8 | Redactar una historia de usuario y revisarla contra la definición de preparado hasta que la cumpla |

### 2. Ficha de patrón del agente del equipo (55 min)

Rellenad `docs/ficha_patron_agente.md` a partir de la plantilla `plantillas/ficha_patron_agente.md`:

- **Patrón elegido** (workflow, enrutador, agente con herramientas…) y por qué no uno más simple.
- **Objetivo** del asistente en una frase.
- **Herramientas** previstas, separando las de solo lectura de las que modifican algo.
- **Bucle**: máximo de pasos, cuándo termina, qué hace si una herramienta falla.
- **Puntos de intervención humana**.
- **Diagrama** en Mermaid del flujo.

## Revisión intermedia presencial (cierre, 8 min por equipo)

Cada equipo presenta:

1. Su RAG funcionando en directo con dos preguntas: una con respuesta y una sin ella.
2. El checklist de calidad: qué cumple y qué no.
3. La ficha de patrón del agente.

El docente y los otros dos equipos dan una valoración rápida: un acierto y una mejora.

## Entrega

1. `rag/ingesta.py` y el índice reproducible (instrucciones en el README del equipo).
2. `docs/checklist_rag.md`.
3. `docs/clasificacion_soluciones.md` con las 8 situaciones.
4. `docs/ficha_patron_agente.md`.
5. Commit: `Sesión 7: índice, checklist y ficha de patrón del agente`.

## Criterios de evaluación (0 a 3 puntos cada uno)

| Criterio | 3 puntos |
| --- | --- |
| Índice | Ingesta incremental funcionando sobre las fuentes del reto |
| Checklist | Métricas reales, umbrales justificados y acciones para lo que no cumple |
| Clasificación | Decisiones razonadas que eligen el sistema más simple suficiente |
| Ficha de patrón | Completa, coherente con el reto y con los puntos humanos bien situados |
