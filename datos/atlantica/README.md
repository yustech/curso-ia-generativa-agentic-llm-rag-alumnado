# Atlántica Logística S.A. (cliente ficticio)

Todos los laboratorios y los tres retos del curso trabajan sobre los activos de una empresa **ficticia**: Atlántica Logística S.A. Los datos son sintéticos. No corresponden a ninguna empresa, persona ni cliente reales y se pueden usar sin restricciones en clase.

Usar un cliente ficticio común tiene tres ventajas: nadie introduce información real de clientes en un modelo, todos los equipos comparten el mismo contexto y los resultados se pueden comparar.

## La empresa

Operador logístico con sede en Vigo, fundado en 1998. Transporte por carretera y almacenaje para empresas de distribución y alimentación. Tiene 1.850 personas en plantilla, 420 camiones y cinco centros: Vigo, Valencia, Zaragoza, Coslada (Madrid) y Bilbao. El área de Tecnología tiene 85 personas.

Sistemas internos que aparecen en los documentos:

| Sistema | Qué es |
| --- | --- |
| Faro | Sistema de gestión del transporte (TMS), escrito en Python |
| Puerto | Sistema de gestión de almacenes (WMS) |
| Brújula | Plataforma de análisis de datos y cuadros de mando |
| Ancla | Portal del empleado (vacaciones, nóminas, formación) |
| Faro-IA | Plataforma interna de IA generativa con modelos locales |

## Contenido de esta carpeta

| Carpeta o fichero | Contenido | Se usa en |
| --- | --- | --- |
| `documentos/` | 12 documentos internos (políticas, guías, procedimientos) en Markdown | RAG (sesiones 5 a 7) y los tres retos |
| `codigo/tarifas/` | Módulo de cálculo de tarifas con deuda técnica y sin tests | Reto 1 (DevAssist) |
| `proyectos/` | Actas de reunión, un extracto del backlog (13 elementos; no incluye todas las tareas de cada sprint, por eso sus puntos no suman lo que dicen las actas) y un informe de estado del proyecto Faro 2.0 | Reto 3 (PMO Copilot) y sesión 12 |
| `infra/peticiones.jsonl` | Peticiones de entornos en lenguaje natural | Reto 2 (InfraPilot) |
| `evaluacion/` | Preguntas de evaluación del RAG y conjuntos dorados iniciales de los retos | Sesiones 4, 7 y 13 |
| `casos_uso.json` | Casos de uso para clasificar | Sesión 1 |
| `casos_alucinacion.jsonl` | Banco de preguntas para provocar alucinaciones | Sesión 4 |
| `incidentes_ia.md` | Casos de fallos de IA para analizar | Sesión 2 |
