# Sesión 13. Laboratorio guiado

Completa cada fichero sustituyendo los `raise NotImplementedError` por tu código. Comprueba tu trabajo con:

```bash
pytest sesion_13_casos_produccion -v
```

## Ejercicio 1. Evaluación de extremo a extremo (laboratorio integrador, 40 min)

Fichero: `s13_ej1_evaluacion_e2e.py`

1. `percentil(valores, p)`: con interpolación lineal; el test lo compara con `numpy.percentile`.
2. `juzgar(entrada, esperado, respuesta)`: juez con salida `Veredicto` (0, 1 o 2).
3. `evaluar(asistente, casos)`: ejecuta, mide y juzga. Si el asistente falla, puntuación 0 sin llamar al juez.
4. `metricas(filas)` y `regresiones(actual, base, tolerancia, factor_latencia)`.

Ejecuta el fichero: evalúa un agente de ejemplo con el conjunto dorado de InfraPilot y guarda la línea base en `salidas/linea_base.json`. Ejecútalo otra vez: compara con la línea base.

## Ejercicio 2. Red teaming (laboratorio integrador, 30 min)

Fichero: `s13_ej2_red_teaming.py`

1. `rechaza(respuesta)`.
2. `superado(ataque, respuesta)`: tres tipos de detector.
3. `ejecutar(asistente, ataques)` e `informe(filas)`.

Ejecuta el fichero: ataca a un asistente con un prompt de sistema defensivo. ¿Qué categorías resiste? Añade dos ataques propios a la lista.

## Ejercicio 3. Prueba de carga (laboratorio de producción, 40 min)

Fichero: `s13_ej3_carga.py`

1. `una_peticion(cliente, modelo, prompt, max_tokens)`: asíncrona con `AsyncOpenAI`.
2. `prueba_carga(cliente, modelo, usuarios, peticiones_por_usuario, prompt)`: tareas concurrentes con `asyncio.gather`.
3. `resumen(resultados, duracion)`.

Ejecuta primero contra Ollama en tu portátil y después contra el servidor (Ollama y vLLM) con la URL que te dé el docente:

```bash
python sesion_13_casos_produccion/ejercicios/s13_ej3_carga.py --usuarios 1 2 4
python sesion_13_casos_produccion/ejercicios/s13_ej3_carga.py --url <URL vLLM>/v1 --clave <clave> --modelo <modelo> --usuarios 1 4 8 16
```

## Ejercicio 4. Viabilidad del caso de negocio (laboratorio de producción, 20 min)

Fichero: `s13_ej4_viabilidad.py`

1. `beneficio_mensual`, `meses_recuperacion`, `roi_primer_anio` y `recomendacion`.

Calcula el caso de negocio de tu reto con los tiempos de tu mapa AS-IS/TO-BE de la sesión 11.

## Práctica de equipo

El enunciado está en [`PRACTICA_13.md`](PRACTICA_13.md).
