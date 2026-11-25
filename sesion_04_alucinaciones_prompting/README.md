# Sesión 4. Limitaciones y alucinaciones · Prompt engineering

<!-- cabecera:inicio -->
| Fecha | Horario | Modalidad | Módulos | Hito |
| --- | --- | --- | --- | --- |
| Miércoles 9 de diciembre de 2026 | 09:00-15:00 | Remoto | M2 · Introducción a GenAI y LLM (2 h) + M3 · Prompt Engineering (4 h) | H1 · Fundamentos y prompting |

**Objetivo:** Detectar respuestas no fiables y diseñar prompts reproducibles orientados a una tarea.
<!-- cabecera:fin -->

Al terminar esta sesión sabrás detectar cuándo una respuesta de un LLM no es fiable, diseñar prompts reproducibles orientados a una tarea y, sobre todo, **medir** si un prompt es mejor que otro. Con esta sesión se cierra el Hito 1: fundamentos y prompting.

<!-- agenda:inicio -->
### Agenda de la sesión

| Hora | Min | Tipo | Módulo | Bloque |
| --- | --- | --- | --- | --- |
| 09:00 | 15 | Teoría | M2 | Activación: caza la alucinación |
| 09:15 | 45 | Teoría | M2 | Teoría: limitaciones de los LLM y tipos de alucinación |
| 10:00 | 60 | Práctica | M2 | Laboratorio: banco de pruebas de alucinaciones |
| 11:00 | 10 | Pausa | M3 | Pausa |
| 11:10 | 60 | Teoría | M3 | Teoría: principios de diseño de prompts |
| 12:10 | 66 | Práctica | M3 | Laboratorio: técnicas de prompting y salidas estructuradas |
| 13:16 | 80 | Práctica | M3 | Reto: rediseño de prompts y evaluación con rúbrica |
| 14:36 | 24 | Teoría | M3 | Cierre: Hito 1 y preguntas de repaso |

Teoría: 2 h 24 min · práctica: 3 h 36 min (las pausas computan en el bloque práctico).
<!-- agenda:fin -->

## Lo que entregas hoy

| Entregable | Dónde | Quién |
| --- | --- | --- |
| Plantilla de prompt estructurado del asistente (versiones 1 y 2) | `prompts/sistema_v1.md` y `prompts/sistema_v2.md` del repositorio del equipo | Equipo |
| Rúbrica de evaluación de respuestas | `docs/rubrica_respuestas.md` | Equipo |
| Conjunto dorado v0 (15 casos) y comparación de versiones | `evals/golden_set.jsonl` y `docs/evaluacion_prompts.md` | Equipo |
| Ejercicios 1 a 5 con los tests en verde | `sesion_04_alucinaciones_prompting/ejercicios/` | Cada persona |

---

## 4.1 Limitaciones de los LLM

Un LLM es extraordinario con el lenguaje y frágil en otras cosas. Conocer sus límites es lo que te permite diseñar alrededor de ellos.

| Limitación | Por qué ocurre | Cómo se mitiga |
| --- | --- | --- |
| Conocimiento congelado | Solo sabe lo que había en sus datos hasta la fecha de corte | Darle la información actual en el contexto (RAG, herramientas) |
| No conoce datos privados | Nunca vio los documentos de Atlántica | RAG con los documentos internos |
| Aritmética y conteo | Procesa tokens, no dígitos ni letras | Que llame a una función de cálculo |
| Razonamiento de varios pasos frágil | Predice tokens; no ejecuta un algoritmo | Descomponer la tarea, pedir razonamiento, verificar |
| Sensibilidad al prompt | Pequeños cambios de redacción cambian la salida | Plantillas versionadas y evaluadas |
| No determinista | Muestrea tokens | Temperatura baja, validación de la salida |
| Contexto limitado | La ventana tiene un tamaño y el medio se recuerda peor | Seleccionar lo relevante |
| Sesgos | Reproduce patrones de los datos de entrenamiento | Evaluar por grupos, instrucciones explícitas |
| Complacencia | Tiende a dar la razón al usuario y aceptar premisas falsas | Instrucciones de corregir premisas; evaluación específica |

## 4.2 Alucinaciones

Una **alucinación** es una respuesta fluida y segura que es falsa o no está respaldada por las fuentes. No es un error ocasional: es una consecuencia directa de cómo funcionan los modelos. Un LLM genera el texto más plausible, no el más verdadero, y cuando no sabe algo produce algo con la forma de una respuesta correcta.

### Tipos de alucinación

| Tipo | Ejemplo | Peligro |
| --- | --- | --- |
| Hecho inventado | Un premio que la empresa nunca ganó | Alto: parece cierto |
| Cita o referencia inventada | Artículos científicos o URL que no existen | Muy alto en informes y documentación |
| Aceptar una premisa falsa | Explicar «por qué Python dejó de tener tipado dinámico» | Alto: refuerza el error del usuario |
| Infidelidad a la fuente (intrínseca) | Resumir un acta y cambiar quién es responsable de una acción | Muy alto en RAG y en documentación |
| Extrapolación (extrínseca) | Añadir datos que no están en el documento | Alto en RAG |
| Cálculo erróneo | Un precio mal multiplicado | Alto en todo lo económico |

### Cómo se reducen

1. **Darle la información** en lugar de pedirle que la recuerde (RAG, herramientas).
2. **Permitir la abstención explícitamente**: «si la información no está en el contexto, responde "No consta en la documentación"».
3. **Exigir citas** de la fuente y comprobarlas.
4. **Temperatura baja** en tareas factuales.
5. **Verificar** con reglas, con otro modelo o con una persona.
6. **Medir** la tasa de alucinación con un banco de pruebas, que es lo que harás hoy.

Ninguna técnica elimina las alucinaciones por completo. El objetivo de diseño es que sean **raras, detectables y de bajo impacto**.

---

## 4.3 Principios de diseño de prompts

Un prompt de un sistema profesional no es una pregunta: es una **especificación**. Los componentes de un buen prompt de sistema:

| Componente | Qué contiene | Ejemplo para InfraPilot |
| --- | --- | --- |
| Rol | Quién es el asistente | «Eres el asistente de infraestructura de Atlántica Logística» |
| Objetivo | Qué tiene que conseguir | «Convertir peticiones de entornos en propuestas de Terraform conformes a la política» |
| Contexto | Información estable que necesita | Política resumida, catálogo de módulos |
| Instrucciones | Pasos o reglas de comportamiento | «Si falta el centro de coste, pídelo antes de proponer nada» |
| Formato de salida | Estructura exacta de la respuesta | «Devuelve JSON con los campos…» |
| Restricciones | Lo que no debe hacer nunca | «Nunca propongas buckets públicos. Nunca apliques cambios» |
| Ejemplos | Pares entrada-salida | Una petición válida y una no conforme |

### Reglas prácticas

- **Sé específico.** «Resume» es ambiguo; «resume en tres viñetas de menos de 20 palabras para un director» no lo es.
- **Separa instrucciones y datos** con delimitadores (`<documento>...</documento>`). Ayuda al modelo y reduce la inyección de instrucciones.
- **Di qué hacer, no solo qué no hacer.**
- **Pon las reglas en el mensaje de sistema** y los datos de cada petición en el mensaje de usuario.
- **Pide un formato verificable** (JSON con esquema) siempre que otro programa vaya a leer la salida.
- **Versiona los prompts** como el código: `sistema_v1.md`, `sistema_v2.md`, con un registro de qué cambió y por qué.

---

## 4.4 Zero-shot, one-shot y few-shot

| Técnica | Qué es | Cuándo |
| --- | --- | --- |
| Zero-shot | Solo instrucciones, sin ejemplos | Tareas comunes y claras |
| One-shot | Un ejemplo | Para fijar el formato |
| Few-shot | Varios ejemplos (3-5 suele bastar) | Para fijar criterio en casos ambiguos, estilo propio o categorías de la empresa |

Los ejemplos se pueden escribir dentro del mensaje de sistema o, mejor, como pares de mensajes `user` / `assistant` previos a la petición real: el modelo los interpreta como turnos ya resueltos.

Cuidado con los ejemplos: el modelo **copia sus patrones**, también los malos. Si todos tus ejemplos son de prioridad P2, sesgarás la salida hacia P2. Varía los ejemplos y cubre los casos frontera.

---

## 4.5 Chain of Thought

Pedir al modelo que **razone paso a paso antes de responder** (*Chain of Thought*) mejora los resultados en problemas de varios pasos: cálculos, lógica o decisiones con varias reglas. El razonamiento ocupa tokens y da al modelo «espacio» para llegar a la respuesta.

```
Razona paso a paso y termina con una línea que empiece por «Respuesta final:».
```

Tres matices profesionales:

1. **Separa el razonamiento de la respuesta** para poder extraer solo la respuesta (lo harás en el ejercicio 3).
2. **Los modelos de razonamiento** (como `qwen3:4b`) ya lo hacen internamente. Pedirles CoT explícito aporta poco y gasta más.
3. **El razonamiento no es una explicación fiable** de por qué el modelo respondió algo. No lo uses como justificación ante un cliente.

---

## 4.6 Prompts estructurados y salidas estructuradas

### Salida con esquema

Si un programa va a leer la respuesta, pídela en JSON y **valídala**. Con la API compatible con OpenAI, el servidor puede obligar al modelo a cumplir un esquema JSON (*structured outputs*). En el curso lo hace `llm.estructurado()` a partir de un modelo Pydantic:

```python
from typing import Literal
from pydantic import BaseModel, Field
from comun import llm

class Incidencia(BaseModel):
    categoria: Literal["transporte", "almacén", "sistemas"]
    prioridad: Literal["P1", "P2", "P3", "P4"]
    resumen: str = Field(max_length=120)

resultado = llm.estructurado("Faro está caído en todos los centros desde las 8:00.", Incidencia)
print(resultado.prioridad)   # P1, ya validado
```

La validación no garantiza que el contenido sea correcto, solo que tiene la forma correcta. Añade **reglas de negocio** encima: por ejemplo, toda P1 requiere intervención humana.

### Prompts estructurados

Un prompt estructurado organiza el mensaje de sistema en secciones con títulos (Rol, Objetivo, Contexto, Instrucciones, Formato, Restricciones). Es más fácil de leer, de revisar entre compañeros y de mejorar por partes. Lo implementarás como una clase en el ejercicio 2.

---

## 4.7 Optimización y evaluación de respuestas

Mejorar un prompt «a ojo» probando dos o tres preguntas es la forma más habitual de engañarse. El método profesional es:

1. **Conjunto dorado**: entre 15 y 50 casos representativos con la respuesta esperada (incluye casos frontera, ambiguos y maliciosos).
2. **Rúbrica**: qué es una respuesta correcta. Por ejemplo: exactitud (0-2), cita la fuente (0-1), formato (0-1), sabe abstenerse (0-1).
3. **Métrica automática** cuando se pueda (coincidencia de valores, JSON válido, palabras clave) y **revisión humana o LLM como juez** cuando no (sesión 12).
4. **Comparar versiones** del prompt con el mismo conjunto y quedarse con la mejor.
5. **Repetir** cada vez que cambies el prompt, el modelo o los datos: es una prueba de regresión.

Hoy empiezas el conjunto dorado de tu reto con 15 casos. Llegará a 30 o más antes del proyecto final, y es la pieza que más pesa en la evaluación del proyecto.

---

## Errores frecuentes

| Error | Síntoma | Solución |
| --- | --- | --- |
| Pedir JSON solo con palabras | A veces llega con texto alrededor | Usa `response_format` con esquema y valida |
| Ejemplos few-shot todos iguales | El modelo responde siempre lo mismo | Varía los ejemplos |
| Evaluar con las mismas preguntas que usaste para escribir el prompt | Resultados optimistas | Separa casos de desarrollo y de evaluación |
| Instrucciones contradictorias | Comportamiento errático | Revisa el prompt completo entre dos personas |
| Confiar en el razonamiento visible | Explicaciones convincentes de respuestas erróneas | Verifica la respuesta, no el razonamiento |

## Para saber más

- Guía de ingeniería de prompts de Anthropic: [docs.anthropic.com](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- Guía de prompting de OpenAI: [platform.openai.com/docs/guides/prompt-engineering](https://platform.openai.com/docs/guides/prompt-engineering)
- Wei et al. (2022), *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*: [arxiv.org/abs/2201.11903](https://arxiv.org/abs/2201.11903)
- Ji et al. (2023), *Survey of Hallucination in Natural Language Generation*: [arxiv.org/abs/2202.03629](https://arxiv.org/abs/2202.03629)
