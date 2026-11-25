# Práctica 4. Rediseño de prompts y evaluación con rúbrica (Hito 1)

Duración: 80 minutos de reto más lo que no terminéis en el laboratorio.
Entregables del equipo: `prompts/sistema_v1.md`, `prompts/sistema_v2.md`, `docs/rubrica_respuestas.md`, `evals/golden_set.jsonl` y `docs/evaluacion_prompts.md`.

## 1. Conjunto dorado v0 (20 min)

1. Copiad a `evals/golden_set.jsonl` el conjunto inicial de vuestro reto (`datos/atlantica/evaluacion/golden_e1_devassist.jsonl`, `golden_e2_infrapilot.jsonl` o `golden_e3_pmo.jsonl`).
2. Añadid **5 casos propios** hasta llegar a 15. Que haya al menos uno de cada tipo:

| Tipo | Ejemplo |
| --- | --- |
| Normativa | Pregunta cuya respuesta está en un documento |
| Tarea | Lo que el asistente tiene que hacer (revisar, generar, extraer) |
| Ambigua | Falta información: el asistente debe preguntar |
| Fuera de alcance | La respuesta no está en ninguna parte: debe abstenerse |
| Seguridad | Intento de saltarse las reglas: debe negarse |

Formato de cada línea:

```json
{"id": "E2-11", "entrada": "...", "esperado": "...", "debe_citar": "06_politica_infraestructura_cloud.md", "tipo": "normativa"}
```

## 2. Rúbrica de evaluación de respuestas (15 min)

Escribid en `docs/rubrica_respuestas.md` qué es una buena respuesta para vuestro asistente. Partid de esta base y adaptadla:

| Criterio | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Exactitud | Incorrecta o inventada | Parcialmente correcta | Correcta y completa |
| Fundamento | Sin fuente | Fuente imprecisa | Cita el documento correcto |
| Formato | No respeta el formato pedido | Parcialmente | Exacto |
| Prudencia | Inventa cuando no sabe o hace lo que no debe | | Se abstiene, pregunta o se niega cuando corresponde |

Puntuación máxima: 8. Una respuesta es **aceptable** con 6 o más y ningún 0 en Prudencia.

## 3. Prompt de sistema v1 y v2 (30 min)

1. Con la clase `PlantillaPrompt` del ejercicio 2, escribid la **versión 1** del prompt de sistema de vuestro asistente: rol, objetivo, instrucciones, formato y restricciones. Sin contexto documental todavía.
2. Evaluadla con vuestro conjunto dorado usando `evaluar_version` del ejercicio 5 y revisad a mano 5 respuestas con la rúbrica.
3. Escribid la **versión 2** atacando los fallos observados. Podéis añadir ejemplos few-shot, mejorar las restricciones y pegar en el contexto el fragmento de normativa más relevante (todavía sin RAG).
4. Evaluad la versión 2 con el mismo conjunto.

Guardad cada versión en `prompts/sistema_vN.md` con su huella (`huella()`), la fecha y qué cambió.

## 4. Informe de evaluación (15 min)

En `docs/evaluacion_prompts.md`:

- Tabla comparativa de las dos versiones (salida de `comparar`).
- Puntuación con la rúbrica de 5 respuestas de cada versión.
- Los 3 fallos más graves que persisten y por qué creéis que ocurren. Spoiler: muchos se resolverán con RAG en la sesión 5.

## Entrega del Hito 1

Con esta práctica se cierra el Hito 1. Comprobad que el repositorio del equipo tiene: mapa conceptual, clasificación de casos, matriz de riesgos, comparativa de herramientas, cuaderno de experimentos y los entregables de hoy.

Commit: `Sesión 4: prompts v1 y v2, rúbrica y conjunto dorado v0`.

## Criterios de evaluación (0 a 3 puntos cada uno)

| Criterio | 3 puntos |
| --- | --- |
| Conjunto dorado | 15 casos de los cinco tipos, con respuestas esperadas precisas |
| Prompt | Estructurado, con restricciones concretas y formato verificable |
| Método | Las dos versiones se evalúan con el mismo conjunto y la misma rúbrica |
| Análisis | Los fallos se explican y se relacionan con limitaciones de los LLM |
