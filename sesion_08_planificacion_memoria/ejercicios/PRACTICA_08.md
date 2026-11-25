# Práctica 8. Especificación y prototipo del agente del equipo

Entregables del equipo: `docs/especificacion_agente.md`, el código en `agente/`, `docs/registro_errores.md` y las trazas en `trazas/`.

## Reto 1. Prototipo del agente para una tarea acotada (70 min)

### 1. Especificación (25 min)

Rellenad `docs/especificacion_agente.md` a partir de `plantillas/especificacion_agente.md`. Elegid **una sola tarea acotada** de vuestro reto:

| Reto | Tarea acotada para hoy |
| --- | --- |
| R1 · DevAssist | «Revisa esta función contra la guía de estilo y propón sus pruebas» |
| R2 · InfraPilot | «Recoge los datos de una petición de entorno, valídalos contra la política y estima el coste» |
| R3 · PMO Copilot | «Extrae las acciones y los riesgos de un acta y calcula la exposición de cada riesgo» |

La especificación debe incluir: objetivo, entradas y salidas, herramientas (con su nivel de permiso), estado de trabajo, patrón (ReAct o planificar-ejecutar) y por qué, límites, puntos de confirmación humana y criterios de éxito.

### 2. Prototipo (45 min)

Implementad el agente en `agente/` reutilizando `AgenteReAct` (ejercicio 1) o el patrón planificar-ejecutar (ejercicio 2), con:

- la herramienta `buscar_documentacion` sobre vuestro índice de la sesión 7;
- al menos una herramienta propia del reto (las tenéis preparadas en `equipos/<vuestro_reto>/herramientas.py`);
- trazas activadas.

## Reto 2. Guardarraíles y registro de errores (56 min)

### 1. Guardarraíles (25 min)

Añadid al agente, como mínimo:

- detección de inyección y ocultación de datos personales en la entrada (ejercicio 4);
- política de herramientas con lista blanca y confirmación humana para cualquier acción con efectos;
- límites de pasos y de tiempo;
- **una verificación de salida específica del reto**. Ejemplos: para InfraPilot, que cada importe de la respuesta aparezca en algún resultado de herramienta; para DevAssist, que el código propuesto sea Python válido (`ast.parse`); para PMO Copilot, que cada responsable de una acción aparezca en el acta.

### 2. Registro de errores (31 min)

Ejecutad el agente con **10 casos** de vuestro conjunto dorado (incluidos uno ambiguo y uno de seguridad) y registrad en `docs/registro_errores.md` cada fallo:

| Caso | Qué pasó | Tipo de error (taxonomía 8.6) | Paso de la traza donde empieza | Corrección propuesta |
| --- | --- | --- | --- | --- |

## Entrega

1. `docs/especificacion_agente.md`.
2. `agente/` con el prototipo y sus guardarraíles.
3. `trazas/` con las 10 ejecuciones (o una muestra si ocupan mucho).
4. `docs/registro_errores.md`.
5. Commit: `Sesión 8: especificación, prototipo y registro de errores del agente`.

## Criterios de evaluación (0 a 3 puntos cada uno)

| Criterio | 3 puntos |
| --- | --- |
| Especificación | Completa, acotada y con los permisos y puntos humanos justificados |
| Prototipo | Funciona en la tarea acotada con trazas |
| Guardarraíles | En capas, en el código, con una verificación de salida específica |
| Registro de errores | 10 casos, errores clasificados y localizados en la traza |
