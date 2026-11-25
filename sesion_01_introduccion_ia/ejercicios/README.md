# Sesión 1. Laboratorio guiado

Completa cada fichero sustituyendo los `raise NotImplementedError` por tu código. Comprueba tu trabajo con:

```bash
pytest sesion_01_introduccion_ia -v
```

Al empezar, todos los tests fallan. Es lo esperado: tu trabajo es ponerlos en verde.

## Ejercicio 0. Entorno (70 minutos, sin tests)

Es la primera práctica del día y la más importante: sin entorno no hay curso.

1. Instala Python 3.12, Visual Studio Code (con la extensión Python), Git, Ollama y LM Studio. Sigue el apartado 1.5 de los apuntes.
2. Descarga los dos modelos del curso:

```bash
ollama pull granite4:micro
ollama pull embeddinggemma
```

3. Clona el repositorio, crea el entorno virtual, actívalo e instala las dependencias.
4. Copia `.env.example` como `.env`.
5. Ejecuta `python comprobar_entorno.py` hasta que no haya ningún `ERROR`. Haz una captura del resultado.
6. Ejecuta los dos ejemplos de la sesión:

```bash
python sesion_01_introduccion_ia/ejemplos/01_hola_llm.py
python sesion_01_introduccion_ia/ejemplos/02_tres_paradigmas.py
```

7. Abre LM Studio, busca y descarga `granite-4.0-micro` (formato GGUF). Carga el modelo y pregúntale lo mismo que en el ejemplo 1. Anota en qué se diferencian la experiencia y la velocidad.
8. Comprueba que llegas al servidor compartido: cambia temporalmente `LLM_BASE_URL` en `.env` por la URL que te dé el docente y vuelve a ejecutar `comprobar_entorno.py`. Después deja la URL de Ollama local.

## Ejercicio 1. Clasificar casos de uso

Fichero: `s01_ej1_clasificacion.py`

El fichero `datos/atlantica/casos_uso.json` contiene 8 casos de uso de Atlántica. Vas a decidir qué paradigma de IA es el más adecuado para cada uno.

1. Completa `cargar_casos(ruta)`: lee el JSON y devuelve la lista.
2. Completa `clasificacion_manual()`. Devuelve un diccionario con los 8 casos (`C1` a `C8`). Para cada uno indica:
   - `paradigma`: uno de los valores de `PARADIGMAS`.
   - `tipo_modelo`: por ejemplo «regresión», «LLM con RAG» u «optimización de rutas».
   - `justificacion`: una frase de al menos 20 caracteres.

   Discútelo con tu equipo antes de escribirlo. Pista: repasa las preguntas del apartado 1.4.
3. Completa `validar_ficha(ficha, casos)`. Devuelve una lista de textos con los problemas encontrados:
   - `"<id>: falta la clasificación"` si falta un caso.
   - `"<id>: paradigma no válido (...)"` si el paradigma no está en `PARADIGMAS`.
   - `"<id>: falta el tipo de modelo"` si está vacío.
   - `"<id>: la justificación es demasiado corta"` si tiene menos de 20 caracteres.
4. Completa `resumen_por_paradigma(ficha)`: cuántos casos hay de cada paradigma, con todas las claves de `PARADIGMAS` en el mismo orden (las que no aparecen valen 0).
5. Completa `a_markdown(ficha, casos)`: una tabla Markdown con las columnas `Caso`, `Descripción`, `Paradigma`, `Tipo de modelo` y `Justificación`.

Ejecuta el fichero: la tabla que imprime es la base de tu ficha de clasificación del reto.

## Ejercicio 2. Pedir la clasificación a un LLM

Fichero: `s01_ej2_clasificar_con_llm.py`

Ahora le pides lo mismo al modelo y comparas. Es tu primer contacto con una **salida estructurada**: en lugar de texto libre, el modelo devuelve un JSON que valida un modelo Pydantic.

1. Completa `construir_prompt(caso)`. El texto debe incluir el caso, la lista de paradigmas posibles y la petición de responder en JSON con los campos `paradigma`, `tipo_modelo` y `justificacion`.
2. Completa `clasificar_con_llm(caso)` con una sola línea: usa `llm.estructurado(...)` con el prompt, el modelo `Clasificacion` y el mensaje de sistema `SISTEMA`.
3. Completa `comparar(manual, automatica)`: cuántos casos coinciden en paradigma, sobre cuántos casos comunes, el porcentaje con un decimal y la lista ordenada de discrepancias.
4. Ejecuta el fichero con el modelo real:

```bash
python sesion_01_introduccion_ia/ejercicios/s01_ej2_clasificar_con_llm.py
```

Responde en tu cuaderno: ¿en qué casos discrepa el modelo de tu equipo? ¿Quién tiene razón y por qué? ¿Te fiarías del modelo para hacer esta clasificación en un proyecto?

## Práctica de equipo

El enunciado está en [`PRACTICA_01.md`](PRACTICA_01.md).
