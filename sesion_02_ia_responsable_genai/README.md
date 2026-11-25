# Sesión 2. IA responsable, panorama de herramientas y fundamentos de la IA generativa

<!-- cabecera:inicio -->
| Fecha | Horario | Modalidad | Módulos | Hito |
| --- | --- | --- | --- | --- |
| Jueves 3 de diciembre de 2026 | 08:00-14:00 | Por confirmar | M1 · Introducción a la Inteligencia Artificial (2 h) + M2 · Introducción a GenAI y LLM (4 h) | H1 · Fundamentos y prompting |

**Objetivo:** Aplicar criterios de IA responsable y explicar qué hace generativo a un modelo.
<!-- cabecera:fin -->

Al terminar esta sesión sabrás identificar los riesgos de un caso de uso de IA y proponer controles concretos, conocerás el panorama de herramientas para trabajar con modelos y entenderás qué hace «generativo» a un modelo. Además harás tus primeras llamadas a un LLM desde Python.

<!-- agenda:inicio -->
### Agenda de la sesión

| Hora | Min | Tipo | Módulo | Bloque |
| --- | --- | --- | --- | --- |
| 08:00 | 15 | Teoría | M1 | Activación: cuando la IA se equivoca en público |
| 08:15 | 45 | Teoría | M1 | Teoría: ética, privacidad, sesgos y marco regulatorio; panorama de herramientas |
| 09:00 | 60 | Práctica | M1 | Laboratorio: matriz de riesgos y controles del reto |
| 10:00 | 10 | Pausa | M2 | Pausa |
| 10:10 | 60 | Teoría | M2 | Teoría: fundamentos de la IA generativa |
| 11:10 | 66 | Práctica | M2 | Laboratorio: primeras llamadas a un LLM local desde Python |
| 12:16 | 80 | Práctica | M2 | Reto: comparación guiada de herramientas y modelos |
| 13:36 | 24 | Teoría | M2 | Cierre: conclusiones y preguntas de repaso |

Teoría: 2 h 24 min · práctica: 3 h 36 min (las pausas computan en el bloque práctico).
<!-- agenda:fin -->

## Lo que entregas hoy

| Entregable | Dónde | Quién |
| --- | --- | --- |
| Matriz de riesgos y controles del reto | `docs/matriz_riesgos.md` del repositorio del equipo | Equipo |
| Cuadro comparativo de herramientas y modelos | `docs/comparativa_herramientas.md` | Equipo |
| Ejercicios 1 a 3 con los tests en verde | `sesion_02_ia_responsable_genai/ejercicios/` | Cada persona |

---

## 2.1 Ética y riesgos de la IA

Un sistema de IA puede funcionar técnicamente y aun así causar daño. Estos son los riesgos que vas a revisar en cualquier proyecto:

| Riesgo | Qué es | Ejemplo | Control típico |
| --- | --- | --- | --- |
| Sesgo y discriminación | El sistema trata peor a un grupo porque los datos reflejan desigualdades | Un filtro de currículos que descarta más mujeres | Medir resultados por grupo; no usar IA en decisiones sobre personas sin evaluación |
| Privacidad | Datos personales expuestos, usados sin base legal o enviados a terceros | Pegar datos de conductores en un chatbot externo | Modelos locales, minimización, anonimización |
| Alucinación | El modelo afirma con seguridad algo falso | Inventar una política de reembolsos | RAG con citas, abstención, revisión humana |
| Seguridad | El sistema es manipulable o filtra información | Inyección de instrucciones en un correo | Separar instrucciones y datos, mínimos privilegios |
| Autonomía excesiva | Un agente actúa más allá de lo que debería | Borrar registros de auditoría para liberar disco | Permisos de solo lectura, confirmación humana |
| Propiedad intelectual | Generar contenido que copia obras protegidas o filtrar código propio | Publicar código generado con licencia incompatible | Revisión de licencias, no enviar código a servicios no aprobados |
| Transparencia | La persona no sabe que habla con una IA ni por qué decide algo | Chatbot que se hace pasar por un agente humano | Avisar de que es IA, explicar la base de la respuesta |
| Impacto ambiental y coste | Consumo de energía y de dinero desproporcionado | Usar un modelo enorme para clasificar tres categorías | Elegir el modelo más pequeño que cumple |

### Principios de uso responsable

Casi todos los marcos (OCDE, UNESCO, Comisión Europea) coinciden en seis principios: **supervisión humana, robustez y seguridad, privacidad, transparencia, equidad y rendición de cuentas**. En la práctica de una consultora se traducen en preguntas que debes saber responder antes de desplegar:

1. ¿Quién revisa la salida antes de que tenga efectos?
2. ¿Cómo sé que funciona? ¿Con qué conjunto de pruebas lo he medido?
3. ¿Qué datos entran en el modelo y dónde se procesan?
4. ¿Sabe la persona usuaria que habla con una IA?
5. ¿Puede el sistema tratar peor a algún grupo?
6. ¿Quién responde si se equivoca?

---

## 2.2 Marco normativo

### RGPD

El Reglamento General de Protección de Datos se aplica siempre que un sistema de IA trate datos personales. Las ideas que más afectan a tus proyectos:

- **Base legal y finalidad**: no puedes reutilizar datos para entrenar o alimentar un modelo con una finalidad distinta sin base legal.
- **Minimización**: envía al modelo solo los datos que necesita.
- **Decisiones automatizadas** (artículo 22): las personas tienen derecho a no ser objeto de decisiones basadas únicamente en tratamiento automatizado que les afecten significativamente.
- **Transferencias internacionales**: enviar datos a un servicio fuera del Espacio Económico Europeo requiere garantías. Es una de las razones para usar modelos locales.

### Reglamento Europeo de IA

El Reglamento (UE) 2024/1689 clasifica los sistemas de IA por nivel de riesgo y entra en aplicación de forma escalonada entre 2025 y 2027:

| Nivel | Ejemplos | Consecuencia |
| --- | --- | --- |
| Riesgo inaceptable | Puntuación social, manipulación que explota vulnerabilidades, reconocimiento de emociones en el trabajo | Prohibido |
| Alto riesgo | Selección de personal, evaluación de trabajadores, acceso a servicios esenciales, infraestructuras críticas | Gestión de riesgos, calidad de datos, documentación técnica, registro, supervisión humana y evaluación de conformidad |
| Riesgo limitado | Chatbots, contenido generado (deepfakes) | Obligaciones de transparencia: informar de que es IA y marcar el contenido sintético |
| Riesgo mínimo | Filtros de spam, asistentes internos de redacción | Códigos de conducta voluntarios |

Además, los proveedores de **modelos de IA de uso general** (los LLM fundacionales) tienen obligaciones propias de documentación, transparencia sobre los datos de entrenamiento y respeto de los derechos de autor.

Como consultor no tienes que ser jurista, pero sí saber **clasificar preliminarmente** un caso de uso y saber cuándo hay que implicar a cumplimiento normativo.

### La política de Atlántica

Lee `datos/atlantica/documentos/03_politica_uso_ia.md`. Es un ejemplo realista de cómo una empresa aterriza estas normas: herramientas aprobadas, revisión humana obligatoria, prohibición de decisiones automatizadas sobre personas, inventario de casos de uso y clasificación de riesgo. Tu asistente de equipo tendrá que cumplirla.

---

## 2.3 Panorama de herramientas

### Dos formas de acceder a un modelo

| | Servicio en la nube (API de un proveedor) | Modelo de pesos abiertos en infraestructura propia |
| --- | --- | --- |
| Ejemplos | Servicios comerciales de OpenAI, Anthropic, Google o Mistral | Llama, Qwen, Gemma, Mistral, Granite, gpt-oss ejecutados con Ollama, LM Studio o vLLM |
| Calidad máxima disponible | La más alta | Algo menor, pero suficiente para muchas tareas concretas |
| Privacidad | Los datos salen de la empresa (con contrato y garantías) | Los datos no salen |
| Coste | Por token, variable | Hardware fijo; coste marginal casi nulo |
| Operación | Ninguna | La tuya: servidores, actualizaciones, monitorización |
| Cuándo elegirlo | Prototipos rápidos, tareas que exigen el mejor modelo, datos públicos | Datos confidenciales, volumen alto, requisitos de soberanía |

En este curso trabajas con la segunda opción, que es la que más valor aporta a los clientes que no pueden sacar sus datos.

### Motores de inferencia del curso

| Motor | Papel | Por qué |
| --- | --- | --- |
| **Ollama** | Motor principal | Instalación sencilla, catálogo de modelos, API compatible con OpenAI, herramientas y JSON Schema |
| **LM Studio** | Exploración | Interfaz gráfica para descargar, comparar y ajustar parámetros de modelos; también ofrece servidor local |
| **Colibri** | Laboratorio de frontera | Ejecuta modelos de mezcla de expertos (MoE) de cientos de miles de millones de parámetros leyendo los expertos desde disco; muy lento con los modelos grandes, ideal para entender la inferencia |
| **vLLM** | Producción | Servidor para muchos usuarios a la vez; solo en el servidor compartido (sesión 13) |

### El resto del ecosistema

| Categoría | Herramientas | Sesión |
| --- | --- | --- |
| Asistentes de código | GitHub Copilot, Continue, asistentes integrados en IDE | 13 |
| Frameworks de aplicaciones | LangChain, LangGraph, LlamaIndex | 10 |
| Protocolo de herramientas | Model Context Protocol (MCP) | 10 |
| Bases vectoriales | Chroma, Qdrant, pgvector | 6 |
| Evaluación y observabilidad | Ragas, DeepEval, promptfoo, Langfuse | 7 y 13 |
| Interfaces | Streamlit, Gradio, Open WebUI | 11 |

### Licencias: una pregunta que siempre debes hacer

«Pesos abiertos» no significa «uso libre». Antes de proponer un modelo a un cliente, lee su licencia:

| Licencia | Ejemplos | Uso comercial |
| --- | --- | --- |
| Apache 2.0 o MIT | Granite, Qwen (mayoría), Mistral (algunos), gpt-oss | Sí, sin restricciones relevantes |
| Licencias propias permisivas con condiciones | Llama, Gemma | Sí, con condiciones (atribución, políticas de uso, límites de usuarios) |
| Licencias no comerciales | Algunos modelos de investigación | No |

---

## 2.4 Fundamentos de la IA generativa

### Qué significa «generar»

Un modelo generativo aprende la distribución de probabilidad de los datos con los que se entrena y puede producir muestras nuevas que parecen de esa distribución. No copia ni busca: **muestrea**.

| Familia | Cómo genera | Uso principal |
| --- | --- | --- |
| Modelos autorregresivos (Transformer decodificador) | Predicen el siguiente token, una y otra vez | Texto y código (LLM) |
| Modelos de difusión | Parten de ruido y lo eliminan paso a paso | Imagen, audio y vídeo |
| GAN y autoencoders variacionales | Un generador y un evaluador compiten / un espacio latente que se muestrea | Imagen sintética, datos sintéticos (hoy menos usados) |
| Multimodales | Combinan codificadores de imagen o audio con un LLM | Describir imágenes, entender documentos escaneados |

### Cómo genera texto un LLM

1. El texto de entrada se trocea en **tokens**.
2. El modelo calcula, para cada token posible del vocabulario, la probabilidad de que sea el siguiente.
3. Se **elige** uno (según la temperatura y otros parámetros de muestreo).
4. El token elegido se añade a la entrada y se repite el proceso hasta un token de fin o hasta el límite.

Consecuencias directas que tienes que tener presentes:

- **Es probabilístico**: la misma pregunta puede dar respuestas distintas.
- **No consulta una base de datos**: responde con lo que «suena» más probable según lo aprendido. Por eso alucina.
- **Su coste crece con los tokens**: de entrada y, sobre todo, de salida.

### De un modelo base a un asistente

| Fase | Qué aprende | Datos |
| --- | --- | --- |
| Preentrenamiento | A predecir el siguiente token: gramática, hechos, estilos, código | Billones de tokens de texto público |
| Ajuste con instrucciones | A seguir órdenes y conversar | Decenas o cientos de miles de pares instrucción-respuesta |
| Alineamiento con preferencias | A preferir respuestas útiles, honestas e inofensivas | Comparaciones de respuestas valoradas por personas o por otros modelos |
| Entrenamiento para razonar (opcional) | A «pensar» paso a paso antes de responder | Problemas con solución verificable |

Lo verás con detalle en la sesión 3.

---

## 2.5 Primeras llamadas a un LLM desde Python

### Mensajes y roles

La API de chat recibe una lista de mensajes. Cada mensaje tiene un **rol**:

| Rol | Para qué |
| --- | --- |
| `system` | Instrucciones de comportamiento: quién es el asistente, qué puede y qué no puede hacer, formato |
| `user` | Lo que pide la persona |
| `assistant` | Lo que respondió el modelo antes (para mantener la conversación) |
| `tool` | El resultado de una herramienta (sesiones 7 a 9) |

```python
from comun import llm

mensajes = [
    {"role": "system", "content": "Eres el asistente interno de Atlántica. Respondes en español y en menos de 80 palabras."},
    {"role": "user", "content": "¿Qué es un operador logístico?"},
]
print(llm.chat(mensajes))
```

**El modelo no tiene memoria.** Cada llamada es independiente: para mantener una conversación tienes que reenviar todo el historial. Lo implementarás en el ejercicio 2.

### Parámetros básicos

| Parámetro | Qué controla | Valor típico |
| --- | --- | --- |
| `temperature` | Aleatoriedad del muestreo | 0-0.3 para tareas precisas; 0.7-1 para creatividad |
| `max_tokens` | Longitud máxima de la respuesta | Limítalo siempre en producción |
| `model` | Qué modelo responde | Según la tarea y el hardware |

### El mismo código con otro motor

Abre LM Studio, ve a *Developer* y pulsa *Start Server*. Cambia en `.env`:

```
LLM_BASE_URL=http://localhost:1234/v1
```

Ejecuta el mismo programa: ahora responde LM Studio. Esta independencia del motor es una decisión de arquitectura que conviene tomar en todos los proyectos.

---

## Errores frecuentes

| Error | Síntoma | Solución |
| --- | --- | --- |
| Pensar que el modelo recuerda la conversación | Responde como si no hubieras dicho nada antes | Reenvía el historial completo |
| Poner las instrucciones en el mensaje de usuario | El modelo las sigue a medias | Las reglas de comportamiento van en `system` |
| Comparar modelos con una sola pregunta | Conclusiones que no se sostienen | Usa varias preguntas y repite cada una |
| Olvidar que LM Studio y Ollama usan puertos distintos | Error de conexión | Ollama: 11434 · LM Studio: 1234 |

## Para saber más

- Reglamento (UE) 2024/1689 de Inteligencia Artificial: [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- Agencia Española de Protección de Datos, guías sobre IA: [aepd.es](https://www.aepd.es/)
- Referencia de la API de chat compatible con OpenAI en Ollama: [docs.ollama.com/openai](https://docs.ollama.com/openai)
