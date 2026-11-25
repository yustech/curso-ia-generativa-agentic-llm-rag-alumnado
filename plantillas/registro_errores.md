# Registro de errores del agente · <reto>

> Sesión 8 en adelante. Cada fallo observado en una traza se anota aquí con su causa. Es la materia prima de las regresiones de la sesión 13.

| Fecha | Caso / entrada | Traza | Qué pasó | Tipo de error | Causa raíz | Corrección | ¿Prueba de regresión? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | `trazas/...jsonl` | | herramienta equivocada / argumentos inválidos / bucle / alucinación / no se detuvo / guardarraíl | | | Sí / No |

## Tipos de error frecuentes

- **Herramienta equivocada**: mejorar la descripción de la herramienta (cuándo usarla y cuándo no).
- **Argumentos inválidos**: tipos cerrados y restricciones en Pydantic; mensaje de error útil para el modelo.
- **Bucle**: detector de repeticiones y máximo de pasos.
- **Cálculo hecho por el modelo**: moverlo a una herramienta determinista.
- **Responde sin consultar**: instrucción en el sistema y prueba con `LLMFalso`.
