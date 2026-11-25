# Sesión 3. Qué es un LLM: tokens, contexto y modelos fundacionales

<!-- cabecera:inicio -->
| Fecha | Horario | Modalidad | Módulos | Hito |
| --- | --- | --- | --- | --- |
| Viernes 4 de diciembre de 2026 | 09:00-15:00 | Remoto | M2 · Introducción a GenAI y LLM (6 h) | H1 · Fundamentos y prompting |

**Objetivo:** Explicar el flujo básico de un LLM y anticipar el impacto del contexto y la tokenización.
<!-- cabecera:fin -->

Al terminar esta sesión sabrás explicar qué ocurre dentro de un LLM desde que recibe un texto hasta que devuelve una respuesta, y podrás anticipar tres cosas que deciden el éxito de un proyecto: cuántos tokens consume una tarea, qué cabe en la ventana de contexto y cuánta memoria necesita un modelo.

Es una sesión de experimentos. Cada afirmación de los apuntes la vas a comprobar con código y la vas a anotar en el cuaderno de experimentos de tu equipo.

<!-- agenda:inicio -->
### Agenda de la sesión

| Hora | Min | Tipo | Bloque |
| --- | --- | --- | --- |
| 09:00 | 15 | Teoría | Activación: ¿cuántos tokens tiene esta frase? |
| 09:15 | 55 | Teoría | Teoría I: anatomía de un LLM |
| 10:10 | 70 | Práctica | Laboratorio: experimentos de tokenización y coste |
| 11:20 | 10 | Pausa | Pausa |
| 11:30 | 50 | Teoría | Teoría II: ventana de contexto y modelos fundacionales (demo de Colibri) |
| 12:20 | 70 | Práctica | Reto 1: la aguja en el pajar (longitud de contexto) |
| 13:30 | 10 | Pausa | Pausa |
| 13:40 | 56 | Práctica | Reto 2: instrucciones, muestreo y benchmark local frente a servidor |
| 14:36 | 24 | Teoría | Cierre: conclusiones del cuaderno |

Teoría: 2 h 24 min · práctica: 3 h 36 min (las pausas computan en el bloque práctico).
<!-- agenda:fin -->

## Lo que entregas hoy

| Entregable | Dónde | Quién |
| --- | --- | --- |
| Cuaderno de experimentos con evidencias y conclusiones | `docs/cuaderno_experimentos.md` (o `.ipynb`) del repositorio del equipo | Equipo |
| Ejercicios 1 a 4 con los tests en verde | `sesion_03_llm_tokens_contexto/ejercicios/` | Cada persona |

---

## 3.1 Qué es un LLM

Un modelo de lenguaje grande (*Large Language Model*) es una red neuronal con miles de millones de **parámetros** entrenada para una sola tarea: dado un texto, predecir el siguiente fragmento. Todo lo demás (responder preguntas, traducir, programar, resumir) emerge de hacer esa tarea muy bien con muchísimos datos.

| Concepto | Qué es | Orden de magnitud |
| --- | --- | --- |
| Parámetros (pesos) | Los números que el entrenamiento ajusta | De 1.000 millones (1B) a más de 1 billón |
| Vocabulario | Los tokens que el modelo conoce | 32.000 a 260.000 tokens |
| Ventana de contexto | Cuántos tokens puede ver a la vez (entrada + salida) | De 4.000 a más de 1 millón |
| Datos de preentrenamiento | Texto con el que aprendió | Billones de tokens |

Cuando leas `qwen3:4b` o `granite4:micro`, el número es el tamaño: 4B son unos 4.000 millones de parámetros. Más parámetros suele significar más conocimiento y mejor razonamiento, pero también más memoria y menos velocidad.

### El flujo completo de una petición

```
Texto ──► Tokenizador ──► IDs de tokens ──► Embeddings ──► N capas Transformer ──► Probabilidades del siguiente token
                                                                                          │
              Texto de salida ◄── Detokenizador ◄── Token elegido (muestreo) ◄──────────┘
                                                         │
                                                         └─► se añade a la entrada y se repite
```

---

## 3.2 Tokenización

Un **token** es la unidad mínima que procesa el modelo: una palabra frecuente, un trozo de palabra, un signo o un espacio. Los tokenizadores modernos (BPE y similares) aprenden de los datos qué fragmentos son frecuentes y los convierten en tokens.

Lo que tienes que saber de los tokens:

- **No son palabras.** En inglés, una palabra son unos 1,3 tokens de media; en español, algo más, porque los tokenizadores se entrenaron con más inglés.
- **El coste y el límite de contexto se miden en tokens**, no en palabras ni en caracteres.
- **Los números y los nombres raros se trocean mucho.** `48.379` pueden ser varios tokens. Por eso los LLM fallan con la aritmética y con contar letras: no «ven» los caracteres.
- **Cada familia de modelos tiene su propio tokenizador.** El mismo texto ocupa distinto en Qwen que en Granite.

```python
import tiktoken

codificador = tiktoken.get_encoding("o200k_base")
tokens = codificador.encode("La logística inversa recupera los palés vacíos.")
print(len(tokens), [codificador.decode([t]) for t in tokens])
```

`tiktoken` es el tokenizador de los modelos de OpenAI. Lo usamos como referencia rápida porque no necesita descargar ningún modelo, salvo un fichero pequeño la primera vez. Para el recuento exacto del modelo que usas, Ollama devuelve los tokens procesados en cada respuesta (ejemplo 2).

### Cuánto cuesta una tarea

Si usas un servicio de pago, el precio va por millón de tokens, con tarifas distintas para la entrada y la salida (la salida suele ser entre 3 y 5 veces más cara). Si usas modelos locales, el coste es de tiempo: los tokens de salida se generan de uno en uno.

```
coste = tokens_entrada × precio_entrada / 1.000.000 + tokens_salida × precio_salida / 1.000.000
```

---

## 3.3 Dentro del modelo: embeddings y atención

### Embeddings de tokens

Cada token se convierte en un vector de miles de números (su *embedding*). Tokens con significado parecido tienen vectores parecidos. Lo trabajarás en profundidad en la sesión 6.

### La arquitectura Transformer

El Transformer procesa todos los tokens a la vez y, en cada capa, deja que cada token «mire» a los demás mediante el mecanismo de **atención**: para cada token calcula cuánto le importa cada uno de los anteriores y mezcla su información. Así, en «el camión que salió de Vigo llegó tarde porque **se** averió», la atención permite relacionar «se» con «camión».

| Variante | Qué hace | Ejemplos |
| --- | --- | --- |
| Solo codificador | Entiende texto; no genera | Modelos de embeddings, BERT |
| Solo decodificador | Genera texto token a token | Todos los LLM de chat actuales |
| Codificador-decodificador | Transforma una secuencia en otra | Modelos de traducción clásicos |

### Mezcla de expertos (MoE)

En un modelo denso, todos los parámetros trabajan en cada token. En un modelo **MoE**, cada capa tiene muchos «expertos» y un enrutador elige unos pocos para cada token. Un modelo MoE de 35B con 3B activos tiene el conocimiento de un modelo grande pero calcula como uno pequeño. Eso sí: **necesita tener todos los expertos accesibles**, por eso ocupa mucha memoria. Colibri explota justo esa idea: guarda los expertos en disco y solo carga los que necesita.

---

## 3.4 La ventana de contexto

La ventana de contexto es el número máximo de tokens que el modelo puede considerar a la vez: mensaje de sistema, historial, documentos que le pases **y** la respuesta que genera.

Lo que pasa cuando te acercas al límite:

| Efecto | Explicación |
| --- | --- |
| Truncado | Si la entrada no cabe, el servidor corta (normalmente el principio). En Ollama, por defecto la ventana es pequeña: si no la amplías con `num_ctx`, el modelo «olvida» el inicio de documentos largos |
| Más memoria | Cada token del contexto ocupa memoria en la **caché KV** (claves y valores de la atención). Duplicar el contexto duplica esa memoria |
| Más lentitud | Procesar la entrada (*prefill*) cuesta más cuanto más larga es |
| Perdido en el medio | Los modelos recuerdan mejor la información del principio y del final que la del medio de un contexto largo |

Por eso el RAG (sesión 5) no consiste en meter todos los documentos en el contexto, sino en meter **solo los fragmentos relevantes**.

### Fijar el contexto en Ollama

En la API nativa, la ventana se fija con la opción `num_ctx`:

```python
from comun import ollama

r = ollama.chat_nativo("Resume este texto: ...", opciones={"num_ctx": 8192})
print(r["prompt_eval_count"], "tokens de entrada procesados")
```

En LM Studio se ajusta al cargar el modelo (*Context Length*).

---

## 3.5 Parámetros de muestreo

El modelo devuelve una probabilidad para cada token posible. **Cómo se elige** uno es configurable:

| Parámetro | Qué hace | Efecto práctico |
| --- | --- | --- |
| `temperature` | Divide las puntuaciones antes de convertirlas en probabilidades. Baja: casi siempre el más probable. Alta: más variedad | 0 para extracción, clasificación y código; 0,7-1 para redacción creativa |
| `top_p` | Solo considera los tokens más probables cuya probabilidad acumulada llega a `p` | 0,9 evita tokens absurdos con temperatura alta |
| `top_k` | Solo considera los `k` tokens más probables | Alternativa más brusca a `top_p` |
| `seed` | Semilla del generador aleatorio | Reproducibilidad de experimentos |
| `max_tokens` | Límite de tokens generados | Controla coste y tiempo |
| `repeat_penalty` | Penaliza repetir tokens recientes | Evita bucles en modelos pequeños |

**Temperatura 0 no garantiza respuestas idénticas** en todos los motores (el cálculo en GPU no siempre es determinista), pero se acerca mucho.

---

## 3.6 Modelos fundacionales

Un **modelo fundacional** es un modelo grande preentrenado de forma general que sirve de base para muchas tareas. Del modelo base al asistente que usas hay varias fases (sesión 2): preentrenamiento, ajuste con instrucciones, alineamiento y, en algunos, entrenamiento para razonar.

### Modelos que razonan

Algunos modelos (como `qwen3:4b`) generan primero un razonamiento interno y después la respuesta. Ollama separa ese razonamiento en el campo `reasoning`. Mejora la calidad en problemas de varios pasos, pero **gasta muchos más tokens y tiempo**: en el laboratorio de la sesión 2 viste que tarda bastante más que `granite4:micro` en responder lo mismo.

### Cuantización

Los pesos se entrenan con 16 bits por parámetro. **Cuantizar** es representarlos con menos bits (8, 5, 4...) a cambio de una pequeña pérdida de calidad. Es lo que permite ejecutar un modelo de 8B en un portátil.

| Formato | Bits por parámetro (aprox.) | Memoria de un modelo de 8B | Calidad |
| --- | --- | --- | --- |
| FP16 / BF16 | 16 | ~15 GB | Referencia |
| Q8_0 | 8,5 | ~8 GB | Casi idéntica |
| Q5_K_M | 5,7 | ~5,4 GB | Muy buena |
| Q4_K_M | 4,8 | ~4,5 GB | Buena: el estándar en local |
| Q2_K | 3 | ~3 GB | Notablemente peor |

**GGUF** es el formato de fichero de llama.cpp, el motor que usan por dentro Ollama y LM Studio. Contiene los pesos cuantizados, el tokenizador y la plantilla de chat.

### Cuánta memoria necesita un modelo

```
memoria_pesos ≈ parámetros × bits / 8
memoria_caché_KV ≈ 2 × capas × cabezas_kv × dimensión_cabeza × tokens_de_contexto × 2 bytes
memoria_total ≈ (pesos + caché KV) × 1,1   (margen del motor)
```

En un portátil de 16 GB, el sistema operativo, el IDE y el navegador ocupan 6-7 GB: quedan unos 8 GB para el modelo y su contexto. Por eso el curso usa modelos de 3-4B en local y el servidor para los grandes. Lo calcularás en el ejercicio 2.

### Ficha del modelo y licencia

Antes de usar un modelo en un proyecto revisa su ficha (*model card*): tamaño, ventana de contexto, idiomas, si admite herramientas, datos de entrenamiento declarados, resultados en evaluaciones y licencia. En Ollama: `ollama show granite4:micro`.

---

## Errores frecuentes

| Error | Síntoma | Solución |
| --- | --- | --- |
| No ampliar `num_ctx` con documentos largos | El modelo ignora el principio del documento | Fija `num_ctx` suficiente (y vigila la memoria) |
| Medir velocidad en la primera llamada | Tiempos enormes | La primera llamada carga el modelo: descártala |
| Comparar tokens de modelos distintos con tiktoken | Cifras que no cuadran | Usa `prompt_eval_count` de Ollama para el modelo concreto |
| Pedir aritmética exacta al LLM | Resultados erróneos con seguridad | Que el modelo llame a una función de cálculo (sesión 9) |

## Para saber más

- Andrej Karpathy, *Let's build the GPT Tokenizer* (vídeo y código): [github.com/karpathy/minbpe](https://github.com/karpathy/minbpe)
- Jay Alammar, *The Illustrated Transformer*: [jalammar.github.io/illustrated-transformer](https://jalammar.github.io/illustrated-transformer/)
- Liu et al. (2023), *Lost in the Middle*: [arxiv.org/abs/2307.03172](https://arxiv.org/abs/2307.03172)
- Documentación de los parámetros de Ollama: [docs.ollama.com/modelfile](https://docs.ollama.com/modelfile)
