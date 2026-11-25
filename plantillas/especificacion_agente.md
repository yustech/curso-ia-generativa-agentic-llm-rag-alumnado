# Especificación del agente · <reto> · tarea acotada

> Sesión 8. Especificad **una sola tarea** antes de programar. Si una sección no se puede rellenar, la tarea no está lista.

## 1. Objetivo

<Una frase con verbo, objeto y criterio de terminado.>

## 2. Entradas y salidas

| | Descripción | Formato | Ejemplo |
| --- | --- | --- | --- |
| Entrada | | texto libre / JSON | |
| Salida | | texto con citas / JSON validado (Pydantic) | |

## 3. Herramientas

| Herramienta | Argumentos | Permiso | Confirmación humana |
| --- | --- | --- | --- |
| | | lectura / escritura / acción externa | no / sí |

## 4. Estado de trabajo

<Qué guarda el agente entre pasos: plan, resultados intermedios, memoria de conversación (ventana o resumen), datos pendientes de pedir al usuario.>

## 5. Patrón

- [ ] ReAct · [ ] Planificar-ejecutar · [ ] Workflow con un paso de LLM
- Por qué: <...>

## 6. Límites

| Límite | Valor |
| --- | --- |
| Pasos máximos | |
| Repeticiones de la misma llamada | |
| Tiempo máximo por tarea | |
| Tokens de contexto (`num_ctx`) | |
| Temas fuera de alcance | |

## 7. Guardarraíles

| Capa | Control | Dónde está en el código |
| --- | --- | --- |
| Entrada | Detección de inyección / datos personales | |
| Herramientas | Lista blanca, validación de argumentos, mínimo privilegio | |
| Salida | Formato, citas, abstención | |

## 8. Criterios de éxito

| Métrica | Umbral | Cómo se mide |
| --- | --- | --- |
| Tarea completada correctamente | ≥ 80 % de 5 casos del conjunto dorado | Revisión manual de trazas |
| Herramientas correctas en el orden correcto | | Trazas |
| Sin acciones con efectos sin confirmación | 100 % | Prueba automática |
