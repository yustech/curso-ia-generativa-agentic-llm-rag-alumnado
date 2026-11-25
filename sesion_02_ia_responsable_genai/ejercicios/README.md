# Sesión 2. Laboratorio guiado

Completa cada fichero sustituyendo los `raise NotImplementedError` por tu código. Comprueba tu trabajo con:

```bash
pytest sesion_02_ia_responsable_genai -v
```

Los tests usan un modelo falso y determinista, así que no dependen de Ollama. Después ejecuta cada fichero con el modelo real para ver el resultado.

## Ejercicio 1. Matriz de riesgos (dentro del laboratorio de M1, 30 min)

Fichero: `s02_ej1_matriz_riesgos.py`

El modelo Pydantic `Riesgo` ya está definido: valida que la probabilidad y el impacto estén entre 1 y 5 y que la categoría sea una de las permitidas.

1. `exposicion(riesgo)`: probabilidad × impacto.
2. `nivel(valor)`: `"bajo"` hasta 6, `"medio"` de 7 a 14 y `"alto"` desde 15. Es el criterio de la metodología de Atlántica (`09_metodologia_proyectos.md`): desde 15 se escala a dirección.
3. `ordenar(riesgos)`: de mayor a menor exposición; a igual exposición, por `id` ascendente.
4. `sin_control(riesgos)`: ids de los riesgos medios o altos sin ningún control. Es el aviso más útil de una matriz.
5. `a_markdown(riesgos)`: tabla con las columnas `Id`, `Riesgo`, `Categoría`, `P`, `I`, `Exposición`, `Nivel` y `Controles`, ordenada por exposición. Los controles se separan con `; ` y, si no hay, se escribe `(ninguno)`.

Ejecuta el fichero para ver la matriz del ejemplo (chatbot de seguimiento de envíos). Úsala como modelo para la de tu reto.

## Ejercicio 2. Primeras llamadas y conversación con memoria (35 min)

Fichero: `s02_ej2_primeras_llamadas.py`

1. `preguntar(pregunta, sistema, temperatura)`: una llamada suelta con `llm.chat(...)`.
2. `Conversacion.enviar(texto)`: añade el mensaje del usuario al historial, llama al modelo con **todo** el historial, añade la respuesta como mensaje `assistant` y la devuelve.
3. `Conversacion.turnos`: cuántos mensajes de usuario hay.
4. `medir(funcion, *args, **kwargs)`: ejecuta la función y devuelve `(resultado, segundos)`.

Ejecuta el fichero y comprueba que en el segundo turno el modelo sabe en qué proyecto trabaja Iván.

## Ejercicio 3. Comparar modelos (30 min)

Fichero: `s02_ej3_comparar_modelos.py`

1. `ejecutar_en_modelo(pregunta, modelo)`: llama con temperatura 0 y devuelve modelo, respuesta, segundos, tokens de salida y tokens por segundo (1 decimal). Las métricas están en `llm.ultima_llamada`.
2. `comparar_modelos(pregunta, modelos)`: ejecuta en todos; si uno falla, la respuesta empieza por `ERROR:` y los números valen 0, pero **la comparación continúa**.
3. `tabla_markdown(resultados, ancho)`: tabla con `Modelo`, `Segundos` (1 decimal), `Tokens`, `Tokens/s` y `Respuesta` recortada a `ancho` caracteres, sin saltos de línea y con `…` si se recorta.

Descarga los modelos que vas a comparar (unos 6 GB en total; hazlo al empezar el laboratorio):

```bash
ollama pull gemma3:4b
ollama pull qwen3:4b
```

Ejecuta el fichero. La primera llamada a cada modelo tarda más porque lo carga en memoria: repite la ejecución y compara.

## Práctica de equipo

El enunciado está en [`PRACTICA_02.md`](PRACTICA_02.md).
