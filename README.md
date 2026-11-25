# Inteligencia Artificial Generativa, Agentic AI, LLM y RAG

Curso práctico de **84 horas** para ingenieras e ingenieros recién incorporados a la consultora. Aprenderás a trabajar con modelos de lenguaje **en local** (Ollama y LM Studio en tu portátil de 16 GB), a construir sistemas **RAG** que responden con las fuentes del cliente y a diseñar **agentes** que usan herramientas con control, trazas y supervisión humana. Todo se mide: cada decisión se apoya en un conjunto de pruebas.

Durante el curso trabajarás en uno de tres equipos sobre un cliente ficticio, **Atlántica Logística**, y construirás un asistente real que defenderás el último día.

> **Apuntes en HTML:** abre [`docs/index.html`](docs/index.html) en el navegador. Cada sesión tiene apuntes, ejercicios, práctica de equipo y presentación.

<!-- resumen:inicio -->
|  |  |
| --- | --- |
| Duración | 84 horas en 14 sesiones de 6 horas |
| Fechas | Del 2 al 23 de diciembre de 2026 |
| Modalidad | Presencial: Mié 02/12, Lun 14/12, Mié 23/12. Resto en remoto (por confirmar: Jue 03/12) |
| Participantes | 12 personas en 3 equipos de 4 |
| Metodología | 60 % práctica y 40 % teoría: cada sesión de 6 horas combina 2 h 24 min de teoría aplicada y 3 h 36 min de práctica (las pausas computan dentro del bloque práctico). |
| Cliente del curso | Atlántica Logística S.A. (ficticio) |
<!-- resumen:fin -->

## Calendario

<!-- calendario:inicio -->
| Sesión | Fecha | Horario | Modalidad | Módulos | Contenido |
| --- | --- | --- | --- | --- | --- |
| 1 | Mié 02/12 | 09:00-15:00 | Presencial | M1 (6 h) | [Introducción a la IA: historia, paradigmas y tipos de modelos](sesion_01_introduccion_ia/README.md) |
| 2 | Jue 03/12 | 08:00-14:00 | Por confirmar | M1 (2 h) + M2 (4 h) | [IA responsable, panorama de herramientas y fundamentos de la IA generativa](sesion_02_ia_responsable_genai/README.md) |
| 3 | Vie 04/12 | 09:00-15:00 | Remoto | M2 (6 h) | [Qué es un LLM: tokens, contexto y modelos fundacionales](sesion_03_llm_tokens_contexto/README.md) |
| 4 | Mié 09/12 | 09:00-15:00 | Remoto | M2 (2 h) + M3 (4 h) | [Limitaciones y alucinaciones · Prompt engineering](sesion_04_alucinaciones_prompting/README.md) |
| 5 | Jue 10/12 | 09:00-15:00 | Remoto | M4 (6 h) | [RAG: concepto, arquitectura y criterios de adopción](sesion_05_rag_arquitectura/README.md) |
| 6 | Vie 11/12 | 09:00-15:00 | Remoto | M4 (6 h) | [Embeddings, búsqueda semántica y bases de datos vectoriales](sesion_06_embeddings_busqueda/README.md) |
| 7 | Lun 14/12 | 09:00-15:00 | Presencial | M4 (2 h) + M5 (4 h) | [Indexación y evaluación RAG · Introducción a los agentes](sesion_07_indexacion_agentes/README.md) |
| 8 | Mar 15/12 | 09:00-15:00 | Remoto | M5 (6 h) | [Agentes: planificación, memoria, estado y guardarraíles](sesion_08_planificacion_memoria/README.md) |
| 9 | Mié 16/12 | 09:00-15:00 | Remoto | M5 (6 h) | [Herramientas y APIs: tool calling seguro y verificable](sesion_09_herramientas_apis/README.md) |
| 10 | Jue 17/12 | 09:00-15:00 | Remoto | M5 (6 h) | [Workflows multiagente y frameworks: LangChain, LlamaIndex y MCP](sesion_10_multiagente_frameworks/README.md) |
| 11 | Vie 18/12 | 09:00-15:00 | Remoto | M5 (2 h) + M6 (4 h) | [Automatización con agentes · Asistentes inteligentes y chatbots](sesion_11_automatizacion_asistentes/README.md) |
| 12 | Lun 21/12 | 09:00-15:00 | Remoto | M6 (6 h) | [Generación de documentación, análisis documental y automatización de procesos](sesion_12_documentacion/README.md) |
| 13 | Mar 22/12 | 09:00-15:00 | Remoto | M6 (4 h) + M7 (2 h) | [Casos de negocio y desarrollo de software · Definición del proyecto final](sesion_13_casos_produccion/README.md) |
| 14 | Mié 23/12 | 09:00-15:00 | Presencial | M7 (6 h) | [Proyecto final: demo, defensa y evaluación](sesion_14_proyecto_final/README.md) |
<!-- calendario:fin -->

## Módulos

<!-- modulos:inicio -->
| Módulo | Nombre | Horas | Sesiones | Temas |
| --- | --- | --- | --- | --- |
| M1 | Introducción a la Inteligencia Artificial | 8 h | 1, 2 | Historia y evolución de la IA; Conceptos de IA, Machine Learning, Deep Learning e IA Generativa; Tipos de modelos de IA; Ética, privacidad, sesgos y uso responsable; Panorama actual de herramientas y casos de uso |
| M2 | Introducción a GenAI y LLM | 12 h | 2, 3, 4 | Fundamentos de IA Generativa; ¿Qué es un LLM?; Tokens, contexto y ventanas de contexto; Funcionamiento de los modelos fundacionales; Limitaciones y alucinaciones |
| M3 | Prompt Engineering | 4 h | 4 | Principios del diseño de prompts; Zero-shot, One-shot y Few-shot; Chain of Thought; Prompts estructurados; Optimización y evaluación de respuestas |
| M4 | RAG (Retrieval-Augmented Generation) | 14 h | 5, 6, 7 | Concepto y arquitectura RAG; Embeddings y búsqueda semántica; Bases de datos vectoriales; Indexación de documentos; Integración de conocimiento empresarial; Laboratorios prácticos |
| M5 | Agentic AI y herramientas avanzadas | 24 h | 7, 8, 9, 10, 11 | Arquitectura de agentes; Planificación y memoria; Uso de herramientas y APIs; Workflows multiagente; Introducción a LangChain, LlamaIndex y MCP; Automatización de tareas con agentes |
| M6 | Aplicaciones prácticas de IA Generativa | 14 h | 11, 12, 13 | Asistentes inteligentes; Chatbots; Generación de documentación; Análisis documental; Automatización de procesos; Casos de uso en negocio y desarrollo software; Laboratorios guiados |
| M7 | Proyecto final y evaluación | 8 h | 13, 14 | Diseño e implementación de un asistente basado en LLM con RAG; Presentación del proyecto; Evaluación práctica y teórica |
<!-- modulos:fin -->

## Antes del primer día

Necesitas unos 40 GB libres y permisos para instalar programas. Si algo falla, ejecuta el paso 7 y envía la salida al docente **antes del 2 de diciembre**.

1. **Python 3.12** desde [python.org](https://www.python.org/downloads/) (en Windows, marca «Add python.exe to PATH»).
2. **Git** desde [git-scm.com](https://git-scm.com/) y **Visual Studio Code** con la extensión Python.
3. **Ollama** desde [ollama.com](https://ollama.com/download). Descarga los dos modelos del curso (unos 2,7 GB):

   ```bash
   ollama pull granite4:micro
   ollama pull embeddinggemma
   ```

4. **LM Studio** desde [lmstudio.ai](https://lmstudio.ai/) (lo usaremos en la sesión 2 para comparar motores).
5. Clona el repositorio y crea el entorno virtual:

   ```bash
   git clone https://github.com/yustech/curso-ia-generativa-agentic-llm-rag-alumnado.git
   cd curso-ia-generativa-agentic-llm-rag-alumnado
   python -m venv .venv
   ```

   | Sistema | Activar el entorno |
   | --- | --- |
   | Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
   | macOS o Linux | `source .venv/bin/activate` |

6. Instala las dependencias y crea tu configuración:

   ```bash
   pip install -r requirements.txt
   copy .env.example .env        # macOS o Linux: cp .env.example .env
   ```

7. Comprueba que todo funciona:

   ```bash
   python comprobar_entorno.py
   ```

   Todas las líneas deben terminar en `OK` (un `AVISO` no impide empezar).

## Estructura del repositorio

```
curso-ia-generativa-agentic-llm-rag-alumnado/
├── README.md                  Este fichero
├── docs/                      Apuntes en HTML y presentaciones (abre docs/index.html)
├── sesion_01_.../             Una carpeta por sesión
│   ├── README.md              Apuntes de la sesión
│   ├── ejemplos/              Código que se explica en clase, listo para ejecutar
│   ├── ejercicios/            Enunciados (README.md), ficheros a completar y práctica de equipo (PRACTICA_XX.md)
│   └── tests/                 Pruebas que comprueban tus ejercicios
├── comun/                     Biblioteca del curso: cliente LLM, buscador, agente de referencia, LLM falso para pruebas
├── datos/atlantica/           Documentación, código, backlog y conjuntos de evaluación del cliente ficticio
├── equipos/                   Retos, herramientas del cliente por equipo y plantilla del proyecto
├── plantillas/                Plantillas de los entregables de equipo
├── proyecto_final/            Enunciado, requisitos y rúbrica del proyecto final
├── .env.example               Configuración del motor de inferencia y los modelos
└── comprobar_entorno.py       Diagnóstico del entorno
```

## Cómo se trabaja en cada sesión

1. **Teoría aplicada** con los apuntes (`README.md` de la sesión) y los ejemplos de `ejemplos/`, que se ejecutan en directo.
2. **Laboratorio guiado** individual: completa los ficheros de `ejercicios/` sustituyendo cada `raise NotImplementedError` por tu código y comprueba con las pruebas:

   ```bash
   pytest sesion_01_introduccion_ia -v
   ```

   Las pruebas usan un **LLM falso** y determinista: comprueban tu lógica sin depender del modelo. Para lanzar además las pruebas con el modelo real: `CURSO_LLM_REAL=1 pytest ...` (en PowerShell: `$env:CURSO_LLM_REAL=1; pytest ...`).
3. **Práctica de equipo** (`ejercicios/PRACTICA_XX.md`) en el repositorio de tu equipo, con su entrega y sus criterios de evaluación.
4. **Cierre**: puesta en común y preguntas de repaso.

## Equipos y retos

<!-- equipos:inicio -->
| Equipo | Reto | Qué construye | Fuentes del RAG | Herramientas |
| --- | --- | --- | --- | --- |
| Equipo 1 | **R1 · DevAssist** | Asistente que responde dudas sobre la guía de estilo y la arquitectura del código de Atlántica, genera pruebas unitarias y revisa cambios antes de una merge request. | Guía de estilo Python, arquitectura de referencia y código del módulo de tarifas. | Leer ficheros del repositorio, ejecutar pytest en un entorno aislado, comprobar el estilo. |
| Equipo 2 | **R2 · InfraPilot** | Asistente que traduce peticiones de entornos en lenguaje natural a Terraform conforme a las políticas de Atlántica, valida el resultado y prepara el plan para su aprobación humana. | Política de infraestructura cloud, catálogo de módulos aprobados y procedimiento de cambios. | Consultar el catálogo de módulos, validar políticas, estimar coste, registrar la solicitud de cambio. |
| Equipo 3 | **R3 · PMO Copilot** | Asistente que convierte actas y correos en historias de usuario, mantiene el backlog, genera el informe de estado semanal y detecta riesgos. | Metodología de proyectos, actas de reunión e informes previos. | Leer y actualizar el backlog (API simulada), calcular métricas del sprint, generar el informe de estado. |
<!-- equipos:fin -->

Detalle de los retos, roles y cómo crear el repositorio del equipo en [`equipos/README.md`](equipos/README.md). Proyecto final y rúbrica en [`proyecto_final/README.md`](proyecto_final/README.md).

## Evaluación

<!-- evaluacion:inicio -->
| Componente | Peso | Evidencias |
| --- | --- | --- |
| Laboratorios y entregables de sesión | 40 % | Evidencias técnicas, documentación y reflexión breve de cada una de las 14 sesiones |
| Proyecto final integrador | 40 % | MVP, arquitectura, pruebas, trazabilidad y presentación |
| Evaluación individual | 20 % | Prueba teórico-práctica y defensa de decisiones |

**Hitos del proyecto**

| Hito | Sesiones | Entregables | Resultado |
| --- | --- | --- | --- |
| H1 · Fundamentos y prompting | 1-4 | Mapa conceptual, matriz de riesgos, cuaderno de experimentos y biblioteca de prompts evaluados. | Se domina el lenguaje base y se controla la calidad de la interacción con un LLM. |
| H2 · Sistema RAG | 5-7 | Arquitectura, notebook de embeddings, índice consultable y checklist de evaluación. | Se recupera conocimiento y se mide la relevancia de las respuestas. |
| H3 · Sistema agéntico | 8-10 | Especificación de agente, tool calling, trazas, workflow multiagente y selección de framework. | El sistema planifica, usa herramientas y tiene controles. |
| H4 · Aplicación y proyecto | 11-14 | Prototipo, pipeline documental, canvas, MVP, documentación, presentación y evaluación. | Se entrega y defiende una solución integrada con valor de negocio. |
<!-- evaluacion:fin -->

## Modelos y motores de inferencia

| Pieza | Por defecto | Alternativas | Dónde se ve |
| --- | --- | --- | --- |
| Motor en tu portátil | Ollama | LM Studio | Sesiones 1 y 2 |
| Modelo de chat | `granite4:micro` (rápido, herramientas y JSON) | `qwen3:4b` (razona, más lento), `gemma3:4b` (buen español, sin herramientas) | Sesiones 2 y 3 |
| Modelo de embeddings | `embeddinggemma` | `bge-m3` (servidor) | Sesión 6 |
| Servidor compartido | Ollama con modelos de 8 B o más | vLLM (sesión 13), Colibri (demostración, sesiones 2 y 3) | Todo el curso |

Todo el código usa la API compatible con OpenAI: cambiar de motor es cambiar `LLM_BASE_URL` en el `.env`.

## Datos

Atlántica Logística y todos sus documentos, personas, proyectos y cifras son **ficticios**. No introduzcas datos reales de clientes ni datos personales en los ejercicios.
