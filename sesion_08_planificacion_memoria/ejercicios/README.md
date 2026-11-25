# Sesión 8. Laboratorio guiado

Completa cada fichero sustituyendo los `raise NotImplementedError` por tu código. Comprueba tu trabajo con:

```bash
pytest sesion_08_planificacion_memoria -v
```

Desde hoy las piezas de agente de la sesión 7 (`calcular`, `esquema`, `ejecutar_herramienta`, `buscar_documentacion`) están en `comun/herramientas.py`.

## Ejercicio 1. Agente ReAct con trazas (laboratorio, 40 min)

Fichero: `s08_ej1_react.py`

1. `clave_llamada(nombre, argumentos)`: clave canónica para detectar repeticiones aunque cambie el orden de las claves del JSON.
2. `AgenteReAct.ejecutar(objetivo)`: el bucle de la sesión 7 con tres mejoras: **trazas** (`inicio`, `modelo`, `herramienta`, `fin`), **detección de bucles** y métricas (llamadas al modelo y segundos). Lee el docstring con calma: el orden de los registros importa y los tests lo comprueban.

Ejecuta el fichero con el modelo real y después lee la traza:

```bash
python sesion_08_planificacion_memoria/ejemplos/01_leer_traza.py trazas/s08_react.jsonl
```

**Comprueba el resultado a mano** con el catálogo (`07_catalogo_modulos_terraform.md`) y la política (`06_politica_infraestructura_cloud.md`). ¿Es correcto? Si no lo es, ¿en qué paso de la traza empieza el error?

## Ejercicio 2. Planificar y ejecutar (laboratorio, 30 min)

Fichero: `s08_ej2_plan_ejecutar.py`

1. `planificar(objetivo, descripcion_herramientas, max_pasos)`: una llamada a `llm.estructurado` con el modelo `Plan`.
2. `validar_plan(plan, herramientas, max_pasos)`: los cuatro problemas del docstring.
3. `ejecutar_plan(plan, registro, detener_en_error)`.
4. `sintetizar(objetivo, resultados)`.

Ejecuta el fichero e imprime el plan. ¿Son ejecutables todos los pasos? ¿Qué pasa con los pasos que dependen de resultados anteriores? ¿La respuesta final dice algo que no salga de los resultados?

## Ejercicio 3. Memoria y estado (Reto 1, 30 min)

Fichero: `s08_ej3_memoria.py`

1. `tokens_aproximados(mensajes)`.
2. `MemoriaVentana.agregar` y `contexto`: el contexto nunca empieza por un mensaje del asistente.
3. `MemoriaResumen.compactar` y `contexto`.
4. `EstadoPeticion.faltan`, `actualizar` y `como_texto`: el estado de trabajo de InfraPilot.

## Ejercicio 4. Guardarraíles (Reto 2, 30 min)

Fichero: `s08_ej4_guardarrailes.py`

1. `detectar_inyeccion(texto)`: los patrones están escritos sin tildes y en minúsculas; normaliza **solo el texto**.
2. `ocultar_datos_personales(texto)`: sustituye y cuenta.
3. `PoliticaHerramientas.autorizar(nombre, argumentos_json, confirmar)`: lista blanca y confirmación humana. `confirmar` es una función que recibes: en el ejemplo pregunta por consola; en la sesión 11 será un botón de la interfaz.
4. `Limites.comprobar(pasos, segundos, llamadas_herramienta)`.

Ejecuta `ejemplos/02_inyeccion_indirecta.py`. ¿El sistema ingenuo obedece la instrucción escondida? ¿Y el defensivo? ¿Te fiarías de la defensa por prompt?

## Práctica de equipo

El enunciado está en [`PRACTICA_08.md`](PRACTICA_08.md).
