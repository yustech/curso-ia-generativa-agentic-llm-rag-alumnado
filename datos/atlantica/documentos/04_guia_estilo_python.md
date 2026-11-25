---
titulo: Guía de estilo de Python
codigo: ATL-DES-004
version: 3.2
fecha: 2026-02-20
propietario: Desarrollo de aplicaciones
clasificacion: Interno
---

# Guía de estilo de Python

Esta guía se aplica a todo el código Python nuevo de Atlántica Logística (Faro, integraciones y herramientas internas). El código heredado se adapta cuando se modifica.

## 1. Versión y herramientas

- Versión de Python: **3.12**.
- Formato automático con `black`, longitud de línea **100**.
- Análisis estático con `ruff` (reglas `E`, `F`, `I`, `B`, `UP`). El pipeline de integración continua falla si hay avisos.
- Comprobación de tipos con `mypy` en modo estricto para los paquetes nuevos.

## 2. Nombres

- Funciones, variables y módulos en `snake_case`; clases en `PascalCase`; constantes en `MAYUSCULAS`.
- Los conceptos del negocio se nombran en español y sin abreviaturas: `tarifa`, `ruta`, `envio`, `cliente`, `peso_kg`.
- No se usan nombres de una letra salvo en comprensiones cortas.

## 3. Tipos y documentación

- Las anotaciones de tipo son **obligatorias** en todas las funciones y métodos públicos.
- Toda función pública tiene un docstring en español con estilo Google: resumen de una línea, `Args:`, `Returns:` y `Raises:` cuando corresponda.

## 4. Importes y cálculos monetarios

- Los importes **nunca** se representan con `float`. Se usa `decimal.Decimal`.
- Los importes se redondean a 2 decimales con `ROUND_HALF_UP` solo al final del cálculo.
- Los porcentajes se expresan como `Decimal("0.21")`, no como `21`.

## 5. Errores y registro

- Las excepciones propias heredan de `AtlanticaError` (paquete `atlantica.errores`).
- No se captura `Exception` de forma genérica salvo en el punto de entrada de un proceso, y siempre se registra.
- **Prohibido usar `print` en código de producción.** Se usa el módulo `logging` con el registrador del módulo: `logger = logging.getLogger(__name__)`.
- No se registran datos personales completos ni secretos.

## 6. Pruebas

- Las pruebas se escriben con `pytest` en la carpeta `tests/` del paquete.
- Cobertura mínima del **80 %** en los módulos nuevos o modificados.
- Cada corrección de un error incluye una prueba que lo reproduce.
- Las pruebas no acceden a servicios externos: se usan dobles de prueba.

## 7. Control de versiones y revisión

- Mensajes de commit con Conventional Commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`.
- Toda merge request necesita **una aprobación** de otra persona del equipo y el pipeline en verde.
- Una merge request no debería superar las 400 líneas cambiadas; si las supera, se divide.

## 8. Ejemplo

```python
import logging
from decimal import ROUND_HALF_UP, Decimal

logger = logging.getLogger(__name__)
IVA_GENERAL = Decimal("0.21")


def precio_con_iva(base: Decimal) -> Decimal:
    """Calcula el precio con IVA general.

    Args:
        base: Importe sin impuestos.

    Returns:
        Importe con IVA redondeado a 2 decimales.
    """
    total = base * (1 + IVA_GENERAL)
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
```
