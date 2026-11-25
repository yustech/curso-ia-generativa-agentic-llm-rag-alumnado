# Práctica 14. Proyecto final

El enunciado completo, los requisitos mínimos, la estructura del repositorio y la rúbrica están en [`proyecto_final/README.md`](../../proyecto_final/README.md). Lo que se hace hoy:

## 1. Finalización y pruebas (100 min)

1. Último ciclo de mejora: ejecutad la evaluación de extremo a extremo y el red teaming, corregid lo que podáis y **volved a evaluar**.
2. Actualizad `docs/informe_evaluacion.md` con los resultados finales comparados con la línea base de la sesión 13.
3. Pasad el checklist del apartado 14.2 de los apuntes y el verificador del ejercicio 1.
4. Etiquetad la versión: `git tag v1.0`.
5. Ensayad la demo completa una vez, cronometrada, con el reparto de la palabra.

## 2. Demo Day (15 + 15 min por equipo)

Seguid la estructura del apartado 14.3. El comité está formado por el docente y, si es posible, personas de la consultora en el papel de cliente.

## 3. Evaluación entre pares (16 min)

Cada persona rellena el formulario que facilite el docente:

- Para cada uno de los otros dos equipos: valor para el cliente, calidad técnica y claridad de la demo (de 1 a 5) y un comentario constructivo.
- Para su propio equipo: contribución de cada miembro (de 1 a 5) con una frase que lo justifique.

## Entrega final

Repositorio del equipo con la etiqueta `v1.0` y:

1. MVP del asistente funcionando con una orden.
2. `README.md` con instalación, uso, arquitectura y limitaciones.
3. `docs/`: ficha del agente, canvas, propuesta técnica, plan de validación, informe de evaluación, ADR y presentación.
4. `evals/golden_set.jsonl` con 30 o más casos y los resultados de la evaluación final.
5. `tests/` con 10 o más pruebas en verde.

## Criterios de evaluación del laboratorio de hoy (0 a 3 puntos cada uno)

Esta nota cuenta en el bloque de laboratorios; la demo y la defensa se puntúan con la rúbrica del proyecto final.

| Criterio | 3 puntos |
| --- | --- |
| Entrega | Etiqueta `v1.0` a tiempo y el verificador devuelve «Entrega completa: sí» |
| Último ciclo de mejora | El informe de evaluación compara con la línea base y muestra mejoras medidas, sin regresiones ocultas |
| Reproducibilidad | Una persona ajena al equipo instala y ejecuta el asistente siguiendo solo el README |
| Evaluación entre pares | Formularios completos con comentarios concretos y constructivos |
