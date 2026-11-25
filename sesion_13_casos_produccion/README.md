# Sesión 13. Casos de negocio y desarrollo de software · Definición del proyecto final

<!-- cabecera:inicio -->
| Fecha | Horario | Modalidad | Módulos | Hito |
| --- | --- | --- | --- | --- |
| Martes 22 de diciembre de 2026 | 09:00-15:00 | Remoto | M6 · Aplicaciones prácticas de IA Generativa (4 h) + M7 · Proyecto final y evaluación (2 h) | H4 · Aplicación y proyecto |

**Objetivo:** Evaluar viabilidad y diseñar una solución integradora alineada con una necesidad real.
<!-- cabecera:fin -->

Esta sesión une las piezas y mira hacia el cliente. En la primera parte verás los casos de uso de IA generativa más habituales en negocio y en desarrollo de software, cómo evaluar su viabilidad y qué hace falta para llevar un prototipo a producción: evaluación de extremo a extremo, pruebas de seguridad y pruebas de carga (con la demostración de vLLM). En la segunda cerrarás la definición del proyecto final de tu equipo.

<!-- agenda:inicio -->
### Agenda de la sesión

| Hora | Min | Tipo | Módulo | Bloque |
| --- | --- | --- | --- | --- |
| 09:00 | 15 | Teoría | M6 | Activación: de la demo al cliente |
| 09:15 | 45 | Teoría | M6 | Teoría: casos de negocio y de desarrollo de software |
| 10:00 | 70 | Práctica | M6 | Laboratorio integrador: evaluación de extremo a extremo y red teaming |
| 11:10 | 10 | Pausa | M6 | Pausa |
| 11:20 | 30 | Teoría | M6 | Teoría: del prototipo a producción (demo de vLLM) |
| 11:50 | 70 | Práctica | M6 | Laboratorio: prueba de carga y panel de métricas |
| 13:00 | 30 | Teoría | M7 | Teoría: qué se evalúa en el proyecto final |
| 13:30 | 66 | Práctica | M7 | Taller: canvas, propuesta técnica y plan de validación |
| 14:36 | 24 | Teoría | M7 | Cierre: ensayo relámpago de la demo |

Teoría: 2 h 24 min · práctica: 3 h 36 min (las pausas computan en el bloque práctico).
<!-- agenda:fin -->

## Lo que entregas hoy

| Entregable | Dónde | Quién |
| --- | --- | --- |
| Canvas del caso de uso | `docs/canvas_caso_uso.md` del repositorio del equipo | Equipo |
| Propuesta técnica | `docs/propuesta_tecnica.md` | Equipo |
| Plan de validación con resultados de evaluación, seguridad y carga | `docs/plan_validacion.md` | Equipo |
| Ejercicios 1 a 4 con los tests en verde | `sesion_13_casos_produccion/ejercicios/` | Cada persona |

---

## 13.1 Casos de uso en negocio

| Área | Casos frecuentes | Patrón técnico | Riesgo típico |
| --- | --- | --- | --- |
| Atención al cliente | Respuesta a consultas, clasificación y enrutado de tickets, resumen de conversaciones | RAG + clasificación + traspaso a persona | Prometer lo que la empresa no puede cumplir |
| Ventas y marketing | Propuestas comerciales, fichas de producto, análisis de oportunidades | Generación con plantilla y datos del CRM | Datos inventados en propuestas |
| Recursos humanos | Asistente de políticas internas, onboarding | RAG | Alto riesgo regulatorio si toca selección o evaluación |
| Jurídico y cumplimiento | Revisión de contratos frente a una política, extracción de cláusulas | Extracción + comparación | Errores con consecuencias legales: revisión humana obligatoria |
| Operaciones | Análisis de incidencias, informes, procedimientos | Agente de solo lectura + documentación | Acciones sin supervisión |
| Dirección | Informes de estado y cuadros de mando narrados | Generación controlada | Cifras incorrectas |

## 13.2 Casos de uso en desarrollo de software

| Caso | Qué se automatiza | Control imprescindible |
| --- | --- | --- |
| Asistentes de código en el IDE | Autocompletado, explicaciones, refactorizaciones | Revisión de código humana y pruebas |
| Generación de pruebas | Pruebas unitarias a partir de código o criterios de aceptación | Que las pruebas fallen cuando el código está mal (pruebas de mutación) |
| Revisión de merge requests | Detección de incumplimientos de estilo, errores, vulnerabilidades | Análisis estático determinista + criterio humano |
| Documentación | Docstrings, README, notas de versión, documentación de API | Coherencia con el código |
| Migración y modernización | Traducir código heredado, actualizar dependencias | Pruebas de regresión |
| Infraestructura como código | Generar Terraform o Kubernetes a partir de peticiones | Validación de política y plan revisado |
| Análisis de incidencias | Resumir registros, proponer causa raíz | Solo lectura; la acción la hace una persona |

Los tres retos del curso son tres de estos casos. Lo que habéis aprendido con ellos (RAG para la normativa, herramientas deterministas para lo verificable, confirmación humana para lo que tiene efectos) se aplica a todos.

## 13.3 Evaluar la viabilidad

Antes de construir, un consultor responde cuatro preguntas:

| Pregunta | Cómo se responde |
| --- | --- |
| ¿Aporta valor suficiente? | Horas ahorradas (con el tiempo de revisión), mejora de calidad, ingresos |
| ¿Hay datos? | Documentos, sistemas con API, conjunto de evaluación posible |
| ¿Qué riesgo tiene? | Impacto de un error, regulación (Reglamento Europeo de IA, RGPD), reputación |
| ¿Cuánto cuesta? | Implantación (desarrollo, integración, formación) y operación (infraestructura, mantenimiento, supervisión) |

Con esos números: beneficio mensual, meses de recuperación y retorno del primer año (ejercicio 4). Un caso con buen retorno pero datos inmaduros o riesgo alto empieza como **piloto acotado**, no como proyecto completo.

---

## 13.4 Del prototipo a producción

| Dimensión | Prototipo | Producción |
| --- | --- | --- |
| Calidad | Funciona con mis ejemplos | Medida con un conjunto dorado y umbrales, con prueba de regresión en cada cambio |
| Seguridad | Prompt con instrucciones | Pruebas de ataque, guardarraíles en código, mínimo privilegio, auditoría |
| Rendimiento | Una persona en mi portátil | Muchos usuarios a la vez con latencia acotada |
| Coste | Despreciable | Calculado y vigilado por petición |
| Operación | Lo arranco yo | Despliegue, monitorización, alertas, actualizaciones de modelo |
| Gobierno | — | Ficha del sistema, inventario de IA, clasificación de riesgo, responsable |

### Servir modelos a muchos usuarios: vLLM

Ollama es excelente para desarrollar y para pocos usuarios. Con muchos usuarios simultáneos, el estándar en servidores propios es **vLLM**, que aporta:

| Técnica | Qué hace |
| --- | --- |
| *Continuous batching* | Agrupa en tiempo real las peticiones de muchos usuarios para aprovechar la GPU |
| *PagedAttention* | Gestiona la caché KV en bloques, como la memoria virtual, sin desperdiciar memoria |
| Paralelismo tensorial | Reparte un modelo grande entre varias GPU |
| API compatible con OpenAI | Tu código no cambia: cambia la URL |

```bash
# En el servidor compartido (lo arranca el docente):
vllm serve <modelo> --port 8000 --api-key <clave> --max-model-len 16384 --gpu-memory-utilization 0.45
```

Requiere Linux y GPU NVIDIA, y usa modelos en formato de Hugging Face (no GGUF). Por eso en el curso solo está en el servidor.

### Métricas de rendimiento

| Métrica | Qué mide | Para quién |
| --- | --- | --- |
| Latencia p50 / p95 | Tiempo de respuesta típico y del 5 % más lento | Experiencia de la persona usuaria |
| Tiempo hasta el primer token | Cuándo empieza a verse la respuesta | Interfaces con streaming |
| Tokens por segundo (agregado) | Capacidad total del servidor | Dimensionamiento |
| Peticiones por segundo | Rendimiento del servicio | Dimensionamiento |
| Tasa de errores | Peticiones fallidas o con timeout | Fiabilidad |

Una prueba de carga mide estas métricas con 1, 2, 4, 8… usuarios simultáneos. Con Ollama la latencia crece casi linealmente al aumentar usuarios; con vLLM crece mucho menos porque agrupa las peticiones.

---

## 13.5 Evaluación de extremo a extremo

La evaluación final del asistente combina lo que has ido construyendo:

1. **Conjunto dorado** de 30 o más casos de todos los tipos (normativa, tarea, ambigua, fuera de alcance, seguridad).
2. **Ejecución automática** del asistente completo (RAG, herramientas, guardarraíles) midiendo la latencia.
3. **Juez** con rúbrica (0 incorrecta, 1 parcial, 2 correcta) calibrado con revisión humana de una muestra.
4. **Métricas**: exactitud global y por tipo, latencia p50 y p95.
5. **Línea base** guardada y **detección de regresiones** en cada cambio de prompt, modelo o datos.

## 13.6 Red teaming y OWASP Top 10 para LLM

El **red teaming** es atacar tu propio sistema para encontrar sus debilidades antes que otros. La referencia es el OWASP Top 10 para aplicaciones LLM (versión 2025):

| Código | Riesgo | Ataque de ejemplo |
| --- | --- | --- |
| LLM01 | Inyección de prompt | «Ignora tus instrucciones…», directa o escondida en un documento |
| LLM02 | Divulgación de información sensible | Pedir credenciales o datos de otros usuarios |
| LLM03 | Cadena de suministro | Modelos o servidores MCP de origen dudoso |
| LLM04 | Envenenamiento de datos y modelos | Documentos manipulados en el índice del RAG |
| LLM05 | Gestión insegura de la salida | La salida contiene código o HTML que otro sistema ejecuta |
| LLM06 | Autonomía excesiva | Que el agente aplique cambios sin aprobación |
| LLM07 | Filtrado del prompt de sistema | Pedir que revele sus instrucciones |
| LLM08 | Debilidades de vectores y embeddings | Acceso a documentos de otro cliente en un índice compartido |
| LLM09 | Desinformación | Que confirme una premisa falsa sobre la política |
| LLM10 | Consumo no acotado | Peticiones que generan salidas enormes o bucles caros |

En el ejercicio 2 automatizarás un conjunto de ataques con detectores. Las defensas ya las conoces: guardarraíles en capas (sesión 8), herramientas de mínimo privilegio (sesión 9), confirmación humana y límites de longitud y de pasos.

---

## 13.7 Qué se evalúa en el proyecto final

El proyecto final es el asistente de tu equipo terminado. Los criterios mínimos del programa del curso:

1. Asistente basado en LLM con una necesidad y unos usuarios definidos.
2. Componente RAG con fuentes identificadas, estrategia de indexación y pruebas de recuperación.
3. Al menos una herramienta o acción controlada.
4. Métricas y conjunto de pruebas para calidad, relevancia y robustez.
5. Controles de privacidad, seguridad, uso responsable y supervisión humana.
6. Documentación reproducible, demo funcional y explicación de las decisiones.

El enunciado completo, la rúbrica y el formato de la demo están en [`proyecto_final/README.md`](../proyecto_final/README.md).

---

## Errores frecuentes

| Error | Síntoma | Solución |
| --- | --- | --- |
| Calcular el ahorro sin el tiempo de revisión | Retorno irreal | Medirlo en el TO-BE |
| Probar seguridad solo con ataques obvios | Falsa confianza | Ataques indirectos y por categorías |
| Medir rendimiento con un solo usuario | Sorpresas en producción | Prueba de carga con concurrencia creciente |
| Cambiar el prompt sin volver a evaluar | Regresiones silenciosas | Línea base y comparación automática |
| Definir el proyecto final sin conjunto dorado | No se puede demostrar que funciona | Plan de validación antes de seguir construyendo |

## Para saber más

- OWASP, *Top 10 for LLM Applications 2025*: [genai.owasp.org/llm-top-10](https://genai.owasp.org/llm-top-10/)
- Documentación de vLLM: [docs.vllm.ai](https://docs.vllm.ai/)
- Kwon et al. (2023), *Efficient Memory Management for Large Language Model Serving with PagedAttention*: [arxiv.org/abs/2309.06180](https://arxiv.org/abs/2309.06180)
- NIST, *AI Risk Management Framework*: [nist.gov/itl/ai-risk-management-framework](https://www.nist.gov/itl/ai-risk-management-framework)
