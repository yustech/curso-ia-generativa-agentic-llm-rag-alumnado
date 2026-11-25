# Sesión 10. Workflows multiagente y frameworks: LangChain, LlamaIndex y MCP

<!-- cabecera:inicio -->
| Fecha | Horario | Modalidad | Módulos | Hito |
| --- | --- | --- | --- | --- |
| Jueves 17 de diciembre de 2026 | 09:00-15:00 | Remoto | M5 · Agentic AI y herramientas avanzadas (6 h) | H3 · Sistema agéntico |

**Objetivo:** Comparar enfoques de orquestación y seleccionar el adecuado según requisitos.
<!-- cabecera:fin -->

Hasta ahora has construido todo a mano, y por eso sabes qué hace cada pieza. Hoy conocerás los frameworks que usarás en los proyectos (LangChain y LangGraph, LlamaIndex) y el protocolo que se ha convertido en el estándar para conectar herramientas a los agentes (MCP). Sobre todo, aprenderás a **elegir** con criterio, que es lo que un cliente espera de ti. Cierra el Hito 3.

<!-- agenda:inicio -->
### Agenda de la sesión

| Hora | Min | Tipo | Bloque |
| --- | --- | --- | --- |
| 09:00 | 15 | Teoría | Activación: ¿un agente o varios? |
| 09:15 | 55 | Teoría | Teoría I: patrones multiagente y Model Context Protocol |
| 10:10 | 70 | Práctica | Laboratorio: tu propio servidor MCP |
| 11:20 | 10 | Pausa | Pausa |
| 11:30 | 50 | Teoría | Teoría II: LangChain, LangGraph y LlamaIndex |
| 12:20 | 70 | Práctica | Reto 1: flujo multiagente con LangGraph |
| 13:30 | 10 | Pausa | Pausa |
| 13:40 | 56 | Práctica | Reto 2: comparativa y matriz de decisión tecnológica |
| 14:36 | 24 | Teoría | Cierre: Hito 3 |

Teoría: 2 h 24 min · práctica: 3 h 36 min (las pausas computan en el bloque práctico).
<!-- agenda:fin -->

## Lo que entregas hoy

| Entregable | Dónde | Quién |
| --- | --- | --- |
| Workflow multiagente del reto | `agente/flujo.py` del repositorio del equipo | Equipo |
| Matriz de decisión tecnológica | `docs/matriz_decision.md` | Equipo |
| Servidor MCP con las herramientas del reto | `mcp/servidor.py` | Equipo |
| Ejercicios 1 a 4 con los tests en verde | `sesion_10_multiagente_frameworks/ejercicios/` | Cada persona |

---

## 10.1 ¿Un agente o varios?

Un sistema **multiagente** reparte el trabajo entre varios agentes especializados, cada uno con su propio prompt, sus herramientas y su responsabilidad.

| Ventajas | Costes |
| --- | --- |
| Prompts más cortos y enfocados: cada agente hace una cosa | Más llamadas al modelo: más latencia y coste |
| Herramientas y permisos separados por rol | Más difícil de depurar: hay que seguir la conversación entre agentes |
| Se puede usar un modelo distinto en cada rol | Los errores se propagan de un agente a otro |
| Encaja con procesos que ya tienen roles (redactar, revisar, aprobar) | Riesgo de sobreingeniería |

La pregunta de diseño es la misma que en la sesión 7: **¿lo resuelve un sistema más simple?** Varios agentes se justifican cuando las tareas son realmente distintas (investigar frente a redactar), necesitan permisos distintos o se benefician de una revisión independiente.

## 10.2 Patrones multiagente

| Patrón | Funcionamiento | Ejemplo en los retos |
| --- | --- | --- |
| Secuencial (cadena) | A → B → C, cada uno con su rol | Investigador → redactor → revisor |
| Supervisor | Un agente reparte el trabajo y combina los resultados | Un coordinador que pide a «estilo», «seguridad» y «pruebas» que revisen una MR |
| Evaluador-optimizador | Uno genera y otro critica hasta aprobar (con máximo de vueltas) | Historia de usuario revisada contra la definición de preparado |
| Paralelo y votación | Varios resuelven lo mismo y se compara | Tres clasificaciones de una incidencia y se queda la mayoritaria |
| Traspaso (*handoff*) | Un agente pasa la conversación a otro más adecuado | El asistente general pasa una petición de entorno a InfraPilot |

Hoy implementarás el patrón secuencial con evaluador-optimizador: investigador, redactor y revisor, con un bucle de correcciones limitado.

---

## 10.3 Model Context Protocol (MCP)

**MCP** es un protocolo abierto para conectar aplicaciones de IA con herramientas y datos. Resuelve un problema de integración: sin un estándar, cada asistente necesita un conector propio para cada sistema (N × M integraciones); con MCP, cada sistema publica un servidor y cada asistente es un cliente (N + M).

```
 Aplicación (host)                        Servidores MCP
┌──────────────────────┐        ┌─────────────────────────────┐
│ Agente / IDE / chat  │        │ atlantica-documentacion     │ → documentos
│   └── Cliente MCP ───┼─stdio──┤   herramientas · recursos   │
│   └── Cliente MCP ───┼─HTTP───┤ backlog-faro                │ → API del backlog
└──────────────────────┘        └─────────────────────────────┘
```

| Primitiva | Qué es | Ejemplo |
| --- | --- | --- |
| Herramientas (*tools*) | Funciones que el modelo puede invocar | `buscar_documentacion`, `leer_documento` |
| Recursos (*resources*) | Datos que la aplicación puede leer y poner en contexto | `atlantica://indice` |
| Prompts | Plantillas reutilizables que ofrece el servidor | «Revisa esta MR según la guía» |

| Transporte | Cuándo |
| --- | --- |
| stdio | El cliente lanza el servidor como proceso local. Lo que usarás hoy |
| HTTP (*streamable HTTP*) | Servidor remoto compartido, con autenticación |

Con el SDK oficial de Python, un servidor son unas líneas:

```python
from mcp.server import MCPServer

servidor = MCPServer("atlantica-documentacion")

@servidor.tool()
def leer_documento(nombre: str) -> str:
    """Devuelve el texto completo de un documento interno."""
    ...

servidor.run()   # stdio
```

El SDK genera el esquema de la herramienta a partir de la firma y el docstring, igual que tu `Registro` de la sesión 9.

### Seguridad en MCP

Un servidor MCP es código que se ejecuta con tus permisos y unas descripciones de herramientas que el modelo lee como instrucciones. Por eso:

- Instala solo servidores de confianza y revisa qué herramientas exponen.
- Aplica en el servidor los mismos controles de la sesión 9: validación, mínimo privilegio y rutas restringidas (`leer_documento` no puede salir de su carpeta).
- Las acciones con efectos siguen necesitando confirmación humana en el cliente.
- Desconfía de las descripciones de herramientas de terceros: pueden contener instrucciones maliciosas (*tool poisoning*).

---

## 10.4 LangChain y LangGraph

**LangChain** es la biblioteca más extendida para construir aplicaciones con LLM. Aporta abstracciones comunes para modelos de muchos proveedores, mensajes, plantillas, herramientas, salidas estructuradas y cientos de integraciones.

```python
from langchain_openai import ChatOpenAI

modelo = ChatOpenAI(model="granite4:micro", base_url="http://localhost:11434/v1", api_key="ollama")
modelo_con_herramientas = modelo.bind_tools([coste_instancia])
```

**LangGraph**, del mismo ecosistema, modela una aplicación como un **grafo de estado**: nodos (funciones que reciben y actualizan el estado), aristas (incluidas las condicionales) y un estado tipado que fluye entre ellos. Es la formalización de la máquina de estados de la sesión 8.

```python
from langgraph.graph import StateGraph, START, END

grafo = StateGraph(Estado)
grafo.add_node("redactor", nodo_redactor)
grafo.add_node("revisor", nodo_revisor)
grafo.add_edge(START, "redactor")
grafo.add_edge("redactor", "revisor")
grafo.add_conditional_edges("revisor", siguiente, ["redactor", END])
app = grafo.compile()
app.invoke({"pregunta": "..."})
```

Lo que aporta LangGraph frente a tu bucle: flujos con ramas y ciclos explícitos, puntos de control (*checkpoints*) para pausar y reanudar (por ejemplo, esperando una aprobación humana), ejecución en streaming y visualización del grafo.

## 10.5 LlamaIndex

**LlamaIndex** nació para el RAG y es especialmente fuerte en todo lo que rodea a los datos: lectores de decenas de formatos, troceadores, índices, recuperadores, reordenadores y motores de consulta.

```python
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

documentos = SimpleDirectoryReader("datos/atlantica/documentos").load_data()
indice = VectorStoreIndex.from_documents(documentos)
respuesta = indice.as_query_engine(similarity_top_k=3).query("¿Cuáles son las ventanas de cambio?")
```

Es tu RAG de la sesión 5 en cinco líneas. La contrapartida es que cada línea esconde decisiones (troceado, prompt, número de trozos) que tienes que conocer y ajustar: ahora sabes cuáles son.

## 10.6 Elegir: matriz de decisión

| | Sin framework | LangChain / LangGraph | LlamaIndex |
| --- | --- | --- | --- |
| Punto fuerte | Control total, cero dependencias | Agentes y flujos con estado; integraciones | RAG y conectores de datos |
| Punto débil | Hay que escribirlo y mantenerlo todo | Capas de abstracción; cambios entre versiones | Menos flexible fuera del RAG |
| Cuándo | Lógica sencilla, requisitos estrictos de auditoría, equipo con criterio | Flujos con varios pasos, ramas, aprobaciones humanas | Muchas fuentes y formatos, RAG avanzado |

Criterios para una matriz de decisión ponderada: simplicidad, control, facilidad de depuración, soporte de RAG, soporte multiagente, ecosistema y estabilidad de la API. Los pesos dependen del proyecto: un cliente regulado pondrá más peso en control y depuración; una prueba de concepto rápida, en ecosistema.

No es una elección excluyente: es habitual usar LlamaIndex para la ingesta, LangGraph para el flujo y MCP para exponer las herramientas. **La independencia del motor de inferencia** (API compatible con OpenAI) se mantiene con los tres.

---

## Errores frecuentes

| Error | Síntoma | Solución |
| --- | --- | --- |
| Varios agentes para un problema simple | Lento, caro y difícil de depurar | Un agente o un workflow |
| Bucle de revisión sin máximo | El redactor y el revisor no terminan nunca | Máximo de iteraciones |
| Adoptar un framework sin entender lo que hace | Comportamientos inexplicables | Revisa troceado, prompts y parámetros por defecto |
| Servidor MCP que permite leer cualquier ruta | Fuga de ficheros | Restringir rutas y validar argumentos |
| Mezclar versiones mayores de un SDK | Errores de importación | Fija versiones en `requirements.txt` |

## Para saber más

- Especificación y documentación de MCP: [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- SDK de Python de MCP: [github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)
- Documentación de LangGraph: [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph/)
- Documentación de LlamaIndex: [docs.llamaindex.ai](https://docs.llamaindex.ai/)
