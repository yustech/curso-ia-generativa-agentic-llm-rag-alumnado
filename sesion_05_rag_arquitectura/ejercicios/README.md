# Sesión 5. Laboratorio guiado

Completa cada fichero sustituyendo los `raise NotImplementedError` por tu código. Comprueba tu trabajo con:

```bash
pytest sesion_05_rag_arquitectura -v
```

Vas a construir un RAG completo **sin ningún framework**: cargador, troceado, índice vectorial, recuperación, prompt con citas y respuesta. Cuando en la sesión 10 uses LangChain o LlamaIndex sabrás exactamente qué hacen por dentro.

## Ejercicio 1. Cargar y trocear documentos (30 min)

Fichero: `s05_ej1_documentos.py`

1. `leer_front_matter(texto)`: separa la cabecera `---` del cuerpo. Ojo: el valor puede contener `:`.
2. `cargar_documentos(carpeta)`: todos los `.md` en orden alfabético.
3. `trocear_por_caracteres(texto, tamano, solape)`: ventana deslizante. Valida los parámetros.
4. `trocear_por_secciones(documento)`: un trozo por cada sección `##`, con el título del documento y de la sección al principio del texto.
5. `estadisticas(textos)`.

Ejecuta el fichero y compara los dos troceados: número de trozos, longitud media y, sobre todo, **lee un trozo de cada tipo**. ¿Cuál entenderías sin ver el documento?

## Ejercicio 2. Un RAG mínimo desde cero (40 min)

Fichero: `s05_ej2_rag_minimo.py`

1. `coseno(a, b)` con NumPy.
2. `IndiceMemoria.agregar(trozos)`: **una sola llamada** a `llm.embeddings` para todos los textos (los tests lo comprueban: llamar una vez por trozo es un error de rendimiento clásico).
3. `IndiceMemoria.buscar(consulta, k)`: los `k` más similares, ordenados.
4. `construir_mensajes(pregunta, resultados)`: el formato exacto del docstring. Fíjate en la última frase del mensaje de sistema: es la primera defensa frente a la inyección indirecta de instrucciones.
5. `fuentes_citadas(respuesta, resultados)`: qué fragmentos ha citado realmente el modelo.
6. `responder(pregunta, indice, k)`.

Ejecuta el fichero con el modelo real. Después prueba con 10 preguntas de `datos/atlantica/evaluacion/preguntas_rag.jsonl` y anota para cada una: ¿el trozo correcto está entre los recuperados?, ¿la respuesta es correcta?, ¿cita bien? Separa los fallos de **recuperación** de los de **generación**.

## Práctica de equipo

El enunciado está en [`PRACTICA_05.md`](PRACTICA_05.md).
