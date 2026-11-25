# Acta de seguimiento · Proyecto Faro 2.0

- **Fecha:** 3 de noviembre de 2026, 10:00-11:00
- **Asistentes:** Lucía Prieto (jefa de proyecto), Andrés Couto (responsable de producto), Iván Seoane (líder técnico), Nerea Galdós (diseño), Paula Ferreiro (cliente Nortia Supermercados)

## Puntos tratados

**Estado del sprint 21.** Se cierran 26 de los 31 puntos comprometidos. Queda pendiente la integración con el GPS de los camiones frigoríficos, bloqueada porque el proveedor de telemetría no ha enviado las credenciales del entorno de pruebas.

**Petición de Nortia.** Paula pide que sus tiendas puedan ver la hora estimada de llegada de cada camión con un margen de error de ±15 minutos y recibir un aviso cuando el camión esté a 30 minutos. También quiere descargar un informe mensual de puntualidad en Excel.

**Diseño.** Nerea presenta el prototipo de la pantalla de seguimiento. Se acepta con un cambio: el mapa debe ocupar la mitad superior en móvil.

## Decisiones

1. El aviso de llegada se enviará por correo electrónico en la primera versión; las notificaciones push quedan para la segunda.
2. El informe de puntualidad se ofrecerá en CSV además de Excel.

## Acciones

| Acción | Responsable | Fecha |
| --- | --- | --- |
| Reclamar las credenciales al proveedor de telemetría | Lucía Prieto | 5/11/2026 |
| Escribir las historias de la petición de Nortia | Andrés Couto | 7/11/2026 |
| Ajustar el prototipo para móvil | Nerea Galdós | 10/11/2026 |

## Riesgos detectados

- Si el proveedor de telemetría no entrega credenciales antes del 14 de noviembre, la estimación de llegada de los frigoríficos se retrasa un sprint. Probabilidad 3, impacto 4.
