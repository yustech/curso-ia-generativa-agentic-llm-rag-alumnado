# Práctica 2. Matriz de riesgos del reto y comparativa de herramientas

Entregables del equipo: `docs/matriz_riesgos.md` y `docs/comparativa_herramientas.md`.

## Parte 1. Matriz de riesgos y controles (laboratorio de M1, 60 min)

Analizad el asistente de vuestro reto como si fuera a ponerse en producción en Atlántica.

1. Leed la política de uso de IA (`datos/atlantica/documentos/03_politica_uso_ia.md`) y la de seguridad (`02_politica_seguridad_informacion.md`).
2. Clasificad preliminarmente el caso de uso según el Reglamento Europeo de IA (prohibido, alto, limitado o mínimo) y justificadlo en dos líneas.
3. Identificad **al menos 8 riesgos** que cubran como mínimo cinco categorías distintas de la tabla del apartado 2.1.
4. Para cada riesgo: probabilidad, impacto y **al menos un control concreto**. «Tener cuidado» no es un control; «el agente solo tiene permisos de lectura en el backlog» sí lo es.
5. Generad la tabla con vuestro código del ejercicio 1 (`a_markdown`) y comprobad con `sin_control` que no queda ningún riesgo medio o alto sin control.

Riesgos que no deberían faltar según el reto:

| Reto | Pistas |
| --- | --- |
| R1 · DevAssist | Código propietario enviado a servicios externos; pruebas generadas que pasan pero no prueban nada; sugerencias que introducen vulnerabilidades |
| R2 · InfraPilot | Terraform que incumple la política (bucket público, región prohibida); aplicar cambios sin aprobación; costes descontrolados |
| R3 · PMO Copilot | Informes con datos inventados; datos personales de las actas; marcar historias como hechas sin revisión |

## Parte 2. Cuadro comparativo de herramientas y modelos (reto de M2, 80 min)

### 2.1 Herramientas (40 min)

Comparad cuatro formas de ejecutar el asistente de vuestro reto. Probad vosotros mismos Ollama y LM Studio; para Colibri y el servicio en la nube usad la información de los apuntes y la demostración del docente.

| Criterio | Ollama | LM Studio | Colibri | Servicio en la nube |
| --- | --- | --- | --- | --- |
| Privacidad de los datos de Atlántica | | | | |
| Facilidad de instalación y uso | | | | |
| Integración desde Python (API) | | | | |
| Velocidad medida (tokens/s) en vuestro portátil | | | No aplica | No aplica |
| Licencia y coste | | | | |
| Encaje con la política de Atlántica | | | | |
| ¿Lo recomendaríais para vuestro reto? ¿Para qué? | | | | |

### 2.2 Modelos (40 min)

Con vuestro código del ejercicio 3, comparad `granite4:micro`, `gemma3:4b` y `qwen3:4b` con **cinco preguntas propias de vuestro reto** (por ejemplo, para InfraPilot: «¿qué etiquetas obligatorias tiene un recurso en Atlántica?» y «escribe un bloque Terraform para un bucket privado»).

Para cada modelo anotad: tiempo medio, tokens por segundo, calidad de las respuestas (de 1 a 5, con un criterio que definís antes de mirar) y si admite herramientas. Cerrad con una recomendación justificada del modelo por defecto para vuestro asistente.

## Entrega

1. `docs/matriz_riesgos.md`: clasificación de riesgo del caso de uso y matriz con al menos 8 riesgos.
2. `docs/comparativa_herramientas.md`: los dos cuadros y la recomendación.
3. Commit: `Sesión 2: matriz de riesgos y comparativa de herramientas`.

## Criterios de evaluación (0 a 3 puntos cada uno)

| Criterio | 3 puntos |
| --- | --- |
| Cobertura de riesgos | 8 o más riesgos en 5 o más categorías, específicos del reto |
| Controles | Concretos, verificables y proporcionados al nivel de riesgo |
| Comparativa | Datos medidos por el equipo, no copiados |
| Recomendación | Justificada con los criterios y coherente con la política de Atlántica |
