# Sesión 4. Laboratorio guiado

Completa cada fichero sustituyendo los `raise NotImplementedError` por tu código. Comprueba tu trabajo con:

```bash
pytest sesion_04_alucinaciones_prompting -v
```

## Ejercicio 1. Banco de pruebas de alucinaciones (laboratorio de M2, 60 min)

Fichero: `s04_ej1_banco_alucinaciones.py`

El fichero `datos/atlantica/casos_alucinacion.jsonl` tiene 10 preguntas diseñadas para provocar alucinaciones. Cada una indica cómo se evalúa (`criterio`): el modelo debe abstenerse, dar un valor exacto, rechazar una premisa falsa o requiere revisión manual.

1. `cargar_casos(ruta)`: lee el JSONL.
2. `contiene_alguna(texto, marcas)`: sin distinguir mayúsculas ni tildes. La función `_normalizar` ya está hecha.
3. `numeros_en(texto)`: extrae los números en formato canónico. Es el paso más delicado: en español, `3.536,5049` y `3536,5049` son el mismo número que `3536.5049`, y `48.379` es cuarenta y ocho mil. Lee bien el docstring y los tests.
4. `evaluar(caso, respuesta)`: devuelve «correcta», «alucinacion» o «revisar» según el criterio.
5. `ejecutar(casos, sistema)` y `resumen(resultados)`.

Ejecuta el fichero. Compara la tasa de alucinación **sin instrucciones** y **con el sistema prudente**. Revisa a mano los casos «revisar» (A02 y A05): ¿son reales las referencias que da?

## Ejercicio 2. Plantilla de prompt estructurado (laboratorio de M3, 20 min)

Fichero: `s04_ej2_plantilla_prompt.py`

1. `sistema()`: construye el mensaje de sistema con las secciones no vacías, en el orden y con los títulos del docstring. Instrucciones numeradas; restricciones con viñetas.
2. `mensajes(entrada)`: sistema, pares de ejemplos y la entrada entre `<entrada>` y `</entrada>`.
3. `huella()`: los 8 primeros caracteres del SHA-256 del prompt. Anótala junto a cada resultado de evaluación para saber qué versión lo produjo.

## Ejercicio 3. Zero-shot, few-shot y cadena de pensamiento (laboratorio de M3, 25 min)

Fichero: `s04_ej3_tecnicas.py`

1. `normalizar_categoria(texto)`: la categoría que aparece **antes** en el texto.
2. `zero_shot(incidencia)` y `mensajes_few_shot(incidencia)` / `few_shot(incidencia)`.
3. `extraer_respuesta_final(texto)`: lo que va tras la **última** «Respuesta final:».
4. `con_razonamiento(pregunta)`.

Ejecuta el fichero y anota: ¿cambia la clasificación entre zero-shot y few-shot? ¿Acierta el cálculo del precio con razonamiento? ¿Y sin él?

## Ejercicio 4. Salida estructurada y reglas de negocio (laboratorio de M3, 21 min)

Fichero: `s04_ej4_salida_estructurada.py`

1. `clasificar(texto)`: una línea con `llm.estructurado`.
2. `problemas_de_negocio(c)`: las tres reglas del docstring. El esquema garantiza la forma; estas reglas, la coherencia.
3. `corregir(c)`: una copia corregida con `model_copy(update=...)`. El original no se modifica.

## Ejercicio 5. Evaluar y comparar versiones de un prompt (reto, 30 min)

Fichero: `s04_ej5_evaluar_prompts.py`

1. `cargar_golden(ruta)`.
2. `palabras_clave(texto)` y `puntuar(respuesta, esperado)`: una métrica sencilla de cobertura de palabras clave. No es perfecta (no entiende sinónimos ni negaciones), pero es rápida, gratuita y suficiente para comparar versiones. En la sesión 12 la complementarás con un LLM como juez.
3. `evaluar_version(nombre, responder, casos)` y `comparar(resultados)`.

Ejecuta el fichero: compara un prompt sin contexto con otro que incluye la política de infraestructura. Es tu primera evidencia de por qué hace falta RAG.

## Práctica de equipo

El enunciado está en [`PRACTICA_04.md`](PRACTICA_04.md).
