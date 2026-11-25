# Práctica 10. Workflow multiagente y matriz de decisión tecnológica (Hito 3)

Entregables del equipo: `agente/flujo.py`, `mcp/servidor.py`, `docs/matriz_decision.md` y `docs/comparativa_frameworks.md`.

## Reto 1. Flujo multiagente con roles especializados (70 min)

Diseñad e implementad con LangGraph un flujo con **al menos tres roles** para vuestro reto. Propuestas:

| Reto | Roles | Herramientas por rol |
| --- | --- | --- |
| R1 · DevAssist | Analista (lee código y guía) → generador de pruebas → verificador (ejecuta las pruebas y devuelve los fallos al generador) | `leer_fichero`, `comprobar_estilo` / ninguna / `ejecutar_pruebas` |
| R2 · InfraPilot | Recopilador (completa la petición y pregunta lo que falta) → diseñador (propone recursos) → auditor de política (valida y devuelve incumplimientos) → preparador del cambio (con aprobación humana) | ninguna / `consultar_catalogo` / `validar_peticion`, `estimar_coste` / `registrar_solicitud_cambio` |
| R3 · PMO Copilot | Extractor (acciones y riesgos del acta) → redactor de historias → revisor de la definición de preparado | `leer_acta` / ninguna / `problemas_preparacion` |

Requisitos:

1. Estado tipado con los campos que comparten los roles.
2. Al menos una arista condicional con máximo de iteraciones.
3. Cada rol solo tiene las herramientas que necesita.
4. Las acciones con efectos pasan por confirmación humana.
5. Probad el flujo con 3 casos del conjunto dorado y guardad las trazas o la salida.

Además, exponed las herramientas de vuestro reto en un **servidor MCP** (`mcp/servidor.py`) siguiendo el ejercicio 1, con las restricciones de seguridad de las herramientas.

## Reto 2. Comparativa y matriz de decisión tecnológica (56 min)

### 1. Comparativa (36 min)

Implementad **la misma tarea acotada** de vuestro reto de dos formas: con vuestro agente sin framework (sesiones 8 y 9) y con el flujo de LangGraph (o con LlamaIndex si vuestra tarea es sobre todo de recuperación). Comparad con 5 casos:

| Criterio | Sin framework | LangGraph / LlamaIndex |
| --- | --- | --- |
| Casos correctos (de 5) | | |
| Latencia media | | |
| Llamadas al modelo por caso | | |
| Líneas de código | | |
| Facilidad para depurar un fallo (1-5) | | |

### 2. Matriz de decisión (20 min)

Con el ejercicio 4, construid la matriz ponderada para vuestro asistente de cara al proyecto final: opciones (sin framework, LangGraph, LlamaIndex y, si queréis, una combinación), criterios con pesos justificados por las necesidades del cliente y decisión final. Registrad la decisión también como ADR.

## Entrega del Hito 3

1. `agente/flujo.py` y su ejecución con 3 casos.
2. `mcp/servidor.py`.
3. `docs/comparativa_frameworks.md` y `docs/matriz_decision.md`.
4. `docs/adr/ADR-00N.md` con la decisión tecnológica.
5. Commit: `Sesión 10: flujo multiagente, servidor MCP y matriz de decisión`.

Comprobad el checklist del Hito 3: especificación del agente, trazas y registro de errores, herramientas con contrato y pruebas, flujo multiagente y selección de framework.

## Criterios de evaluación (0 a 3 puntos cada uno)

| Criterio | 3 puntos |
| --- | --- |
| Flujo multiagente | Tres roles con permisos separados, arista condicional con máximo y confirmación humana |
| Servidor MCP | Herramientas del reto expuestas con validación y restricciones |
| Comparativa | Las dos implementaciones medidas con los mismos casos |
| Decisión | Pesos justificados por el cliente, coherente con la comparativa, registrada como ADR |
