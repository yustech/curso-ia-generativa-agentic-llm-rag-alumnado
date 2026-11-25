# Sesión 1. Introducción a la IA: historia, paradigmas y tipos de modelos

<!-- cabecera:inicio -->
| Fecha | Horario | Modalidad | Módulos | Hito |
| --- | --- | --- | --- | --- |
| Miércoles 2 de diciembre de 2026 | 09:00-15:00 | Presencial | M1 · Introducción a la Inteligencia Artificial (6 h) | H1 · Fundamentos y prompting |

**Objetivo:** Distinguir los principales paradigmas de IA y situarlos en una línea evolutiva.
<!-- cabecera:fin -->

Al terminar esta sesión sabrás situar la IA generativa dentro del mapa completo de la inteligencia artificial, distinguir sus paradigmas y elegir el tipo de modelo adecuado para un problema. Además tendrás tu entorno de trabajo funcionando y formarás parte de uno de los tres equipos del curso.

Ya sabes programar. Esta sesión no repasa matemáticas ni estadística: se centra en el criterio que necesitas en una consultora para no proponer un LLM donde basta una regla, ni una regla donde hace falta un modelo.

<!-- agenda:inicio -->
### Agenda de la sesión

| Hora | Min | Tipo | Bloque |
| --- | --- | --- | --- |
| 09:00 | 15 | Teoría | Activación: un LLM corriendo en este portátil |
| 09:15 | 55 | Teoría | Teoría I: historia y evolución de la IA |
| 10:10 | 70 | Práctica | Laboratorio: preparación del entorno (Python, Ollama, LM Studio) |
| 11:20 | 10 | Pausa | Pausa |
| 11:30 | 50 | Teoría | Teoría II: IA, ML, DL e IA generativa; tipos de modelos |
| 12:20 | 70 | Práctica | Reto 1: formación de equipos y mapa conceptual colaborativo |
| 13:30 | 10 | Pausa | Pausa |
| 13:40 | 56 | Práctica | Reto 2: clasificación de 6 casos de uso |
| 14:36 | 24 | Teoría | Cierre: puesta en común y presentación de los retos del curso |

Teoría: 2 h 24 min · práctica: 3 h 36 min (las pausas computan en el bloque práctico).
<!-- agenda:fin -->

## Lo que entregas hoy

| Entregable | Dónde | Quién |
| --- | --- | --- |
| Entorno verificado: salida de `python comprobar_entorno.py` sin errores | Captura en el repositorio del equipo | Cada persona |
| Mapa conceptual de la IA | `docs/mapa_conceptual.md` del repositorio del equipo | Equipo |
| Ficha de clasificación de 6 casos de uso | `docs/clasificacion_casos.md` | Equipo |
| Ejercicios 1 y 2 con los tests en verde | `sesion_01_introduccion_ia/ejercicios/` | Cada persona |

---

## 1.1 Qué es (y qué no es) la inteligencia artificial

La inteligencia artificial es el campo que construye sistemas capaces de realizar tareas que, hechas por una persona, consideraríamos que requieren inteligencia: reconocer, predecir, decidir, comunicarse o crear.

Dos matices que conviene tener claros desde el principio:

- **IA no es sinónimo de aprendizaje.** Un sistema experto con reglas escritas a mano o un algoritmo de búsqueda de rutas también son IA. Mucho software empresarial que funciona perfectamente es IA «clásica».
- **IA no es sinónimo de IA generativa.** La IA generativa es la rama que más ha crecido desde 2022, pero en una empresa logística como Atlántica la mayor parte del valor sigue viniendo de modelos predictivos y de optimización.

### Tres formas de construir un sistema inteligente

| Enfoque | Cómo se obtiene el comportamiento | Ejemplo en Atlántica | Punto fuerte | Punto débil |
| --- | --- | --- | --- | --- |
| Simbólico (reglas) | Una persona escribe las reglas | «Si la carga supera 1.000 kg, aplica recargo» | Explicable, predecible | No escala a problemas difusos |
| Aprendizaje automático | El sistema aprende patrones de datos etiquetados o no | Predecir la demanda diaria de camiones | Aprende relaciones complejas | Necesita datos y no siempre explica |
| IA generativa | Un modelo preentrenado con enormes cantidades de datos genera contenido nuevo | Redactar la respuesta a una reclamación | Muy flexible, entiende lenguaje natural | Puede inventar, es más cara y menos predecible |

La pregunta profesional no es «¿cómo aplico IA generativa aquí?», sino «¿qué enfoque resuelve este problema con la calidad, el coste y el riesgo que el cliente puede asumir?».

---

## 1.2 Historia y evolución de la IA

La historia de la IA alterna periodos de entusiasmo con «inviernos» en los que la financiación y el interés cayeron. Conocerla ayuda a relativizar las promesas actuales.

| Año | Hito | Por qué importa |
| --- | --- | --- |
| 1950 | Alan Turing publica *Computing Machinery and Intelligence* y propone el juego de la imitación | Primera pregunta formal sobre si una máquina puede pensar |
| 1956 | Conferencia de Dartmouth: nace el término *artificial intelligence* | Inicio del campo como disciplina |
| 1958 | Perceptrón de Rosenblatt | Primera red neuronal que aprende |
| 1966 | ELIZA, el primer chatbot | Ya entonces la gente atribuía comprensión a un programa que solo seguía patrones |
| 1974-1980 | Primer invierno de la IA | Las promesas superaron a la capacidad de cálculo |
| 1980s | Sistemas expertos en empresas | IA simbólica con reglas; caros de mantener |
| 1987-1993 | Segundo invierno | Los sistemas expertos no escalaron |
| 1997 | Deep Blue vence a Kaspárov | Búsqueda y fuerza bruta, no aprendizaje |
| 2012 | AlexNet gana ImageNet con redes profundas y GPU | Comienza la era del deep learning |
| 2016 | AlphaGo vence a Lee Sedol | Aprendizaje por refuerzo y redes profundas |
| 2017 | Artículo *Attention Is All You Need*: la arquitectura Transformer | Base de todos los LLM actuales |
| 2018-2020 | BERT, GPT-2 y GPT-3 | Modelos preentrenados de lenguaje; GPT-3 muestra aprendizaje con pocos ejemplos |
| 2022 | ChatGPT | La IA generativa llega al gran público; ajuste con instrucciones y preferencias humanas |
| 2023 | Modelos de pesos abiertos (Llama, Mistral) y herramientas como Ollama | Se pueden ejecutar LLM en servidores propios y portátiles |
| 2024-2026 | Modelos que razonan, agentes, Model Context Protocol (MCP), modelos abiertos pequeños y eficientes | Los LLM pasan de responder a actuar; la inferencia local se vuelve viable en la empresa |

Tres lecciones de esta historia para tu trabajo:

1. **Los saltos llegan cuando coinciden algoritmo, datos y cálculo.** El Transformer existía en 2017; lo que cambió después fue la escala.
2. **La gente sobreestima lo que entiende un sistema conversacional.** Le pasó a ELIZA en 1966 y nos pasa hoy con los LLM. De ahí la importancia de evaluar.
3. **Las expectativas desmedidas acaban en desencanto.** Un consultor serio promete lo que puede medir.

---

## 1.3 IA, machine learning, deep learning e IA generativa

Los cuatro términos se suelen usar como sinónimos y no lo son. Son conjuntos anidados:

```
Inteligencia artificial
└── Machine learning (aprende de datos)
    └── Deep learning (redes neuronales profundas)
        └── IA generativa (genera contenido nuevo: texto, imagen, audio, código)
            └── Modelos de lenguaje grandes (LLM)
```

### Machine learning

El sistema aprende una función a partir de ejemplos en lugar de que la escribas tú. Hay tres grandes familias:

| Tipo | Qué aprende | Datos que necesita | Ejemplo |
| --- | --- | --- | --- |
| Supervisado | A predecir una etiqueta o un valor | Ejemplos con la respuesta correcta | Predecir si un envío llegará tarde |
| No supervisado | Estructura oculta en los datos | Datos sin etiquetar | Agrupar clientes por patrón de envíos |
| Por refuerzo | Una política de acciones que maximiza una recompensa | Un entorno donde probar acciones | Asignar muelles de carga en tiempo real |

Dentro del supervisado, si la respuesta es una categoría hablamos de **clasificación**; si es un número, de **regresión**.

### Deep learning

Usa redes neuronales con muchas capas que aprenden representaciones de los datos por sí mismas: en una imagen, las primeras capas detectan bordes y las últimas, objetos. Es lo que permitió los grandes avances en visión, voz y lenguaje. Necesita muchos datos y hardware específico (GPU).

### IA generativa

Modelos que aprenden la distribución de los datos y pueden **generar** muestras nuevas plausibles. Un LLM ha aprendido, a partir de billones de palabras, qué texto suele seguir a otro, y con eso genera respuestas, código o resúmenes. La sesión 2 explica cómo.

### Discriminativo frente a generativo

| | Modelo discriminativo | Modelo generativo |
| --- | --- | --- |
| Pregunta que responde | ¿A qué clase pertenece esto? | ¿Cómo sería un ejemplo nuevo de esto? |
| Salida | Una etiqueta o un número | Texto, imagen, audio o código |
| Ejemplo | Clasificador de incidencias | Asistente que redacta la respuesta a la incidencia |
| Evaluación | Exactitud, precisión, recall: fácil de medir | Calidad abierta: hay que diseñar cómo medirla |

Esta última fila es la razón por la que el curso dedica tanto tiempo a evaluar.

---

## 1.4 Tipos de modelos y cómo elegir

| Tipo de modelo | Entrada típica | Salida | Caso en logística |
| --- | --- | --- | --- |
| Regresión | Datos tabulares, series temporales | Número | Demanda diaria de camiones |
| Clasificación | Datos tabulares, texto, imagen | Categoría | Prioridad de una incidencia |
| Agrupamiento (clustering) | Datos tabulares | Grupos | Segmentación de clientes |
| Detección de anomalías | Transacciones, sensores | Normal o anómalo | Fraude en tarjetas de combustible |
| Recomendación | Historial de interacciones | Ranking | Sugerir servicios a un cliente |
| Visión por computador | Imagen o vídeo | Objetos, texto leído | Lectura de matrículas en la barrera |
| Procesamiento del lenguaje | Texto | Etiquetas, entidades | Extraer datos de un albarán |
| Optimización y búsqueda | Restricciones y objetivo | Plan óptimo | Rutas de reparto con ventanas horarias |
| LLM (generativo) | Texto e instrucciones | Texto, código, JSON | Asistente interno, generación de documentación |
| Multimodal | Texto, imagen, audio | Texto o imagen | Describir los daños en la foto de un palé |
| Agente (LLM + herramientas) | Un objetivo | Acciones en sistemas | Preparar una solicitud de cambio de infraestructura |

### Preguntas para elegir

1. **¿La regla se puede escribir?** Si sí, escríbela. Es más barata, explicable y fiable.
2. **¿Hay datos históricos con la respuesta correcta?** Entonces machine learning supervisado.
3. **¿La entrada o la salida es lenguaje natural abierto?** Ahí brilla un LLM.
4. **¿Hay que actuar sobre sistemas?** Agente, con permisos limitados y supervisión humana.
5. **¿Qué pasa si se equivoca?** Cuanto mayor sea el daño, más controles, más evaluación y más intervención humana.

Un error habitual en proyectos reales es usar un LLM para calcular una ruta óptima o un precio. Un LLM no optimiza ni calcula de forma fiable; puede, en cambio, **llamar** a un optimizador o a una función de cálculo. Lo verás en las sesiones de agentes.

---

## 1.5 Tu entorno de trabajo

Todo el curso funciona con modelos ejecutados **en tu portátil** o en el **servidor compartido** del curso. Ningún dato sale a servicios externos.

### Piezas del entorno

| Pieza | Para qué | Instalación |
| --- | --- | --- |
| Python 3.12 | Lenguaje de los laboratorios | [python.org](https://www.python.org/downloads/) |
| Visual Studio Code | Editor | [code.visualstudio.com](https://code.visualstudio.com/) con la extensión Python |
| Git | Control de versiones | [git-scm.com](https://git-scm.com/) |
| Ollama | Motor de inferencia principal: descarga y sirve modelos | [ollama.com](https://ollama.com/download) |
| LM Studio | Interfaz gráfica para explorar modelos y parámetros | [lmstudio.ai](https://lmstudio.ai/) |

### Puesta en marcha paso a paso

1. Instala Ollama y comprueba que responde:

```bash
ollama --version
ollama pull granite4:micro
ollama pull embeddinggemma
ollama run granite4:micro "Hola, ¿quién eres?"
```

2. Clona el repositorio del curso, crea el entorno virtual e instala las dependencias:

```bash
git clone https://github.com/yustech/curso-ia-generativa-agentic-llm-rag-alumnado.git
cd curso-ia-generativa-agentic-llm-rag-alumnado
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows (PowerShell)
source .venv/bin/activate         # macOS o Linux
pip install -r requirements.txt
```

3. Crea tu fichero de configuración a partir del ejemplo:

```bash
copy .env.example .env            # Windows
cp .env.example .env              # macOS o Linux
```

4. Comprueba el entorno:

```bash
python comprobar_entorno.py
```

Todas las líneas deben terminar en `OK` (un `AVISO` no bloquea).

### Por qué estos modelos

Los portátiles del curso tienen 16 GB de RAM. Un modelo de 3-4 mil millones de parámetros cuantizado ocupa entre 2 y 3,5 GB y responde con fluidez. `granite4:micro` admite herramientas y salidas en JSON, y tiene licencia Apache 2.0, que permite uso comercial. Para experimentos con modelos mayores usarás el servidor compartido. En la sesión 3 aprenderás a calcular cuánta memoria necesita un modelo.

### El cliente común del curso

Todos los laboratorios usan `comun/llm.py`, que habla con cualquier servidor compatible con la API de OpenAI. La URL está en `.env`. Cambiar de Ollama a LM Studio o al servidor compartido es cambiar una línea; el código no cambia.

```python
from comun import llm

print(llm.chat("Explica en una frase qué es Atlántica Logística."))
print(llm.ultima_llamada)   # modelo, segundos y tokens
```

---

## 1.6 El proyecto del curso

Durante las 14 sesiones vas a construir, en equipo, un **asistente basado en LLM con RAG y herramientas** para un caso real de Atlántica Logística. Cada sesión añade una pieza y termina con un entregable.

| Equipo | Reto | Qué hace el asistente |
| --- | --- | --- |
| Equipo 1 | R1 · DevAssist | Responde dudas sobre la guía de estilo y la arquitectura, genera pruebas y revisa código |
| Equipo 2 | R2 · InfraPilot | Traduce peticiones de entornos a Terraform conforme a la política y prepara el cambio para aprobación |
| Equipo 3 | R3 · PMO Copilot | Convierte actas en historias de usuario, mantiene el backlog y redacta el informe de estado |

Roles dentro del equipo (rotan cada hito): responsable de producto y calidad, ingeniería de IA, ingeniería de conocimiento (RAG) e ingeniería de integración (herramientas).

La evaluación del curso es: laboratorios y entregables de sesión (40 %), proyecto final (40 %) y evaluación individual (20 %). El detalle está en el `README.md` de la raíz.

---

## Errores frecuentes

| Error | Síntoma | Solución |
| --- | --- | --- |
| Ollama no está arrancado | `comprobar_entorno.py` no conecta con `localhost:11434` | Abre la aplicación Ollama o ejecuta `ollama serve` |
| No se activó el entorno virtual | `ModuleNotFoundError: No module named 'openai'` | Activa `.venv` y vuelve a ejecutar |
| PowerShell no deja activar el entorno | Error de directiva de ejecución | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Falta el modelo | `model "granite4:micro" not found` | `ollama pull granite4:micro` |
| El portátil va muy lento | Respuestas de más de 30 s | Cierra aplicaciones; no tengas modelos cargados a la vez en Ollama y LM Studio |

## Para saber más

- Russell y Norvig, *Artificial Intelligence: A Modern Approach*, 4.ª ed. Capítulo 1: historia y fundamentos.
- Documentación de Ollama: [docs.ollama.com](https://docs.ollama.com/)
- Vaswani et al. (2017), *Attention Is All You Need*: [arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)
