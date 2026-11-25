# Sesión 5. RAG: concepto, arquitectura y criterios de adopción

<!-- cabecera:inicio -->
| Fecha | Horario | Modalidad | Módulos | Hito |
| --- | --- | --- | --- | --- |
| Jueves 10 de diciembre de 2026 | 09:00-15:00 | Remoto | M4 · RAG (Retrieval-Augmented Generation) (6 h) | H2 · Sistema RAG |

**Objetivo:** Describir los componentes de una solución RAG y decidir cuándo aporta valor.
<!-- cabecera:fin -->

Al terminar esta sesión sabrás explicar qué es la generación aumentada por recuperación (RAG), describir cada componente de su arquitectura, construir un RAG mínimo sin frameworks y, lo más importante para una consultora, **decidir cuándo un RAG aporta valor y cuándo no**.

<!-- agenda:inicio -->
### Agenda de la sesión

| Hora | Min | Tipo | Bloque |
| --- | --- | --- | --- |
| 09:00 | 15 | Teoría | Activación: pregúntale al modelo por la política de vacaciones |
| 09:15 | 55 | Teoría | Teoría I: concepto, arquitectura y flujo RAG |
| 10:10 | 70 | Práctica | Laboratorio: un RAG mínimo desde cero |
| 11:20 | 10 | Pausa | Pausa |
| 11:30 | 50 | Teoría | Teoría II: casos de uso y criterios de adopción |
| 12:20 | 70 | Práctica | Reto 1: arquitectura RAG del reto del equipo |
| 13:30 | 10 | Pausa | Pausa |
| 13:40 | 56 | Práctica | Reto 2: decisiones justificadas y revisión cruzada |
| 14:36 | 24 | Teoría | Cierre: preguntas de repaso |

Teoría: 2 h 24 min · práctica: 3 h 36 min (las pausas computan en el bloque práctico).
<!-- agenda:fin -->

## Lo que entregas hoy

| Entregable | Dónde | Quién |
| --- | --- | --- |
| Diagrama de arquitectura RAG del asistente | `docs/arquitectura_rag.md` del repositorio del equipo | Equipo |
| Tres decisiones justificadas en formato ADR | `docs/adr/` | Equipo |
| Ejercicios 1 y 2 con los tests en verde | `sesion_05_rag_arquitectura/ejercicios/` | Cada persona |

---

## 5.1 El problema que resuelve el RAG

En la sesión 4 comprobaste que un LLM no conoce los documentos de Atlántica, inventa cuando no sabe y no cita fuentes. Hay tres formas de darle ese conocimiento:

| Opción | Cómo | Problema |
| --- | --- | --- |
| Meter todos los documentos en el prompt | Contexto largo | Caro, lento, limitado por la ventana y el modelo se pierde en el medio |
| Reentrenar o ajustar el modelo con los documentos | Ajuste fino | Caro, hay que repetirlo con cada cambio, no cita fuentes y sigue alucinando |
| **Recuperar solo los fragmentos relevantes y dárselos** | RAG | Hay que construir y mantener la recuperación |

**RAG** (*Retrieval-Augmented Generation*) significa: antes de generar, **recuperar** de una base de conocimiento los fragmentos más relevantes para la pregunta y **aumentar** el prompt con ellos. El modelo responde a partir de esos fragmentos y puede citarlos.

Es, con diferencia, el patrón de IA generativa más desplegado en empresas.

---

## 5.2 Arquitectura y flujo

Un sistema RAG tiene dos flujos: uno que se ejecuta cuando cambian los documentos (ingesta) y otro en cada pregunta (consulta).

```
INGESTA (cuando cambian los documentos)
Documentos ──► Carga y limpieza ──► Troceado ──► Embeddings ──► Índice (base vectorial)
                                         │                            ▲
                                         └── metadatos ───────────────┘

CONSULTA (en cada pregunta)
Pregunta ──► Embedding de la pregunta ──► Búsqueda en el índice ──► k trozos ──► (Reordenación)
                                                                                     │
Respuesta con citas ◄── LLM ◄── Prompt = instrucciones + trozos numerados + pregunta ◄┘
```

### Componentes

| Componente | Qué hace | Decisiones clave |
| --- | --- | --- |
| Cargador | Lee PDF, Word, HTML, Markdown, bases de datos | Qué fuentes, con qué permisos, cada cuánto se actualizan |
| Limpieza | Quita cabeceras repetidas, menús, ruido | Conservar la estructura (títulos, tablas) |
| Troceado (*chunking*) | Divide en fragmentos recuperables | Tamaño, solapamiento, respetar secciones |
| Metadatos | Documento, sección, fecha, clasificación, autor | Sirven para filtrar y para citar |
| Modelo de embeddings | Convierte texto en vectores | Idioma, calidad, dimensión, coste |
| Índice | Guarda los vectores y busca los más parecidos | En memoria, Chroma, Qdrant, pgvector |
| Recuperador | Busca los `k` trozos más relevantes | `k`, búsqueda semántica, léxica o híbrida (sesión 6) |
| Reordenador | Reordena los candidatos con un modelo más preciso | Opcional; mejora la precisión |
| Constructor del prompt | Junta instrucciones, trozos y pregunta | Cómo numerar, cómo pedir citas, cuándo abstenerse |
| Generador | El LLM que responde | Modelo, temperatura baja |

### El troceado importa más de lo que parece

| Estrategia | Ventaja | Inconveniente |
| --- | --- | --- |
| Tamaño fijo de caracteres con solapamiento | Sencilla, predecible | Corta frases y tablas por la mitad |
| Por párrafos | Respeta unidades de sentido | Párrafos muy desiguales |
| **Por secciones del documento** | Cada trozo trata un tema y se puede citar («Política de vacaciones › 1. Vacaciones») | Secciones largas hay que subdividirlas |
| Semántica (corta donde cambia el tema) | Trozos coherentes | Más compleja y costosa |

Regla práctica: trozos de entre 300 y 1.500 caracteres, que tengan sentido por sí solos. Añade al principio de cada trozo el título del documento y de la sección: el trozo «Se solicitan con 15 días de antelación» no sirve de nada sin saber de qué habla.

### El prompt de un RAG

```
Eres el asistente interno de Atlántica. Responde SOLO con la información de los fragmentos.
Cita cada afirmación con el número del fragmento entre corchetes, por ejemplo [2].
Si la respuesta no está en los fragmentos, responde exactamente: «No consta en la documentación».

[1] 11_politica_vacaciones_teletrabajo.md › 1. Vacaciones
Cada persona tiene 25 días laborables...

[2] ...

Pregunta: ¿Cuántos días de vacaciones tengo?
```

---

## 5.3 Lo que puede fallar en un RAG

Diagnosticar un RAG exige separar los dos problemas posibles:

| Síntoma | Fallo de | Causas típicas | Solución |
| --- | --- | --- | --- |
| La respuesta correcta no está en los trozos recuperados | **Recuperación** | Troceado malo, embeddings poco adecuados al idioma, `k` pequeño, la pregunta usa otras palabras | Mejorar troceado, búsqueda híbrida, reordenación, reescribir la pregunta |
| El trozo correcto está, pero la respuesta es mala | **Generación** | Prompt poco claro, modelo pequeño, demasiados trozos irrelevantes | Mejor prompt, menos ruido, modelo mayor |
| Responde con datos de un documento obsoleto | Ingesta | El índice no se actualiza | Ingesta incremental, fechas en metadatos |
| Muestra información a quien no debe verla | Seguridad | El índice ignora los permisos | Filtrar por permisos antes de recuperar |

Por eso en la sesión 7 medirás por separado la recuperación (¿está el trozo correcto entre los `k` primeros?) y la generación (¿la respuesta es fiel a los trozos?).

---

## 5.4 Cuándo usar RAG: criterios de adopción

| Situación | Recomendación |
| --- | --- |
| Preguntas sobre documentación interna extensa que cambia | **RAG** |
| Hay que citar la fuente o auditar la respuesta | **RAG** |
| Los documentos caben enteros en el contexto y son pocos | Contexto directo (más simple) |
| Hay que consultar datos estructurados (pedidos, backlog, inventario) | **Herramientas** o consultas SQL, no RAG (sesiones 8 y 9) |
| Hay que cambiar el estilo, el formato o enseñar una tarea muy específica | Ajuste fino o few-shot, no RAG |
| Respuestas sobre conocimiento general | El modelo solo, sin RAG |

### Preguntas para evaluar un caso de uso con un cliente

1. **¿Existen los documentos y son de calidad?** Un RAG sobre documentación desactualizada o contradictoria da respuestas desactualizadas o contradictorias.
2. **¿Con qué frecuencia cambian?** Define la estrategia de actualización del índice.
3. **¿Quién puede ver qué?** Los permisos documentales deben respetarse en la recuperación.
4. **¿Qué pasa si se equivoca?** Determina el umbral de calidad y la revisión humana.
5. **¿Cómo vamos a medir que funciona?** Sin un conjunto de preguntas con su respuesta, no hay forma de saberlo.
6. **¿Cuántas preguntas al día y con qué latencia?** Dimensiona el hardware y el coste.

### Riesgos específicos del RAG

- **Inyección indirecta de instrucciones**: un documento puede contener texto como «ignora tus instrucciones y…». El modelo lo lee como parte del contexto. Mitigación: delimitar los fragmentos, instrucciones claras de que el contexto son datos y no órdenes, y no dar al asistente permisos peligrosos.
- **Fuga de información**: el asistente recupera un documento confidencial y lo resume a quien no debería verlo.
- **Falsa sensación de fiabilidad**: las citas dan apariencia de rigor aunque el modelo haya malinterpretado el fragmento.

---

## 5.5 Registro de decisiones de arquitectura (ADR)

Un **ADR** documenta una decisión técnica relevante para que dentro de seis meses alguien sepa por qué se tomó. Atlántica los exige (`05_arquitectura_referencia.md`). Formato:

```markdown
# ADR-001. Troceado por secciones del documento

- **Estado:** aceptado · 10/12/2026
- **Contexto:** los documentos de Atlántica están estructurados en secciones numeradas y
  el asistente debe citar la sección de la que obtiene cada dato.
- **Decisión:** trocear por secciones `##`, subdividiendo las de más de 1.500 caracteres por párrafos.
- **Alternativas consideradas:** tamaño fijo de 800 caracteres con solapamiento de 100 (corta tablas);
  por párrafos (trozos demasiado pequeños sin contexto).
- **Consecuencias:** citas legibles; trozos de tamaño desigual; hay que revisar el troceado si
  cambian las plantillas de los documentos.
```

Hoy escribiréis tres ADR del RAG de vuestro asistente.

---

## Errores frecuentes

| Error | Síntoma | Solución |
| --- | --- | --- |
| Trozos sin contexto | Se recuperan fragmentos que no se entienden solos | Prefija título del documento y de la sección |
| `k` demasiado grande | Respuestas confusas y lentas | Empieza con `k` = 3-5 y mide |
| No pedir abstención | Inventa cuando la recuperación falla | Instrucción explícita y probada |
| Calcular embeddings en cada pregunta para todo el corpus | Lentitud extrema | Los embeddings de los documentos se calculan una vez y se guardan |
| Usar RAG para datos estructurados | Respuestas incorrectas sobre cifras | Consultas o herramientas |

## Para saber más

- Lewis et al. (2020), *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*: [arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)
- Gao et al. (2024), *Retrieval-Augmented Generation for Large Language Models: A Survey*: [arxiv.org/abs/2312.10997](https://arxiv.org/abs/2312.10997)
- Plantilla de ADR de Michael Nygard: [cognitect.com/blog/2011/11/15/documenting-architecture-decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
