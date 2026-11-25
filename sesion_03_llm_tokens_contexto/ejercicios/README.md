# Sesión 3. Laboratorio guiado

Completa cada fichero sustituyendo los `raise NotImplementedError` por tu código. Comprueba tu trabajo con:

```bash
pytest sesion_03_llm_tokens_contexto -v
```

Cada ejercicio alimenta un experimento del cuaderno de tu equipo (`PRACTICA_03.md`). Anota los resultados a medida que los obtengas.

> `tiktoken` descarga un fichero pequeño con la codificación la primera vez que se usa. Si no tienes conexión, pide al docente la copia de la caché.

## Ejercicio 1. Tokens y coste (laboratorio, 35 min)

Fichero: `s03_ej1_tokens.py`

1. `contar_tokens(texto, codificacion)` y `trozos(texto, codificacion)`: usa `tiktoken.get_encoding(...)`, `encode` y `decode`. La concatenación de los trozos debe reconstruir el texto original.
2. `tokens_por_palabra(texto)`: tokens / palabras, con 2 decimales (0.0 si no hay palabras).
3. `estimar_coste(...)`: coste con precios por millón de tokens, 4 decimales.
4. `coste_mensual(...)`: peticiones al día × días × coste por petición, 2 decimales.
5. `comparar_textos(textos)`: una fila por texto con nombre, palabras, tokens y tokens por palabra.

Experimento para el cuaderno: compara un párrafo de un documento de Atlántica con su traducción al inglés, un bloque de código y una tabla con números. Ejecuta también `ejemplos/02_tokens_del_modelo.py`: ¿coinciden los tokens de tiktoken con los de cada modelo?

## Ejercicio 2. ¿Cabe este modelo en mi portátil? (laboratorio, 35 min)

Fichero: `s03_ej2_memoria.py`

1. `memoria_pesos_gb(miles_de_millones, bits)`.
2. `memoria_kv_gb(capas, cabezas_kv, dim_cabeza, contexto, bytes_por_valor)`.
3. `memoria_total_gb(...)`: pesos según el formato (`BITS_FORMATO`) más caché KV, más el margen. `ValueError` si el formato no existe.
4. `cabe(memoria, ram_gb, reservada_gb)`: compara con la RAM libre (16 GB menos 7 GB reservados por defecto).
5. `contexto_maximo(...)`: el mayor contexto en múltiplos de 1.024 que cabe.

Experimento para el cuaderno: calcula la memoria de `granite4:micro` (3B), `qwen3:4b` y un modelo de 8B en Q4_K_M con 4K, 8K y 32K de contexto. Después ejecuta `ejemplos/04_memoria_del_modelo.py` y compara tu cálculo con lo que mide Ollama.

## Ejercicio 3. La aguja en el pajar (Reto 1, 70 min)

Fichero: `s03_ej3_aguja.py`

1. `construir_pajar(n_frases, aguja, posicion)`: frases de relleno en orden (repitiendo la lista) y la aguja insertada antes de la frase de índice `round(posicion * n_frases)`. `ValueError` si la posición no está entre 0 y 1.
2. `encontrada(respuesta, valor)`: el valor aparece en la respuesta ignorando espacios y puntos.
3. `tabla(resultados)`: tabla Markdown con «sí» o «no».

La función `prueba(...)` ya está hecha: llama a la API nativa de Ollama fijando `num_ctx`. Ejecuta el fichero (tarda unos minutos). Responde en el cuaderno:

- ¿Qué pasa cuando el texto supera `num_ctx`? ¿Qué parte del texto se pierde?
- ¿Influye la posición de la aguja?
- ¿Cuánto tarda con 400 frases y `num_ctx` 8192 frente a 2048?

## Ejercicio 4. Muestreo y benchmark (Reto 2, 56 min)

Fichero: `s03_ej4_muestreo_benchmark.py`

1. `generar_varias(prompt, temperatura, n)`.
2. `diversidad(respuestas)`: proporción de respuestas distintas, sin distinguir mayúsculas ni espacios de los extremos.
3. `experimento_temperatura(prompt, temperaturas, n)`.
4. `resumen(muestras)`: media, mínimo y máximo con 1 decimal.

`benchmark(...)` ya está hecha. Para medir el servidor compartido añade a tu `.env`:

```
SERVIDOR_CURSO_URL=<URL que te dé el docente>
SERVIDOR_CURSO_CLAVE=<clave de tu equipo>
SERVIDOR_CURSO_MODELO=<modelo grande del servidor>
```

## Práctica de equipo

El enunciado está en [`PRACTICA_03.md`](PRACTICA_03.md).
