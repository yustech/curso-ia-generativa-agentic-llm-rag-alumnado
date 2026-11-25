# Práctica 12. Pipeline documental del reto e informe de validación y trazabilidad

Entregables del equipo: `documental/` y `docs/informe_validacion.md`.

## Reto 1. Pipeline documental del reto (70 min)

Construid en `documental/` un pipeline que **genere el documento principal de vuestro reto** con el reparto de trabajo del apartado 12.4 (estructura y cifras por código, redacción por el LLM):

| Reto | Entrada | Documento generado |
| --- | --- | --- |
| R1 · DevAssist | Un fichero de código | Informe de revisión: incumplimientos de la guía (de `comprobar_estilo`), pruebas propuestas con su resultado (de `ejecutar_pruebas`) y propuesta de refactorización explicada |
| R2 · InfraPilot | Una petición de entorno | Solicitud de cambio para el CAB: resumen, recursos, Terraform (de `generar_terraform`), coste (de `estimar_coste`), cumplimiento (de `validar_peticion`), plan de marcha atrás y ventana propuesta |
| R3 · PMO Copilot | Las actas de la semana y el backlog | Informe de estado semanal con historias propuestas a partir de las acciones (validadas con `problemas_preparacion`) |

Requisitos:

1. Una plantilla con la estructura exigida por la normativa de Atlántica (`08_procedimiento_gestion_cambios.md`, `09_metodologia_proyectos.md` o `04_guia_estilo_python.md`).
2. Cada dato generado lleva su fuente (fichero, sección, herramienta).
3. Si hay extracción, campos opcionales y normalización por código.
4. El documento se guarda en `salidas/` con la huella del prompt y el modelo usados.

## Reto 2. Informe de validación y trazabilidad (56 min)

1. Escribid al menos **4 comprobaciones deterministas** específicas de vuestro documento (ejercicio 3).
2. Definid la **rúbrica** del juez para vuestro documento y ejecutadlo.
3. Generad **5 documentos** (5 entradas distintas) y validad todos.
4. **Calibrad el juez**: revisad vosotros los 5 documentos con la misma rúbrica y comparad vuestras notas con las del juez. ¿Coincidís? ¿En qué se equivoca?
5. Escribid `docs/informe_validacion.md` con: las comprobaciones y su resultado en los 5 documentos, la comparación juez frente a personas, los errores encontrados y qué capa los detectó, y la política de revisión humana que proponéis (qué se revisa siempre y qué porcentaje en muestra).

## Entrega

1. `documental/` con el pipeline y sus pruebas.
2. `salidas/` con los 5 documentos generados (o una muestra).
3. `docs/informe_validacion.md`.
4. Commit: `Sesión 12: pipeline documental y validación`.

## Criterios de evaluación (0 a 3 puntos cada uno)

| Criterio | 3 puntos |
| --- | --- |
| Pipeline | Estructura y cifras por código, redacción por el LLM, documento conforme a la normativa |
| Trazabilidad | Cada dato con su fuente y comprobación automática de que aparece en ella |
| Validación | Cuatro o más comprobaciones, juez con rúbrica concreta y 5 documentos validados |
| Calibración y política | Juez comparado con personas y política de revisión justificada |
