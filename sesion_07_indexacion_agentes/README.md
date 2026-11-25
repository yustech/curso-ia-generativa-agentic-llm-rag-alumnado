# Sesión 7. Indexación y evaluación RAG · Introducción a los agentes

<!-- cabecera:inicio -->
| Fecha | Horario | Modalidad | Módulos | Hito |
| --- | --- | --- | --- | --- |
| Lunes 14 de diciembre de 2026 | 09:00-15:00 | Presencial | M4 · RAG (Retrieval-Augmented Generation) (2 h) + M5 · Agentic AI y herramientas avanzadas (4 h) | H2 · Sistema RAG |

**Objetivo:** Construir un índice básico, evaluar su recuperación y diferenciar chatbot, workflow y agente.
<!-- cabecera:fin -->

Esta sesión cierra el bloque de RAG y abre el de agentes. En la primera parte construirás un pipeline de ingesta que se mantiene al día solo y aprenderás a evaluar un RAG de extremo a extremo con un checklist de calidad. En la segunda entenderás qué es un agente, en qué se diferencia de un chatbot y de un workflow, y programarás tu primer bucle de agente sin frameworks.

Es la sesión presencial de mitad de curso: termina con la **revisión intermedia** de cada equipo.

<!-- agenda:inicio -->
### Agenda de la sesión

| Hora | Min | Tipo | Módulo | Bloque |
| --- | --- | --- | --- | --- |
| 09:00 | 15 | Teoría | M4 | Activación: reglas de la revisión intermedia |
| 09:15 | 45 | Teoría | M4 | Teoría: indexación y evaluación de la recuperación |
| 10:00 | 60 | Práctica | M4 | Laboratorio: pipeline de ingesta y métricas de recuperación |
| 11:00 | 10 | Pausa | M5 | Pausa |
| 11:10 | 60 | Teoría | M5 | Teoría: introducción a los agentes |
| 12:10 | 66 | Práctica | M5 | Laboratorio: tu primer bucle de agente |
| 13:16 | 80 | Práctica | M5 | Reto: clasificación de soluciones y ficha de patrón del agente |
| 14:36 | 24 | Teoría | M5 | Cierre: revisión intermedia presencial (8 min por equipo) |

Teoría: 2 h 24 min · práctica: 3 h 36 min (las pausas computan en el bloque práctico).
<!-- agenda:fin -->

## Lo que entregas hoy

| Entregable | Dónde | Quién |
| --- | --- | --- |
| Índice consultable del reto con ingesta incremental | `rag/ingesta.py` del repositorio del equipo | Equipo |
| Checklist de calidad del RAG con métricas | `docs/checklist_rag.md` | Equipo |
| Ficha de patrón del agente | `docs/ficha_patron_agente.md` | Equipo |
| Ejercicios 1 a 3 con los tests en verde | `sesion_07_indexacion_agentes/ejercicios/` | Cada persona |

---

## 7.1 El pipeline de ingesta en producción

En la sesión 5 indexaste los documentos una vez. En un cliente real los documentos cambian cada día, y reconstruir el índice entero cada vez es lento y caro. Un pipeline de ingesta profesional:

| Paso | Qué hace | Detalle práctico |
| --- | --- | --- |
| Descubrir | Lista los documentos de las fuentes | Carpetas, SharePoint, wikis, bases de datos |
| Detectar cambios | Compara cada documento con la última versión indexada | **Huella** (hash) del contenido en un manifiesto |
| Extraer y limpiar | Convierte a texto conservando la estructura | Títulos, tablas y listas |
| Trocear | Divide en fragmentos | Por secciones, con título |
| Enriquecer | Añade metadatos | Documento, sección, versión, clasificación, fecha, huella |
| Vectorizar | Calcula embeddings por lotes | Mismo modelo que en la consulta |
| Indexar | `upsert` de lo nuevo y modificado; borrado de lo eliminado | Ids estables por documento y posición |
| Registrar | Guarda el manifiesto y un informe | Qué cambió, cuántos trozos, errores |

La **ingesta incremental** solo reprocesa lo que cambió: si de 4.000 documentos se modifican 12, solo se recalculan esos 12. Lo implementarás en el ejercicio 1 con una huella SHA-256 por documento.

Dos detalles que dan problemas en proyectos reales:

- **Al modificar un documento hay que borrar sus trozos anteriores** antes de indexar los nuevos: si el documento pasó de 5 secciones a 4, el quinto trozo antiguo seguiría en el índice respondiendo con información obsoleta.
- **Si cambias de modelo de embeddings o de estrategia de troceado, hay que reindexarlo todo.** Guarda en el manifiesto con qué modelo se indexó.

---

## 7.2 Evaluar un RAG de extremo a extremo

En la sesión 6 mediste la recuperación. Un RAG completo se evalúa en dos niveles:

| Nivel | Pregunta | Métrica del curso | Herramientas en el mercado |
| --- | --- | --- | --- |
| Recuperación | ¿Llega la fuente correcta al modelo? | Hit@k, MRR | Las mismas en Ragas o DeepEval (*context recall*) |
| Generación: fidelidad | ¿La respuesta se apoya en los fragmentos? | ¿Cita la fuente correcta? | *Faithfulness* con LLM como juez |
| Generación: respuesta | ¿Responde lo que se esperaba? | Cobertura de términos clave | *Answer relevancy*, *answer correctness* |
| Generación: prudencia | ¿Se abstiene cuando no hay fuente? | Tasa de abstención correcta | Casos negativos del conjunto |

### Checklist de calidad

Antes de enseñar un RAG a un cliente, fija **umbrales** y compruébalos con un conjunto de preguntas:

| Criterio | Umbral orientativo |
| --- | --- |
| La fuente correcta está entre los `k` recuperados | ≥ 85 % |
| Se abstiene en todas las preguntas sin fuente | 100 % |
| Cita la fuente correcta | ≥ 80 % |
| Cubre los términos clave de la respuesta esperada | ≥ 50 % |
| Latencia p95 | Según el caso de uso |

Los umbrales los decide el negocio según el riesgo. Lo importante es que existan, que se midan siempre igual y que una caída bloquee el despliegue (lo automatizarás en la sesión 13).

---

## 7.3 Qué es un agente

Un **agente** es un sistema en el que un LLM **decide qué acciones tomar** para alcanzar un objetivo, las ejecuta mediante herramientas, observa el resultado y repite hasta terminar.

| Componente | Qué es | En Atlántica |
| --- | --- | --- |
| Modelo | El LLM que razona y decide | `granite4:micro` o un modelo mayor del servidor |
| Instrucciones | Objetivo, reglas y límites | «Nunca apliques cambios en producción» |
| Herramientas | Funciones que puede invocar | Buscar en la documentación, validar Terraform, consultar el backlog |
| Memoria y estado | Lo que recuerda durante y entre tareas | Historial, datos de la petición en curso |
| Bucle | Decidir → actuar → observar | Hasta responder o alcanzar el máximo de pasos |

### Cómo usa herramientas un LLM (*tool calling*)

El modelo no ejecuta nada. Recibe la descripción de las herramientas (nombre, descripción y esquema JSON de los parámetros) y, cuando decide usar una, devuelve un mensaje especial con el nombre y los argumentos. **Tu programa** la ejecuta y le devuelve el resultado en un mensaje de rol `tool`.

```
usuario: «¿Cuánto cuestan dos m6i.large y una db.t3.medium?»
   modelo → tool_call: buscar_documentacion(consulta="coste m6i.large db.t3.medium")
programa → tool: «[1] ... m6i.large 85 € ... db.t3.medium 70 € ...»
   modelo → tool_call: calcular(expresion="2 * 85 + 70")
programa → tool: «240»
   modelo → «Según el catálogo (ATL-INF-007), 240 € al mes.»
```

Fíjate en que el agente **combina** RAG (buscar en la documentación) con una herramienta de cálculo, que resuelve la limitación aritmética de la sesión 4.

---

## 7.4 Chatbot, workflow y agente

| | Chatbot (con o sin RAG) | Workflow con LLM | Agente |
| --- | --- | --- | --- |
| Quién decide los pasos | Nadie: pregunta y respuesta | El programador, de antemano | El modelo, en cada ejecución |
| Flujo | Fijo | Fijo, con pasos que usan el LLM | Dinámico |
| Previsibilidad | Alta | Alta | Menor |
| Coste y latencia | Bajos | Medios y predecibles | Variables y mayores |
| Cuándo | Responder preguntas | El proceso se conoce y se repite | El camino depende de lo que se vaya encontrando |
| Ejemplo | Asistente de vacaciones | Acta → extraer acciones → crear historias → informe | «Prepara el entorno de pre de Faro» con validaciones y aclaraciones |

**La recomendación profesional: usa el sistema más simple que resuelva el problema.** Muchos «agentes» de las demos son mejores como workflows: más baratos, más fiables y más fáciles de probar. Un agente se justifica cuando los pasos no se pueden prever.

### Patrones intermedios

Entre el workflow fijo y el agente autónomo hay patrones muy útiles:

| Patrón | Qué hace | Ejemplo |
| --- | --- | --- |
| Encadenamiento | Pasos fijos, cada uno con el LLM | Extraer → resumir → traducir |
| Enrutador | El LLM clasifica y se elige un camino | Pregunta de normativa → RAG; de backlog → herramienta |
| Paralelización | Varios LLM a la vez y se combinan | Revisar un código desde tres puntos de vista |
| Orquestador-trabajadores | Un LLM reparte subtareas | Informe con secciones que escriben otros |
| Evaluador-optimizador | Un LLM genera y otro critica hasta aprobar | Historia de usuario revisada contra la definición de preparado |

---

## 7.5 El bucle del agente

```python
mensajes = [sistema, objetivo]
for paso in range(MAX_PASOS):
    respuesta = llm(mensajes, herramientas)
    if no hay llamadas a herramientas:
        return respuesta                       # terminado
    mensajes.append(respuesta)                 # la petición de herramienta del modelo
    for llamada in respuesta.llamadas:
        resultado = ejecutar(llamada)          # ¡tu código, con tus controles!
        mensajes.append(resultado)             # rol "tool"
return "No he podido completarlo"              # límite de pasos
```

Cuatro reglas de diseño que aplicarás desde hoy:

1. **Límite de pasos siempre.** Un agente sin límite puede entrar en un bucle infinito y costoso.
2. **Las herramientas nunca lanzan excepciones al modelo**: devuelven un error legible para que el modelo pueda reaccionar.
3. **Valida los argumentos** que propone el modelo antes de ejecutar (sesión 9).
4. **Registra cada paso**: herramienta, argumentos y resultado. Sin trazas no sabrás por qué el agente hizo lo que hizo (sesión 8).

---

## Errores frecuentes

| Error | Síntoma | Solución |
| --- | --- | --- |
| No borrar los trozos antiguos al modificar un documento | El asistente responde con información obsoleta | Borrar por documento antes de reindexar |
| Evaluar solo con preguntas que tienen respuesta | El sistema nunca aprende a abstenerse | Incluir preguntas sin fuente |
| Usar `eval()` en una herramienta de cálculo | Ejecución de código arbitrario | Evaluador seguro con `ast` |
| Olvidar el `tool_call_id` en el mensaje de la herramienta | Error de la API | Copiar el id de cada llamada |
| Agente para un proceso que siempre es igual | Coste y fallos innecesarios | Workflow |

## Para saber más

- Anthropic, *Building effective agents*: [anthropic.com/research/building-effective-agents](https://www.anthropic.com/research/building-effective-agents)
- Documentación de Ragas (métricas de RAG): [docs.ragas.io](https://docs.ragas.io/)
- Guía de tool calling de Ollama: [docs.ollama.com/capabilities/tool-calling](https://docs.ollama.com/capabilities/tool-calling)
