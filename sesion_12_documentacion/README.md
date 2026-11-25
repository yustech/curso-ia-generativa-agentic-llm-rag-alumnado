# Sesión 12. Generación de documentación, análisis documental y automatización de procesos

<!-- cabecera:inicio -->
| Fecha | Horario | Modalidad | Módulos | Hito |
| --- | --- | --- | --- | --- |
| Lunes 21 de diciembre de 2026 | 09:00-15:00 | Remoto | M6 · Aplicaciones prácticas de IA Generativa (6 h) | H4 · Aplicación y proyecto |

**Objetivo:** Aplicar GenAI a documentos con criterios de calidad, trazabilidad y revisión humana.
<!-- cabecera:fin -->

Los documentos son el caso de uso de IA generativa más rentable en una consultora y en sus clientes: actas, informes, contratos, especificaciones, documentación técnica. Al terminar esta sesión sabrás extraer información estructurada de documentos, generar documentos con control de calidad y, sobre todo, **garantizar la trazabilidad**: que cada dato de un documento generado se pueda rastrear hasta su fuente.

<!-- agenda:inicio -->
### Agenda de la sesión

| Hora | Min | Tipo | Bloque |
| --- | --- | --- | --- |
| 09:00 | 15 | Teoría | Activación: 40 actas y un viernes por la tarde |
| 09:15 | 55 | Teoría | Teoría I: análisis documental y extracción estructurada |
| 10:10 | 70 | Práctica | Laboratorio: de las actas a JSON validado |
| 11:20 | 10 | Pausa | Pausa |
| 11:30 | 50 | Teoría | Teoría II: generación documental controlada y LLM como juez |
| 12:20 | 70 | Práctica | Reto 1: pipeline documental del reto |
| 13:30 | 10 | Pausa | Pausa |
| 13:40 | 56 | Práctica | Reto 2: informe de validación y trazabilidad |
| 14:36 | 24 | Teoría | Cierre: preguntas de repaso |

Teoría: 2 h 24 min · práctica: 3 h 36 min (las pausas computan en el bloque práctico).
<!-- agenda:fin -->

## Lo que entregas hoy

| Entregable | Dónde | Quién |
| --- | --- | --- |
| Pipeline documental del reto | `documental/` del repositorio del equipo | Equipo |
| Informe de validación y trazabilidad | `docs/informe_validacion.md` | Equipo |
| Ejercicios 1 a 3 con los tests en verde | `sesion_12_documentacion/ejercicios/` | Cada persona |

---

## 12.1 Análisis documental

| Tarea | Qué produce | Ejemplo en Atlántica |
| --- | --- | --- |
| Clasificar | Tipo, tema o prioridad del documento | ¿Es un acta, un contrato o una incidencia? |
| Extraer | Campos estructurados | Acciones, responsables y fechas de un acta |
| Resumir | Versión breve | Resumen de un mes de actas para dirección |
| Comparar | Diferencias entre versiones o frente a una norma | ¿Cumple este contrato la política de proveedores? |
| Responder | Respuesta a una pregunta con fuente | RAG (sesiones 5 a 7) |

## 12.2 Extracción estructurada

Es la tarea documental más fiable con modelos pequeños, porque el modelo no tiene que crear sino localizar y copiar. Las claves:

1. **Un esquema** (Pydantic) con campos obligatorios y opcionales.
2. **Instrucción de no inventar**: si un dato no aparece, `null` o lista vacía. Un campo obligatorio que el documento no contiene invita a alucinar.
3. **Copiar tal cual y normalizar con código**: pide al modelo la fecha «tal como aparece» y conviértela tú a ISO con una función determinista. Los modelos se equivocan más calculando fechas que copiándolas.
4. **Validación de forma** (el esquema) y **de trazabilidad** (que cada dato aparezca en el texto).

```python
class Accion(BaseModel):
    descripcion: str
    responsable: str = Field(description="Nombre tal como aparece en el acta")
    fecha: str | None = Field(default=None, description="Fecha tal como aparece, o null")
```

## 12.3 Resumen de documentos largos

| Técnica | Cómo | Cuándo |
| --- | --- | --- |
| Directo | Todo el documento en el contexto | Cabe en la ventana con margen |
| Map-reduce | Resumir cada parte por separado (*map*) y luego resumir los resúmenes (*reduce*) | Documentos o colecciones grandes |
| Refinado | Resumen inicial que se va actualizando con cada parte | Cuando el orden importa (una historia, un hilo) |
| Extractivo | Seleccionar frases literales importantes | Cuando la fidelidad literal es crítica |

Cuidado con los resúmenes de resúmenes: cada paso puede perder o deformar datos. Para dirección, mejor un resumen que cite el acta de la que sale cada punto.

## 12.4 Generación documental controlada

El error de principiante es pedir al LLM «escribe el informe de estado». El resultado es fluido, pero mezcla datos ciertos con inventados y cambia de estructura cada vez. El enfoque profesional reparte el trabajo:

| Lo hace el código | Lo hace el LLM |
| --- | --- |
| La estructura (plantilla) | La redacción de las partes en lenguaje natural |
| Las cifras y los cálculos (puntos, porcentajes, exposición) | El resumen ejecutivo a partir de esas cifras |
| Las reglas (semáforo, riesgos que se escalan) | La explicación de los riesgos |
| Las fuentes | Nada que no esté en los datos que se le pasan |

Es la misma idea de las herramientas deterministas de la sesión 9, aplicada a documentos.

Ejemplos de generación documental en desarrollo de software: documentación de API a partir del código, docstrings, notas de versión a partir de los commits, README de un repositorio, descripción de una merge request, guiones de prueba a partir de criterios de aceptación.

## 12.5 Trazabilidad

Un documento generado es **trazable** si cada dato se puede rastrear hasta una fuente concreta:

- Citas o referencias a la fuente (acta, sección, línea).
- Comprobación automática de que nombres, cifras y fechas aparecen en el original.
- Registro de qué versión del prompt, qué modelo y qué fuentes produjeron el documento.

En consultoría esto no es un detalle: un informe a dirección con un dato inventado destruye la credibilidad del equipo.

## 12.6 Control de calidad en tres capas

| Capa | Qué detecta | Coste | Ejemplo |
| --- | --- | --- | --- |
| Comprobaciones deterministas | Estructura, cifras, formatos, campos vacíos | Casi nulo | Las seis secciones están; «30 de 34 puntos» coincide con los datos |
| LLM como juez | Calidad del texto, fidelidad, tono, omisiones | Una llamada por documento | Rúbrica: ¿afirma algo que no está en los datos? |
| Revisión humana | Todo lo demás y la responsabilidad final | Alto | Revisión de una muestra o de los documentos que las capas anteriores marcan |

### LLM como juez

Usar un modelo para evaluar la salida de otro escala la evaluación, pero tiene sesgos conocidos: prefiere respuestas largas, puede preferir su propio estilo y es inconsistente con rúbricas vagas. Buenas prácticas:

- Rúbrica concreta, con criterios observables.
- Salida estructurada (puntuación, ¿cumple?, motivos).
- Darle los **datos de origen**, no solo el documento.
- **Calibrarlo**: comparar sus juicios con los de personas en una muestra antes de fiarse.

### Muestreo para revisión humana

Revisar el 100 % no escala; no revisar nada no es responsable. Lo habitual: revisar siempre lo que las comprobaciones o el juez marcan, más una **muestra aleatoria reproducible** del resto (por ejemplo, el 20 %). Si la muestra encuentra errores, se amplía.

---

## Errores frecuentes

| Error | Síntoma | Solución |
| --- | --- | --- |
| Campos obligatorios que el documento no siempre contiene | El modelo inventa responsables o fechas | Campos opcionales y abstención |
| Pedir al modelo que calcule o normalice | Fechas y cifras erróneas | Copiar tal cual y normalizar con código |
| Generar el documento entero con el LLM | Estructura y cifras inestables | Plantilla y datos por código, redacción por el LLM |
| Juez sin datos de origen | No detecta invenciones | Pasar siempre los datos |
| Revisar solo lo que parece mal | Errores sistemáticos invisibles | Muestra aleatoria |

## Para saber más

- Zheng et al. (2023), *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*: [arxiv.org/abs/2306.05685](https://arxiv.org/abs/2306.05685)
- Documentación de salidas estructuradas de Ollama: [docs.ollama.com/capabilities/structured-outputs](https://docs.ollama.com/capabilities/structured-outputs)
