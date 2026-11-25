# Contrato de herramientas · <reto>

> Sesión 9. Una ficha por herramienta. La descripción y los argumentos son **lo que ve el modelo**: escribidlos para él.

## Herramienta: `<nombre>`

| Campo | Valor |
| --- | --- |
| Descripción (tal como la ve el modelo) | <Qué hace, cuándo usarla y cuándo NO usarla> |
| Sistema del cliente | <API, fichero, función de `equipos/...`> |
| Efectos | Ninguno (solo lectura) / Modifica <...> / Acción externa |
| Nivel de permiso | lectura / escritura / requiere confirmación humana |
| Idempotente | Sí / No (explicad qué pasa si se llama dos veces) |
| Timeout y reintentos | <p. ej. 10 s, 3 reintentos con espera exponencial solo en errores 5xx y de red> |
| Modo degradado | <Qué responde si el servicio no está disponible> |

### Argumentos

| Nombre | Tipo | Obligatorio | Restricciones | Descripción para el modelo |
| --- | --- | --- | --- | --- |
| | `str` | Sí | `pattern=...` | |
| | `Literal[...]` | | valores cerrados | |
| | `int` | | `ge=..., le=...` | |

```python
class ArgumentosEjemplo(BaseModel):
    """Copiad aquí el modelo Pydantic real."""
```

### Salida

<Formato de la salida (texto breve o JSON) y un ejemplo real.>

### Errores

| Situación | Mensaje que recibe el modelo | Qué debe hacer el modelo |
| --- | --- | --- |
| Argumentos inválidos | `ERROR: argumentos no válidos: ...` | Corregir y reintentar una vez |
| Recurso no encontrado | | |
| Servicio no disponible | | Informar al usuario sin inventar |
| Acción no autorizada | `ERROR: acción no autorizada (...)` | No reintentar |

### Pruebas

| Prueba | Fichero |
| --- | --- |
| Caso normal | `tests/test_herramientas.py::test_...` |
| Caso frontera | |
| Argumentos rechazados | |
