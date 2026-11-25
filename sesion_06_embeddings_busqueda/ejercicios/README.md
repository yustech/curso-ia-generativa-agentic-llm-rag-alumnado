# Sesión 6. Laboratorio guiado

Completa cada fichero sustituyendo los `raise NotImplementedError` por tu código. Comprueba tu trabajo con:

```bash
pytest sesion_06_embeddings_busqueda -v
```

A partir de hoy los laboratorios cargan los documentos con la versión de referencia de `comun/documentos.py` (equivalente a tu ejercicio de la sesión 5), para que nadie dependa de haberlo terminado.

## Ejercicio 1. Medidas de similitud (laboratorio, 20 min)

Fichero: `s06_ej1_similitud.py`

1. `normalizar(v)` (cuidado con la norma 0).
2. `coseno(a, b)` y `distancia_euclidea(a, b)`.
3. `matriz_similitud(vectores)`: **sin bucles**, con una multiplicación de matrices.
4. `mas_similares(consulta, vectores, k)`.

Ejecuta `ejemplos/01_similitudes.py` y responde: ¿qué pareja de frases sin palabras en común tiene mayor similitud? ¿Y la frase en inglés?

## Ejercicio 2. BM25, semántica e híbrida (laboratorio, 50 min)

Fichero: `s06_ej2_busqueda.py`

1. `tokenizar(texto)`: la normalización tiene que ser idéntica para documentos y consultas. Conserva la ñ (`años` no es `anos`) y los términos técnicos con punto o guion (`t3.medium`, `FARO-142`).
2. `BuscadorBM25`: construye `BM25Okapi` y busca con `get_scores`.
3. `BuscadorSemantico`: una llamada a `llm.embeddings` para todos los trozos; normaliza.
4. `fusion_rrf(rankings, k)`: la fórmula de los apuntes. Los tests comprueban las puntuaciones exactas.
5. `BuscadorHibrido.buscar`.

Ejecuta el fichero con tres consultas y observa qué buscador acierta en cada caso.

## Ejercicio 3. Métricas y tabla comparativa (Reto 1, 30 min)

Fichero: `s06_ej3_metricas.py`

1. `acierto_en_k` y `rango_reciproco`.
2. `cargar_preguntas`: solo las preguntas con fuente.
3. `evaluar(buscar, preguntas, k)`: hit@k, MRR y lista de fallos.
4. `tabla(resultados, k)`.

Ejecuta el fichero: produce la tabla comparativa de las tres estrategias con k = 1 y k = 3 sobre las 28 preguntas con fuente. **Antes de ejecutarlo, apuesta en el chat qué estrategia ganará.**

## Ejercicio 4. Base vectorial persistente con Chroma (Reto 2, 25 min)

Fichero: `s06_ej4_chroma.py`

1. `crear_coleccion(ruta, nombre)`: distancia coseno y `embedding_function=None`.
2. `indexar(coleccion, trozos, lote)`: `upsert` por lotes, con metadatos.
3. `consultar(coleccion, pregunta, k, documento)`: con filtro opcional por documento y similitud = 1 − distancia.

Ejecuta el fichero dos veces: la segunda no recalcula nada en Chroma porque `upsert` reemplaza los mismos ids. Mira la carpeta `indices/chroma`: es tu base vectorial.

## Práctica de equipo

El enunciado está en [`PRACTICA_06.md`](PRACTICA_06.md).
