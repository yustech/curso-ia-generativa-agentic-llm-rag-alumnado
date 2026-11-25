---
titulo: Procedimiento de gestión de cambios
codigo: ATL-OPS-008
version: 3.3
fecha: 2026-02-11
propietario: Operaciones
clasificacion: Interno
---

# Procedimiento de gestión de cambios

## 1. Tipos de cambio

| Tipo | Definición | Aprobación |
| --- | --- | --- |
| Estándar | Cambio repetitivo, de bajo riesgo y documentado en el catálogo de cambios estándar (por ejemplo, añadir un nodo al clúster con el módulo aprobado) | Preaprobado: basta con registrarlo |
| Normal | Cualquier otro cambio planificado en producción | Comité de Cambios (CAB) |
| Emergencia | Cambio necesario para resolver un incidente P1 o P2 en curso | Directora de Sistemas (CIO) por teléfono o correo |

## 2. Comité de Cambios (CAB)

- Se reúne los **jueves a las 10:00**.
- Las solicitudes de cambio normal se registran antes del **martes a las 14:00** de la misma semana.
- Toda solicitud incluye: descripción, motivo, sistemas afectados, plan de despliegue, **plan de marcha atrás (rollback)**, pruebas realizadas en preproducción, ventana propuesta y responsable.
- Una solicitud sin plan de marcha atrás se rechaza sin evaluarla.

## 3. Ventanas de cambio

Los cambios normales en producción se ejecutan en las ventanas de **martes y jueves de 22:00 a 02:00**. Fuera de ellas solo se permiten cambios estándar y de emergencia.

Durante el periodo de cierre de año (del 15 de diciembre al 7 de enero) y la semana del Black Friday solo se admiten cambios de emergencia.

## 4. Cambios de emergencia

El cambio se ejecuta tras la aprobación de la CIO y se presenta en el CAB siguiente. La revisión posterior se documenta en un plazo máximo de **48 horas**.

## 5. Cambios realizados con ayuda de IA

Un agente de IA puede preparar la solicitud de cambio y el plan de Terraform, pero **no puede aplicarlo**. La aplicación la ejecuta siempre el pipeline tras la aprobación humana registrada en la solicitud.
