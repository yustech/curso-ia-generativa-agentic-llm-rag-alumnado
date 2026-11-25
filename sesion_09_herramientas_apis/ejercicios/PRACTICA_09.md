# Práctica 9. Agente del equipo con dos herramientas, contrato y pruebas

Entregables del equipo: `agente/` actualizado, `docs/contrato_herramientas.md` y `tests/` con las pruebas.

## Reto 1. Agente del equipo con dos herramientas (70 min, tras los ejercicios 2 y 3)

Integrad en vuestro agente **al menos dos herramientas del reto** usando el `Registro` del ejercicio 1, con modelos de argumentos Pydantic. Herramientas disponibles en `equipos/<reto>/herramientas.py`:

| Reto | Herramientas recomendadas | ¿Con efectos? |
| --- | --- | --- |
| R1 · DevAssist | `leer_fichero`, `comprobar_estilo`, `ejecutar_pruebas`, `calcular_tarifa` | No |
| R2 · InfraPilot | `validar_peticion`, `estimar_coste`, `generar_terraform`; `registrar_solicitud_cambio` | La última sí |
| R3 · PMO Copilot | `Backlog.listar`, `metricas_sprint`, `historias_no_preparadas`, `leer_acta`; `actualizar_estado`, `crear_historia` | Las dos últimas sí |

Requisitos:

1. Cada herramienta tiene un modelo de argumentos con descripciones, tipos cerrados (`Literal`) donde se pueda y restricciones (`ge`, `pattern`…).
2. Las herramientas con efectos se registran con `con_efectos=True` y pasan por la `PoliticaHerramientas` de la sesión 8 (confirmación humana).
3. Las herramientas que dependen de un servicio que puede fallar tienen timeout, reintentos y modo degradado.
4. Probad el agente con 5 casos del conjunto dorado y guardad las trazas.

## Reto 2. Contrato de herramientas y pruebas (56 min)

### 1. Contrato (20 min)

Rellenad `docs/contrato_herramientas.md` a partir de `plantillas/contrato_herramientas.md`, una ficha por herramienta: nombre, descripción tal como la ve el modelo, argumentos con tipo y restricciones, salida, efectos y nivel de permiso, errores posibles con el mensaje que recibe el modelo, idempotencia, timeout y reintentos.

### 2. Pruebas (36 min)

Escribid en `tests/` al menos **10 pruebas deterministas**:

- 4 de las herramientas (casos normales y frontera).
- 3 de validación de argumentos (casos que deben rechazarse).
- 2 del bucle del agente con `comun.llm.usar_llm_falso`: una con la secuencia correcta de herramientas y otra con un error de herramienta del que el agente se recupera.
- 1 de la política de confirmación: una acción con efectos rechazada por la persona no se ejecuta.

Opcional: 2 pruebas con el modelo real marcadas con `@pytest.mark.llm_real`.

## Entrega

1. `agente/` con las dos herramientas integradas y sus guardarraíles.
2. `docs/contrato_herramientas.md`.
3. `tests/` con 10 o más pruebas en verde (`pytest tests -v`).
4. Commit: `Sesión 9: herramientas con contrato y pruebas`.

## Criterios de evaluación (0 a 3 puntos cada uno)

| Criterio | 3 puntos |
| --- | --- |
| Integración | Dos o más herramientas validadas, con permisos y recuperación ante fallos |
| Contrato | Completo, con errores, efectos e idempotencia |
| Pruebas | 10 o más deterministas que cubren herramientas, validación, bucle y política |
| Robustez | El agente se recupera de un error de herramienta y degrada sin inventar |
