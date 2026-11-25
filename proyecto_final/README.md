# Proyecto final: asistente basado en LLM con RAG para Atlántica Logística

El proyecto final es el asistente que tu equipo ha ido construyendo durante todo el curso, terminado, evaluado y defendido ante un comité el **miércoles 23 de diciembre**. Cuenta un **40 % de la nota del curso**.

## El encargo

Atlántica Logística quiere decidir si invierte en asistentes de IA generativa con modelos locales (plataforma Faro-IA). Ha encargado a la consultora tres pilotos, uno por equipo:

| Equipo | Reto | Usuario | Encargo |
| --- | --- | --- | --- |
| Equipo 1 | R1 · DevAssist | Equipo de Desarrollo de aplicaciones | Asistente que responde dudas sobre la guía de estilo y la arquitectura, revisa código y propone pruebas |
| Equipo 2 | R2 · InfraPilot | Equipo de Plataforma e infraestructura | Asistente que convierte peticiones de entornos en propuestas de Terraform conformes a la política y prepara la solicitud de cambio para su aprobación |
| Equipo 3 | R3 · PMO Copilot | Jefes y jefas de proyecto | Asistente que convierte actas en historias de usuario, mantiene el backlog y redacta el informe de estado semanal |

## Requisitos mínimos

1. **Asistente basado en LLM** con una necesidad y unos usuarios definidos (canvas del caso de uso).
2. **Componente RAG** con fuentes identificadas, estrategia de indexación (incremental) y pruebas de recuperación (hit@k, MRR).
3. **Al menos una herramienta o acción controlada** con contrato, validación y, si tiene efectos, confirmación humana.
4. **Métricas y conjunto de pruebas** para calidad, relevancia y robustez: conjunto dorado de 30 o más casos, evaluación de extremo a extremo con línea base, red teaming y prueba de carga.
5. **Controles de privacidad, seguridad, uso responsable y supervisión humana**: guardarraíles en código, mínimo privilegio, transparencia, sin datos personales ni secretos.
6. **Documentación reproducible, demo funcional y explicación de las decisiones** (ADR).

## Estructura del repositorio del equipo

Partid de `equipos/plantilla_proyecto/`:

```
asistente-<reto>/
├── README.md                    Instalación, uso, arquitectura y limitaciones
├── app.py                       Interfaz (streamlit run app.py)
├── requirements.txt
├── .env.example
├── agente/                      Lógica del asistente, flujo y guardarraíles
├── rag/                         Ingesta incremental y búsqueda
├── herramientas/                Herramientas con contrato
├── mcp/                         Servidor MCP (opcional)
├── documental/                  Pipeline documental (si aplica)
├── evals/
│   ├── golden_set.jsonl         30 o más casos de los cinco tipos
│   ├── preguntas_recuperacion.jsonl
│   └── evaluar.py               Evaluación de extremo a extremo
├── tests/                       10 o más pruebas deterministas
└── docs/
    ├── ficha_agente.md          Ficha del sistema (plantilla)
    ├── canvas_caso_uso.md
    ├── propuesta_tecnica.md
    ├── plan_validacion.md
    ├── informe_evaluacion.md
    ├── matriz_riesgos.md
    ├── adr/                     Decisiones de arquitectura
    └── presentacion.md
```

## Calendario

| Fecha | Hito del proyecto |
| --- | --- |
| Sesiones 1-4 | Hito 1: reto asignado, riesgos, prompts y conjunto dorado v0 |
| Sesiones 5-7 | Hito 2: RAG con índice y checklist de calidad · revisión intermedia (14/12) |
| Sesiones 8-10 | Hito 3: agente con herramientas, pruebas y decisión tecnológica |
| Sesiones 11-13 | Hito 4: interfaz, pipeline documental, evaluación, seguridad y carga; definición final |
| 23/12 | Demo Day: entrega de la etiqueta `v1.0`, demo y defensa |

## Demo (15 minutos + 15 de preguntas)

Estructura obligatoria en el apartado 14.3 de la sesión 14: problema, solución, demo en directo (caso normal, caso con herramienta y confirmación, caso sin respuesta, intento de ataque), métricas, valor y siguientes pasos.

## Rúbrica (30 puntos)

| Criterio | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| **1. Necesidad y valor** | Sin usuario ni problema claros | Problema genérico | Problema concreto con usuario | Problema concreto, usuario, AS-IS/TO-BE y caso de negocio con números |
| **2. RAG** | No hay | Funciona sin evaluación | Evaluado con hit@k/MRR | Evaluado, incremental, con decisiones justificadas |
| **3. Herramientas y acciones** | No hay | Una sin validación | Con contrato y validación | Con contrato, validación, permisos y confirmación humana |
| **4. Arquitectura y decisiones** | Sin documentar | Diagrama | Diagrama y ADR | Diagrama, ADR y alternativas evaluadas con datos |
| **5. Calidad y evaluación** | Sin pruebas | Pruebas ad hoc | Conjunto dorado y métricas | 30+ casos, línea base, juez calibrado y regresiones |
| **6. Seguridad y uso responsable** | No considerado | En el prompt | Guardarraíles en código | Guardarraíles en capas, red teaming y transparencia |
| **7. Ingeniería** | No arranca | Arranca con ayuda | Reproducible | Reproducible, con pruebas en verde y sin secretos |
| **8. Rendimiento y operación** | No considerado | Medido en local | Prueba de carga | Prueba de carga, coste y propuesta de despliegue |
| **9. Demo** | No funciona | Funciona con fallos graves | Funciona | Funciona, incluye casos límite y tiene plan B |
| **10. Comunicación y defensa** | Confusa | Técnica sin negocio | Clara | Clara, con datos, reconoce límites y responde con solvencia |

Nota del proyecto = puntos / 30 × 10. Cada persona del comité puntúa por separado y la nota es la media. La evaluación entre pares puede ajustar la nota individual del proyecto hasta un ± 10 %.

## Entrega

Antes de las 10:45 del 23 de diciembre:

1. Etiqueta `v1.0` en el repositorio del equipo (`git tag v1.0 && git push --tags`).
2. El verificador `sesion_14_proyecto_final/ejercicios/s14_ej1_verificar_entrega.py` devuelve «Entrega completa: sí».
3. Enlace al repositorio enviado al docente.
