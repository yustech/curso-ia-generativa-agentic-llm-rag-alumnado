# Práctica 6. Comparativa de estrategias de búsqueda y base vectorial del reto

Entregables del equipo: `rag/busqueda.py` (o un cuaderno `.ipynb`) y `docs/comparativa_busqueda.md`.

## Reto 1. Comparación de estrategias de búsqueda (70 min)

### 1. Preguntas de evaluación del reto (20 min)

Escribid en `evals/preguntas_recuperacion.jsonl` **al menos 15 preguntas** de vuestro reto con el documento que debería recuperarse (mismo formato que `datos/atlantica/evaluacion/preguntas_rag.jsonl`). Incluid:

- 5 preguntas con las mismas palabras que el documento.
- 5 preguntas parafraseadas o con sinónimos («¿cuándo se juntan los del CAB?»).
- 3 preguntas con códigos, siglas o identificadores (`ATL-INF-006`, `FARO-142`, `m6i.large`).
- 2 preguntas sin fuente (deben quedar fuera de los resultados relevantes).

Para PMO Copilot, añadid las actas como documentos indexables: cargadlas con `cargar_trozos(carpeta=DATOS / "proyectos" / "actas")` además de los documentos generales.

### 2. Comparativa (50 min)

Con vuestro código de los ejercicios 2 y 3, comparad al menos **cinco configuraciones** y documentad la tabla:

| Configuración | Hit@1 | Hit@3 | MRR | Fallos | Latencia media |
| --- | --- | --- | --- | --- | --- |
| BM25 | | | | | |
| Semántica (`embeddinggemma`) | | | | | |
| Híbrida RRF | | | | | |
| Semántica con trozos de 500 caracteres | | | | | |
| Una variante vuestra (otro modelo de embeddings, otro `k` de RRF, reordenación con el LLM…) | | | | | |

Para medir la latencia, usad `medir` de la sesión 2. Para probar otro modelo de embeddings: `ollama pull bge-m3` y cambiad `EMBED_MODEL` (recordad reindexar).

Analizad cada fallo: ¿es un problema de vocabulario, de troceado o de que la pregunta es ambigua?

## Reto 2. Base vectorial persistente con Chroma (56 min)

1. Cread `rag/busqueda.py` en el repositorio del equipo con una función `buscar(pregunta, k)` que use **la configuración ganadora** sobre una colección Chroma persistente con los documentos de vuestro reto.
2. Añadid filtros por metadatos útiles para vuestro reto (por ejemplo, para InfraPilot, buscar solo en la política y el catálogo).
3. Escribid una prueba de humo en `tests/test_busqueda.py` que compruebe que tres preguntas recuperan su documento correcto entre los 3 primeros (podéis marcarla para que solo se ejecute con el modelo real).

## Entrega

1. `evals/preguntas_recuperacion.jsonl` con 15 o más preguntas.
2. `docs/comparativa_busqueda.md` con la tabla, el análisis de fallos y la decisión (actualizad el ADR de la sesión 5 si cambia).
3. `rag/busqueda.py` y su prueba.
4. Commit: `Sesión 6: comparativa de búsqueda y base vectorial`.

## Criterios de evaluación (0 a 3 puntos cada uno)

| Criterio | 3 puntos |
| --- | --- |
| Preguntas | 15 o más, de los cuatro tipos, con fuente correcta |
| Comparativa | Cinco configuraciones medidas con hit@k, MRR y latencia |
| Análisis | Cada fallo diagnosticado y decisión justificada con datos |
| Implementación | Búsqueda persistente, con filtros y prueba |
