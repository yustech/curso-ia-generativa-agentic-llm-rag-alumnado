# Práctica 13. Canvas, propuesta técnica y plan de validación del proyecto final

Entregables del equipo: `docs/canvas_caso_uso.md`, `docs/propuesta_tecnica.md` y `docs/plan_validacion.md`.

## Parte 1. Laboratorio integrador con el asistente del equipo (durante los laboratorios de M6)

Aplicad los ejercicios a **vuestro asistente completo**:

1. **Evaluación de extremo a extremo** con vuestro conjunto dorado, ampliado a **30 casos o más**. Guardad la línea base.
2. **Red teaming** con los ataques del ejercicio 2 adaptados a vuestro reto y al menos 4 propios (por ejemplo, para PMO Copilot, un acta con una instrucción escondida; para InfraPilot, una petición que intenta colar un bucket público con otro nombre).
3. **Prueba de carga** de vuestro asistente contra el servidor compartido con 1, 4 y 8 usuarios.
4. **Caso de negocio** con el ejercicio 4.

## Parte 2. Taller: definición del proyecto final (66 min)

### 1. Canvas del caso de uso (20 min)

Rellenad `docs/canvas_caso_uso.md` con la plantilla `plantillas/canvas_caso_uso.md`: problema, usuarios, propuesta de valor, datos y fuentes, solución, métricas de éxito, riesgos y controles, costes y beneficio, y clasificación según el Reglamento Europeo de IA.

### 2. Propuesta técnica (26 min)

Rellenad `docs/propuesta_tecnica.md` con la plantilla `plantillas/propuesta_tecnica.md`: arquitectura (diagrama Mermaid actualizado), modelo y motor de inferencia, RAG (fuentes, troceado, búsqueda), herramientas con sus permisos, guardarraíles, framework elegido (enlace al ADR), requisitos de hardware y despliegue.

### 3. Plan de validación (20 min)

Rellenad `docs/plan_validacion.md` con la plantilla `plantillas/plan_validacion.md`: conjunto dorado, métricas y umbrales de aceptación, resultados de hoy (evaluación, red teaming, carga), regresiones vigiladas y política de revisión humana.

### Cierre: ensayo relámpago (24 min)

Cada equipo hace un ensayo de **5 minutos** del arranque de su demo (problema, solución y una pregunta en directo) y recibe comentarios.

## Entrega

1. `docs/canvas_caso_uso.md`, `docs/propuesta_tecnica.md` y `docs/plan_validacion.md`.
2. `evals/golden_set.jsonl` con 30 casos o más y `salidas/linea_base.json`.
3. Commit: `Sesión 13: definición del proyecto final y plan de validación`.

## Criterios de evaluación (0 a 3 puntos cada uno)

| Criterio | 3 puntos |
| --- | --- |
| Canvas | Problema, valor y riesgos concretos, con números del caso de negocio |
| Propuesta técnica | Arquitectura completa y coherente con las decisiones registradas |
| Plan de validación | 30 o más casos, umbrales, resultados reales de evaluación, seguridad y carga |
| Ensayo | Mensaje claro y demo en directo funcionando |
