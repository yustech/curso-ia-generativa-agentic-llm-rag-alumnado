# Sesión 9. Laboratorio guiado

Completa cada fichero sustituyendo los `raise NotImplementedError` por tu código. Comprueba tu trabajo con:

```bash
pytest sesion_09_herramientas_apis -v
```

Todas las pruebas de hoy son deterministas: ni el modelo ni la API real son necesarios para ponerlas en verde.

## Preparación: la API simulada del backlog

Abre una segunda terminal (con el entorno virtual activado) y arranca la API:

```bash
python -m comun.api_backlog --reiniciar
```

Prueba en el navegador `http://127.0.0.1:8765/historias?sprint=23`. Para el ejercicio 2 la arrancarás con fallos simulados: `python -m comun.api_backlog --fallos 0.3`.

## Ejercicio 1. Herramientas con contrato validado (laboratorio, 70 min)

Fichero: `s09_ej1_herramientas.py`

1. `ResultadoHerramienta.como_texto()`.
2. `describir_errores(error)`: convierte un `ValidationError` en una línea que el modelo entienda.
3. `Registro.herramienta(argumentos, descripcion, con_efectos)`: un **decorador con parámetros** (una función que devuelve el decorador). Si nunca has escrito uno, mira el test `registro()` para ver cómo se usa.
4. `Registro.esquemas()`: el esquema sale de `model_json_schema()`.
5. `Registro.ejecutar(nombre, argumentos_json)`: valida y ejecuta sin lanzar nunca excepciones.

Ejecuta antes `ejemplos/01_esquema_desde_pydantic.py` para ver qué recibe el modelo y qué detecta la validación.

## Ejercicio 2. Cliente de API robusto (Reto 1, 35 min)

Fichero: `s09_ej2_cliente_api.py`

1. `espera_exponencial(intento, base, maximo)`.
2. `ClienteBacklog._peticion(...)`: la pieza central. Reintenta los errores transitorios y los de transporte; no reintenta los definitivos. Recibe `dormir` como parámetro para que los tests no esperen de verdad.
3. `listar`, `obtener` y `actualizar_estado`.

Arranca la API con `--fallos 0.3` y ejecuta el fichero varias veces. Observa en la terminal de la API las respuestas 503 y cómo el cliente las absorbe.

## Ejercicio 3. Agente con dos herramientas y modo degradado (Reto 1, 35 min)

Fichero: `s09_ej3_agente_backlog.py`

1. `crear_registro(cliente)`: dos herramientas de solo lectura con sus modelos de argumentos (ya definidos).
2. `api_disponible(cliente)`.
3. `responder(pregunta, cliente)`: si la API no está disponible, responde con el mensaje degradado **sin llamar al modelo**; si lo está, usa `comun.agente.AgenteReAct`.

Ejecuta el fichero con la API arrancada con fallos. Después para la API (Ctrl+C) y vuelve a ejecutarlo: ¿qué responde ahora?

## Práctica de equipo

El enunciado está en [`PRACTICA_09.md`](PRACTICA_09.md).
