# Práctica 3. Cuaderno de experimentos

Entregable del equipo: `docs/cuaderno_experimentos.md` (o un cuaderno `.ipynb` con sus conclusiones en Markdown).

Un cuaderno de experimentos es el documento en el que un equipo técnico deja constancia de **qué hipótesis probó, cómo, qué obtuvo y qué decide**. Es la costumbre que separa la intuición («parece que va mejor») de la ingeniería («con 8K de contexto el modelo encuentra el dato en 6 de 6 pruebas y tarda el doble»).

## Estructura de cada experimento

```markdown
## Experimento N. Título

- **Hipótesis:** lo que creemos que va a pasar, antes de probarlo.
- **Método:** qué ejecutamos, con qué modelo, parámetros y número de repeticiones.
- **Resultados:** tabla con los datos obtenidos (no capturas de pantalla).
- **Conclusión:** qué aprendemos y qué decisión tomamos para nuestro asistente.
```

## Los cinco experimentos

| N.º | Experimento | Ejercicio | Decisión que alimenta para el reto |
| --- | --- | --- | --- |
| 1 | Tokens en español, en inglés, en código y en tablas, con tiktoken y con el recuento de cada modelo | 1 | ¿Cuántos tokens ocupan nuestros documentos? ¿Cuánto costaría el asistente con un servicio de pago? |
| 2 | Memoria de tres modelos con tres tamaños de contexto: cálculo frente a medición | 2 | ¿Qué modelo y qué contexto máximo usamos en el portátil? |
| 3 | La aguja en el pajar con dos longitudes, tres posiciones y dos `num_ctx` | 3 | ¿Qué `num_ctx` necesitamos? ¿Podemos meter todos los documentos en el contexto o hace falta RAG? |
| 4 | Diversidad de respuestas con tres temperaturas | 4 | ¿Qué temperatura usamos para cada tipo de tarea del asistente? |
| 5 | Velocidad del portátil frente al servidor compartido | 4 | ¿Qué partes del trabajo hacemos en local y cuáles en el servidor? |

### Datos de vuestro reto para el experimento 1 y el 3

| Reto | Textos para medir tokens | Contexto que necesitaría el asistente |
| --- | --- | --- |
| R1 · DevAssist | `04_guia_estilo_python.md` y `codigo/tarifas/calculo.py` | Guía + arquitectura + fichero de código |
| R2 · InfraPilot | `06_politica_infraestructura_cloud.md` y `07_catalogo_modulos_terraform.md` | Política + catálogo + procedimiento de cambios |
| R3 · PMO Copilot | Las cuatro actas y `backlog.json` | Actas de un mes + metodología + backlog |

Para el experimento 3, repetid la prueba usando como pajar vuestros documentos reales en lugar de las frases de relleno.

## Conclusiones finales

Cerrad el cuaderno con una sección **«Decisiones para el asistente»** de 5 a 10 líneas: modelo por defecto, `num_ctx`, temperatura por tipo de tarea, qué se ejecuta en local y qué en el servidor, y si los documentos caben en el contexto o necesitáis RAG.

## Entrega

1. `docs/cuaderno_experimentos.md` con los cinco experimentos y las decisiones.
2. Commit: `Sesión 3: cuaderno de experimentos`.

## Criterios de evaluación (0 a 3 puntos cada uno)

| Criterio | 3 puntos |
| --- | --- |
| Método | Hipótesis previas, parámetros documentados y repeticiones |
| Evidencias | Tablas con datos propios y reproducibles |
| Interpretación | Explica los resultados con los conceptos de los apuntes |
| Decisiones | Concretas y derivadas de los datos |
