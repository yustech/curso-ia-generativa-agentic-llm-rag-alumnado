---
titulo: Metodología de gestión de proyectos de Tecnología
codigo: ATL-PMO-009
version: 4.2
fecha: 2026-01-30
propietario: Oficina de proyectos (PMO)
clasificacion: Interno
---

# Metodología de gestión de proyectos de Tecnología

## 1. Marco de trabajo

Los proyectos de desarrollo siguen Scrum con **sprints de 2 semanas**. Cada sprint empieza el lunes con la planificación y termina el viernes de la semana siguiente con la revisión y la retrospectiva.

## 2. Historias de usuario

- Formato del título: «Como <rol> quiero <objetivo> para <beneficio>».
- Cada historia tiene criterios de aceptación en formato Gherkin: «Dado <contexto>, cuando <acción>, entonces <resultado>».
- Se estiman en puntos con la serie **1, 2, 3, 5, 8 y 13**. Una historia de más de 13 puntos se divide antes de entrar en un sprint.

**Definición de preparado (DoR).** Una historia entra en un sprint si tiene título con el formato correcto, al menos dos criterios de aceptación, estimación y dependencias identificadas.

**Definición de hecho (DoD).** Una historia está hecha cuando el código está revisado e integrado, las pruebas automáticas pasan, la documentación está actualizada y el responsable de producto la ha aceptado en la revisión del sprint.

## 3. Backlog

El backlog se gestiona en la herramienta de seguimiento corporativa. Cada elemento tiene identificador (`FARO-123`), tipo (historia, tarea, error), estado (`Por hacer`, `En curso`, `En revisión`, `Hecho`), prioridad (`Alta`, `Media`, `Baja`), puntos, sprint y responsable.

## 4. Informe de estado semanal

Cada **viernes antes de las 13:00** el jefe de proyecto envía a dirección el informe de estado con esta estructura:

1. Resumen en tres líneas.
2. Semáforo general, de plazo, de coste y de alcance.
3. Avance del sprint: puntos comprometidos y completados.
4. Hitos próximos.
5. Riesgos y problemas abiertos.
6. Decisiones que se necesitan de dirección.

**Criterios del semáforo:**

| Color | Plazo y coste |
| --- | --- |
| Verde | Desviación igual o inferior al 5 % |
| Ámbar | Desviación entre el 5 % y el 15 % |
| Rojo | Desviación superior al 15 %, o un hito crítico en peligro |

## 5. Riesgos

Cada riesgo tiene descripción, probabilidad (1 a 5), impacto (1 a 5), exposición (probabilidad × impacto), responsable y plan de respuesta. Los riesgos con exposición **igual o superior a 15** se escalan al comité de dirección en el siguiente informe.

## 6. Actas

Toda reunión de seguimiento genera un acta en 24 horas con asistentes, decisiones, acciones (responsable y fecha) y riesgos detectados.
