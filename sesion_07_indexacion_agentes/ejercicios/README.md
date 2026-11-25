# Sesión 7. Laboratorio guiado

Completa cada fichero sustituyendo los `raise NotImplementedError` por tu código. Comprueba tu trabajo con:

```bash
pytest sesion_07_indexacion_agentes -v
```

## Ejercicio 1. Pipeline de ingesta incremental (laboratorio de M4, 30 min)

Fichero: `s07_ej1_ingesta.py`

1. `huella(texto)`.
2. `clasificar_cambios(documentos, manifiesto)`: nuevos, modificados, eliminados y sin cambios.
3. `PipelineIngesta.borrar_documento(nombre)`: `delete` con filtro `where` por metadato.
4. `PipelineIngesta.indexar_documento(documento)`: trocea con `trocear_por_secciones` de `comun.documentos`, una llamada de embeddings y `upsert`.
5. `PipelineIngesta.procesar(carpeta)`: el orden importa. Primero borra los modificados y los eliminados, después indexa los nuevos y los modificados, y al final guarda el manifiesto.

Prueba el comportamiento incremental: ejecuta el fichero dos veces (la segunda no indexa nada). Después copia la carpeta de documentos a `salidas/docs_prueba/`, modifica un documento, borra otro y ejecuta `PipelineIngesta(...).procesar("salidas/docs_prueba")`.

## Ejercicio 2. Evaluar el RAG de extremo a extremo (laboratorio de M4, 30 min)

Fichero: `s07_ej2_evaluar_rag.py`

1. `se_abstiene(texto)`, `documentos_citados(texto, documentos)` y `cobertura(respuesta, esperado)`.
2. `evaluar_pregunta(pregunta, resultado)`: métricas distintas según la pregunta tenga fuente o no.
3. `agregar(por_pregunta)`: media de cada métrica solo sobre las preguntas en las que aparece.
4. `checklist(metricas, umbrales)`.

Ejecuta el fichero: evalúa el RAG de referencia con las 30 preguntas y muestra el checklist. Anota qué criterios no se cumplen y por qué.

## Ejercicio 3. Tu primer bucle de agente (laboratorio de M5, 66 min)

Fichero: `s07_ej3_bucle_agente.py`

1. `calcular(expresion)`: evaluador aritmético **seguro** con el módulo `ast`. Nunca uses `eval`: un modelo manipulado podría pedirte que evalúes `__import__('os').system(...)`. Los tests lo comprueban.
2. `esquema(nombre, descripcion, propiedades, requeridas)`: el formato de herramienta de la API de OpenAI.
3. `ejecutar_herramienta(nombre, argumentos_json, registro)`: nunca lanza excepciones; los errores vuelven como texto `ERROR: ...`.
4. `bucle(objetivo, registro, herramientas, sistema, max_pasos)`: el bucle de los apuntes (7.5).

Antes de programar el bucle, ejecuta `ejemplos/01_tool_calling_paso_a_paso.py` y lee los cuatro mensajes del intercambio.

Ejecuta el fichero con el modelo real: los dos objetivos combinan búsqueda en la documentación y cálculo. Lee los pasos que imprime. ¿Usa siempre `calcular` para las cuentas? ¿Qué pasa si quitas esa herramienta del registro?

## Práctica de equipo

El enunciado está en [`PRACTICA_07.md`](PRACTICA_07.md).
