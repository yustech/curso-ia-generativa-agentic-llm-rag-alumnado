# Asistente <reto> · Equipo <n>

Plantilla de partida del repositorio de equipo. Sustituid los textos entre `< >`.

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows (en Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env            # y editad CURSO_RAIZ
ollama pull granite4:micro
ollama pull embeddinggemma
```

## Uso

```bash
python -m agente.asistente "¿Cuántos días de vacaciones hay?"   # consola
streamlit run app.py                                            # interfaz
pytest                                                          # pruebas
python -m evals.evaluar                                         # evaluación de extremo a extremo
python -m evals.evaluar --linea-base                            # guarda la línea base (sesión 13)
```

## Punto de partida

La plantilla funciona desde el primer día: un agente ReAct con una herramienta (`buscar_documentacion`), un registro de herramientas con validación Pydantic y confirmación humana para las acciones con efectos, un guardarraíl de entrada, una interfaz Streamlit, 7 pruebas y la evaluación de extremo a extremo.

Resultado de referencia de la plantilla sin tocar (granite4:micro, portátil de 16 GB): exactitud 0,8 en los 5 casos de ejemplo. Falla `G-01` porque **responde bien pero no cita la fuente**: es la primera mejora que tendréis que hacer (sesión 4).

| Carpeta | Qué contiene | Sesión en la que la completáis |
| --- | --- | --- |
| `entorno.py` | Conexión con el repositorio del curso (`CURSO_RAIZ`) | — |
| `agente/` | Prompt de sistema, agente y guardarraíles | 4, 8 |
| `rag/` | Índice y búsqueda | 5, 6, 7 |
| `herramientas/` | Registro con contratos y herramientas del reto | 9 |
| `mcp/` | Servidor MCP (opcional) | 10 |
| `app.py` | Interfaz | 11 |
| `documental/` | Pipeline documental | 12 |
| `evals/` | Conjunto dorado y evaluación | 4, 6, 13 |
| `tests/` | Pruebas deterministas con el LLM falso | 8, 9, 13 |
| `docs/` | Plantillas de los entregables | todas |

## Arquitectura

<Diagrama y explicación breve: interfaz → agente → (RAG | herramientas) → LLM local. Decisiones en `docs/adr/`.>

## Limitaciones conocidas

<Qué no hace, en qué falla y qué supervisión humana necesita.>
