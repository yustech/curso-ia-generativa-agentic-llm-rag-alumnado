# Sesión 10. Laboratorio guiado

Completa cada fichero sustituyendo los `raise NotImplementedError` por tu código. Comprueba tu trabajo con:

```bash
pytest sesion_10_multiagente_frameworks -v
```

> Las versiones de las bibliotecas están fijadas en `requirements.txt`. El SDK de MCP 2.x llama `MCPServer` a lo que en la versión 1 se llamaba `FastMCP`, y sus objetos usan nombres de atributos de estilo Python (`input_schema`, `is_error`). Si encuentras ejemplos en internet con la sintaxis antigua, adáptalos.

## Ejercicio 1. Tu propio servidor MCP (laboratorio, 35 min)

Fichero: `s10_ej1_servidor_mcp.py`

1. `listar_documentos()`.
2. `leer_documento(nombre)`: con la restricción de rutas. Es el control de seguridad más importante del servidor.
3. `buscar_documentacion(consulta, k)`: usa la de `comun.herramientas` y limita `k` entre 1 y 8.
4. `indice()`: el recurso `atlantica://indice`.

El registro en el servidor ya está hecho al final del fichero. Los docstrings son lo que verá el modelo: léelos con esa mirada.

## Ejercicio 2. Cliente MCP y agente (laboratorio, 35 min)

Fichero: `s10_ej2_cliente_mcp.py`

1. `mcp_a_openai(herramienta)`: convierte la definición MCP al formato de herramienta de la API de OpenAI.
2. `texto_resultado(resultado)`.
3. `agente_mcp(objetivo, ruta, max_pasos, sistema)`: el bucle de agente de siempre, pero las herramientas se ejecutan en el servidor con `await sesion.call_tool(...)`. Es una función asíncrona porque el cliente MCP lo es.

Ejecuta el fichero. El agente lanza tu servidor como proceso, descubre sus herramientas y las usa.

## Ejercicio 3. Flujo multiagente con LangGraph (Reto 1, 50 min)

Fichero: `s10_ej3_multiagente.py`

1. `nodo_investigador`, `nodo_redactor` y `nodo_revisor`: cada nodo recibe el estado y devuelve **solo las claves que cambia**.
2. `siguiente(estado)`: la arista condicional, con el máximo de revisiones.
3. `construir_grafo(buscar)`.

Antes, ejecuta `ejemplos/01_langchain_basico.py` para ver LangChain contra Ollama. Después ejecuta el fichero con el modelo real y responde: ¿cuántas vueltas da el revisor? ¿Mejora el borrador tras la corrección?

## Ejercicio 4. Matriz de decisión (Reto 2, 20 min)

Fichero: `s10_ej4_matriz_decision.py`

1. `normalizar_pesos`, `puntuar`, `ranking` y `tabla`.

Ejecuta `ejemplos/02_llamaindex_rag.py` y compara con tu RAG de la sesión 5: mismas respuestas en muchas menos líneas, pero ¿sabes qué troceado y qué prompt ha usado?

## Práctica de equipo

El enunciado está en [`PRACTICA_10.md`](PRACTICA_10.md).
