# Sesión 6. Embeddings, búsqueda semántica y bases de datos vectoriales

<!-- cabecera:inicio -->
| Fecha | Horario | Modalidad | Módulos | Hito |
| --- | --- | --- | --- | --- |
| Viernes 11 de diciembre de 2026 | 09:00-15:00 | Remoto | M4 · RAG (Retrieval-Augmented Generation) (6 h) | H2 · Sistema RAG |

**Objetivo:** Interpretar cómo se representan y recuperan documentos mediante embeddings.
<!-- cabecera:fin -->

Al terminar esta sesión entenderás cómo se representa el significado de un texto como un vector, sabrás comparar estrategias de búsqueda (léxica, semántica e híbrida) **con métricas** y tendrás tu primera base de datos vectorial persistente.

<!-- agenda:inicio -->
### Agenda de la sesión

| Hora | Min | Tipo | Bloque |
| --- | --- | --- | --- |
| 09:00 | 15 | Teoría | Activación: el significado como geometría |
| 09:15 | 55 | Teoría | Teoría I: embeddings y similitud |
| 10:10 | 70 | Práctica | Laboratorio: embeddings y ranking |
| 11:20 | 10 | Pausa | Pausa |
| 11:30 | 50 | Teoría | Teoría II: búsqueda léxica, semántica e híbrida; bases vectoriales |
| 12:20 | 70 | Práctica | Reto 1: comparación de estrategias de búsqueda |
| 13:30 | 10 | Pausa | Pausa |
| 13:40 | 56 | Práctica | Reto 2: base vectorial persistente con Chroma |
| 14:36 | 24 | Teoría | Cierre: tabla comparativa y preguntas de repaso |

Teoría: 2 h 24 min · práctica: 3 h 36 min (las pausas computan en el bloque práctico).
<!-- agenda:fin -->

## Lo que entregas hoy

| Entregable | Dónde | Quién |
| --- | --- | --- |
| Notebook o script funcional de búsqueda sobre los documentos del reto | `rag/busqueda.py` (o `.ipynb`) del repositorio del equipo | Equipo |
| Tabla comparativa de estrategias con hit@k y MRR | `docs/comparativa_busqueda.md` | Equipo |
| Ejercicios 1 a 4 con los tests en verde | `sesion_06_embeddings_busqueda/ejercicios/` | Cada persona |

---

## 6.1 Qué es un embedding

Un **embedding** es un vector de números (de unos cientos a unos miles) que representa el significado de un texto. Lo produce un modelo entrenado para que textos con significado parecido tengan vectores cercanos.

```python
from comun import llm

v = llm.embeddings(["¿Cuántos días de vacaciones tengo?", "Política de vacaciones: 25 días laborables"])
print(len(v[0]))   # 768 dimensiones con embeddinggemma
```

Propiedades que tienes que conocer:

| Propiedad | Consecuencia práctica |
| --- | --- |
| Captura significado, no palabras | «Comité de Cambios» y «CAB» pueden quedar cerca aunque no compartan letras |
| Depende del modelo | Los vectores de dos modelos distintos no se pueden comparar ni mezclar en un índice |
| Depende del idioma de entrenamiento | Un modelo entrenado solo en inglés funciona mal en español: elige uno multilingüe |
| Tiene longitud máxima | Textos más largos se truncan: otra razón para trocear |
| Es un cálculo barato frente a generar | Se calcula una vez por trozo y se guarda |

### Modelos de embeddings

| Modelo | Dimensión | Idiomas | Notas |
| --- | --- | --- | --- |
| `embeddinggemma` | 768 | Multilingüe | Pequeño (300M), el del curso |
| `bge-m3` | 1.024 | Multilingüe | Muy bueno en español; más pesado |
| `nomic-embed-text` | 768 | Sobre todo inglés | Popular, rápido |
| `multilingual-e5` | 384-1.024 | Multilingüe | Requiere prefijos «query:» y «passage:» |

Algunos modelos funcionan mejor si distingues la pregunta del documento con un prefijo o una instrucción. Consulta su ficha.

---

## 6.2 Similitud entre vectores

| Medida | Fórmula | Rango | Uso |
| --- | --- | --- | --- |
| Coseno | `a·b / (‖a‖‖b‖)` | -1 a 1 | La más usada: compara la dirección, no la longitud |
| Producto escalar | `a·b` | Sin límite | Igual al coseno si los vectores están normalizados (y más rápido) |
| Distancia euclídea | `‖a − b‖` | 0 a ∞ | Menor es más parecido |

**Normalizar** un vector es dividirlo por su norma para que mida 1. Con vectores normalizados, coseno y producto escalar coinciden y buscar se reduce a una multiplicación de matrices: así lo hace el buscador de referencia del curso (`comun/buscador.py`).

Las puntuaciones absolutas no significan nada por sí solas: 0,54 puede ser un acierto con un modelo y ruido con otro. Lo que importa es el **orden**.

---

## 6.3 Búsqueda léxica: BM25

Antes de los embeddings, los buscadores comparaban **palabras**. BM25 es el algoritmo léxico de referencia (lo usan Elasticsearch y OpenSearch). Puntúa un documento según:

- cuántas veces aparecen en él los términos de la consulta (con saturación: la décima repetición suma menos que la primera);
- lo raro que es cada término en la colección (un término raro como «Multi-AZ» pesa mucho más que «política»);
- la longitud del documento (penaliza los muy largos).

Fortalezas y debilidades frente a la búsqueda semántica:

| | Léxica (BM25) | Semántica (embeddings) |
| --- | --- | --- |
| Códigos, siglas, nombres propios (`ATL-INF-006`, `FARO-142`, `t3.medium`) | Excelente | Regular |
| Sinónimos y paráfrasis («antelación» frente a «con cuánto tiempo») | Mala | Excelente |
| Otro idioma | No funciona | Funciona con modelos multilingües |
| Explicabilidad | Alta: se ve qué palabras coincidieron | Baja |
| Coste | Mínimo | Calcular y guardar vectores |

---

## 6.4 Búsqueda híbrida y fusión de rankings

La búsqueda **híbrida** combina las dos: obtiene un ranking léxico y otro semántico y los fusiona. La forma más robusta de fusionar es **Reciprocal Rank Fusion (RRF)**, que solo usa las posiciones y no las puntuaciones (que no son comparables entre sí):

```
puntuación_RRF(d) = Σ  1 / (k + posición de d en el ranking i)      con k = 60
                    i
```

Un documento que sale tercero en BM25 y primero en semántica obtiene `1/63 + 1/61`. Uno que solo aparece en un ranking suma un único término.

En corpus grandes y variados, con códigos, siglas y nombres propios, la búsqueda híbrida suele ser igual o mejor que cualquiera de las dos por separado, y es la opción por defecto en muchos sistemas de producción. **Pero no siempre gana**: en el corpus pequeño de Atlántica, con un buen modelo multilingüe, la búsqueda semántica sola obtiene mejor MRR que la híbrida (lo comprobarás en el ejercicio 3). La conclusión profesional no es «usa siempre híbrida», sino **«mide con tus datos y decide»**.

### Reordenación (*reranking*)

Un **reordenador** es un modelo que recibe la pregunta y un fragmento **juntos** y puntúa su relevancia. Es más preciso que comparar vectores calculados por separado, pero mucho más lento, así que se aplica solo a los 20-50 primeros candidatos. Se puede usar un modelo de reordenación específico o el propio LLM con un prompt («puntúa de 0 a 10 la relevancia de este fragmento para la pregunta»).

---

## 6.5 Bases de datos vectoriales

Con unos cientos de trozos basta un array de NumPy. Con millones hace falta una base de datos vectorial, que aporta:

| Función | Para qué |
| --- | --- |
| Índice aproximado (ANN, normalmente HNSW) | Buscar entre millones de vectores en milisegundos, a cambio de no garantizar el resultado exacto |
| Persistencia | No recalcular embeddings cada vez |
| Metadatos y filtros | «Solo documentos de RRHH», «solo clasificación Interno», «solo versión vigente» |
| Actualización | Añadir, modificar y borrar trozos sin reconstruir todo |

| Opción | Tipo | Cuándo |
| --- | --- | --- |
| Chroma | Biblioteca embebida o servidor | Prototipos y aplicaciones pequeñas; la del curso |
| Qdrant | Servidor dedicado | Producción, filtros avanzados, gran volumen |
| pgvector | Extensión de PostgreSQL | Si el cliente ya usa PostgreSQL (es el estándar de Atlántica) |
| FAISS | Biblioteca de búsqueda | Máximo rendimiento sin servidor |

```python
import chromadb

cliente = chromadb.PersistentClient(path="indices/chroma")
coleccion = cliente.get_or_create_collection("atlantica", embedding_function=None,
                                             configuration={"hnsw": {"space": "cosine"}})
coleccion.upsert(ids=[...], documents=[...], embeddings=[...], metadatas=[...])
resultado = coleccion.query(query_embeddings=[vector], n_results=4, where={"documento": "06_politica_infraestructura_cloud.md"})
```

Pasamos `embedding_function=None` y los vectores calculados por nosotros para controlar exactamente qué modelo se usa (el mismo en la ingesta y en la consulta).

---

## 6.6 Métricas de recuperación

Para comparar estrategias necesitas preguntas con su fuente correcta (`datos/atlantica/evaluacion/preguntas_rag.jsonl`) y métricas:

| Métrica | Qué mide | Cálculo |
| --- | --- | --- |
| **Hit@k** (tasa de acierto) | ¿Aparece la fuente correcta entre los `k` primeros? | Proporción de preguntas en que sí |
| **MRR** (*Mean Reciprocal Rank*) | ¿En qué posición aparece? | Media de `1 / posición` (0 si no aparece) |
| Precisión@k | ¿Qué proporción de los `k` recuperados es relevante? | Útil cuando hay varias fuentes correctas |
| Recall@k | ¿Qué proporción de las fuentes relevantes se recupera? | Ídem |

Si la fuente correcta está primera en todas las preguntas, MRR = 1. Si está siempre segunda, 0,5. Hit@k y MRR son las dos métricas que usarás en la tabla comparativa de hoy y en el checklist de calidad de la sesión 7.

---

## Errores frecuentes

| Error | Síntoma | Solución |
| --- | --- | --- |
| Mezclar vectores de dos modelos | Resultados absurdos | Un índice, un modelo; si cambias de modelo, reindexa |
| No normalizar al usar producto escalar | Los textos largos ganan siempre | Normaliza o usa coseno |
| Tokenizar BM25 sin quitar tildes ni mayúsculas | «Política» y «politica» no coinciden | Normaliza igual la consulta y los documentos |
| Comparar estrategias con 3 preguntas | Conclusiones aleatorias | Al menos 20-30 preguntas |
| Olvidar `embedding_function=None` en Chroma | Chroma descarga su propio modelo | Pasa tus embeddings |

## Para saber más

- Robertson y Zaragoza (2009), *The Probabilistic Relevance Framework: BM25 and Beyond*.
- Cormack et al. (2009), *Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods*.
- Tabla de clasificación de modelos de embeddings MTEB: [huggingface.co/spaces/mteb/leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- Documentación de Chroma: [docs.trychroma.com](https://docs.trychroma.com/)
