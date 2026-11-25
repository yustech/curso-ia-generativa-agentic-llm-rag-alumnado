# Sesión 9. Herramientas y APIs: tool calling seguro y verificable

<!-- cabecera:inicio -->
| Fecha | Horario | Modalidad | Módulos | Hito |
| --- | --- | --- | --- | --- |
| Miércoles 16 de diciembre de 2026 | 09:00-15:00 | Remoto | M5 · Agentic AI y herramientas avanzadas (6 h) | H3 · Sistema agéntico |

**Objetivo:** Integrar herramientas externas de forma segura y verificable.
<!-- cabecera:fin -->

Al terminar esta sesión sabrás diseñar herramientas para agentes como **contratos**: con esquema, validación de entradas y salidas, errores comprensibles y nivel de permiso explícito. Integrarás una API REST real (simulada) con timeouts y reintentos, y probarás todo con pytest sin necesidad de un modelo.

<!-- agenda:inicio -->
### Agenda de la sesión

| Hora | Min | Tipo | Bloque |
| --- | --- | --- | --- |
| 09:00 | 15 | Teoría | Activación: ¿qué puede salir mal al llamar a una API? |
| 09:15 | 55 | Teoría | Teoría I: contratos de herramientas y validación |
| 10:10 | 70 | Práctica | Laboratorio: herramientas validadas y API simulada |
| 11:20 | 10 | Pausa | Pausa |
| 11:30 | 50 | Teoría | Teoría II: gestión de errores y recuperación |
| 12:20 | 70 | Práctica | Reto 1: agente del equipo con dos herramientas |
| 13:30 | 10 | Pausa | Pausa |
| 13:40 | 56 | Práctica | Reto 2: casos de prueba con pytest |
| 14:36 | 24 | Teoría | Cierre: revisión de contratos entre equipos |

Teoría: 2 h 24 min · práctica: 3 h 36 min (las pausas computan en el bloque práctico).
<!-- agenda:fin -->

## Lo que entregas hoy

| Entregable | Dónde | Quién |
| --- | --- | --- |
| Prototipo funcional del agente con dos herramientas | `agente/` del repositorio del equipo | Equipo |
| Contrato de herramientas | `docs/contrato_herramientas.md` | Equipo |
| Casos de prueba con pytest | `tests/` | Equipo |
| Ejercicios 1 a 3 con los tests en verde | `sesion_09_herramientas_apis/ejercicios/` | Cada persona |

---

## 9.1 Una herramienta es un contrato

Cuando le das una herramienta a un agente, le das una **capacidad** en un sistema real. Su definición es un contrato entre tres partes: el modelo que la invoca, el código que la ejecuta y el sistema que la sufre.

| Elemento del contrato | Para quién | Ejemplo |
| --- | --- | --- |
| Nombre | El modelo | `consultar_historia` (verbo + objeto, sin ambigüedad) |
| Descripción | El modelo | «Devuelve todos los datos de un elemento del backlog. Úsala cuando conozcas el identificador» |
| Esquema de argumentos | El modelo y la validación | `identificador`: texto con el patrón `FARO-\d+` |
| Salida | El modelo | JSON con `ok`, `datos` o `error` |
| Efectos | La persona responsable | Solo lectura / modifica datos / irreversible |
| Errores posibles | El modelo y quien opera | 404 si no existe; 503 si el servicio no responde |
| Límites | Quien opera | Timeout de 5 s, 3 reintentos |

### La descripción es parte del prompt

El modelo decide qué herramienta usar **solo** por su nombre, su descripción y su esquema. Una mala descripción produce llamadas equivocadas. Buenas prácticas:

- Di **cuándo** usarla y cuándo no: «Úsala solo si conoces el identificador; si no, usa `listar_historias`».
- Describe cada parámetro con su formato y un ejemplo.
- Pocas herramientas, bien diferenciadas. Con más de 10-15, los modelos pequeños se confunden.
- Prefiere parámetros con valores cerrados (`Literal`) a texto libre.

---

## 9.2 Diseñar buenas herramientas

| Principio | Mal | Bien |
| --- | --- | --- |
| Granularidad adecuada | `ejecutar_sql(consulta)` | `listar_historias(estado, sprint)` |
| Mínimo privilegio | `gestionar_backlog(accion, ...)` con borrado incluido | Lectura y escritura en herramientas separadas, y sin borrado |
| Determinismo donde se pueda | Pedir al LLM que calcule el coste | `estimar_coste(recursos)` que calcula con el catálogo |
| Idempotencia | `crear_historia` que duplica si se reintenta | Usar un id de petición o comprobar antes |
| Salidas compactas | Devolver 200 campos | Devolver los campos que el modelo necesita |
| Errores accionables | `Exception` | «No existe FARO-999. Usa listar_historias para ver los identificadores» |

La regla más importante, que viste en la traza de la sesión 8: **todo lo que se pueda calcular o comprobar con código no se deja al modelo**. Las herramientas de los retos (`equipos/*/herramientas.py`) están diseñadas así: el validador de la política, la estimación de costes y el comprobador de estilo son deterministas.

---

## 9.3 Validación de entradas y salidas

Los argumentos que propone el modelo son **datos no fiables**: pueden tener un tipo incorrecto, valores fuera de rango o haber sido manipulados mediante una inyección. Valídalos siempre antes de ejecutar.

Con Pydantic, un solo modelo te da el esquema que ve el LLM y la validación:

```python
from typing import Literal
from pydantic import BaseModel, Field

class ArgsListar(BaseModel):
    estado: Literal["Por hacer", "En curso", "En revisión", "Hecho"] | None = None
    sprint: int | None = Field(default=None, ge=1, description="Número de sprint")

ArgsListar.model_json_schema()      # → lo que recibe el modelo
ArgsListar.model_validate(datos)    # → lanza ValidationError si no cumple
```

Cuando la validación falla, **devuelve el error al modelo** en lenguaje claro («sprint: debe ser mayor o igual que 1»). Los modelos suelen corregirse en el siguiente paso.

Valida también las **salidas** cuando vayan a usarse para actuar: un Terraform generado se valida contra la política antes de proponerlo; un código generado se compila con `ast.parse` antes de ejecutar sus pruebas.

---

## 9.4 Integrar APIs externas

```python
import httpx

cliente = httpx.Client(base_url="http://127.0.0.1:8765", timeout=5.0, headers={"X-Api-Key": clave})
respuesta = cliente.get("/historias", params={"sprint": 23})
respuesta.raise_for_status()
historias = respuesta.json()
```

Lo que nunca debe faltar en una integración:

| Elemento | Por qué |
| --- | --- |
| **Timeout** | Sin él, una API colgada bloquea al agente indefinidamente |
| Autenticación con credenciales propias del agente | Trazabilidad y mínimo privilegio; nunca las credenciales de una persona |
| Secretos fuera del código | Variables de entorno o gestor de secretos (`.env` no se sube a Git) |
| Gestión de errores por tipo | No es lo mismo un 404 (no existe) que un 503 (reintenta) |
| Registro | Cada llamada en la traza |

---

## 9.5 Gestión de errores y recuperación

| Tipo de fallo | Ejemplos | Estrategia |
| --- | --- | --- |
| Transitorio | 503, 429, 502, timeout, conexión rechazada | **Reintentar** con espera exponencial (0,5 s, 1 s, 2 s…) y un máximo |
| Definitivo del cliente | 400, 404, 422 | No reintentar; devolver el error al modelo para que corrija |
| Autenticación | 401, 403 | No reintentar; avisar a quien opera |
| Caída prolongada | Todos los reintentos fallan | **Modo degradado**: responder sin inventar, decir qué no se puede hacer |

Dos detalles profesionales:

- **Los reintentos solo son seguros en operaciones idempotentes** (consultar, o actualizar un estado a un valor concreto). Reintentar «crear historia» puede crear dos.
- **Un modo degradado es mejor que una respuesta inventada.** Si el backlog no responde, el asistente dice «no puedo consultar el backlog ahora», no improvisa un estado.

Patrones avanzados que conviene conocer: *circuit breaker* (dejar de llamar a un servicio que falla durante un tiempo), *jitter* (aleatorizar la espera para no saturar al servicio cuando se recupera) y colas para operaciones que pueden esperar.

---

## 9.6 Probar herramientas y agentes

| Qué se prueba | Cómo | Sin modelo |
| --- | --- | --- |
| Herramientas | Pruebas unitarias normales | Sí |
| Validación de argumentos | Casos válidos y no válidos | Sí |
| Cliente de API | `httpx.MockTransport` simula respuestas, errores y timeouts | Sí |
| Bucle del agente | LLM falso con respuestas programadas (`comun.llm.usar_llm_falso`) | Sí |
| Comportamiento real | Conjunto dorado con el modelo | No (se marca como `llm_real`) |

La pirámide es la de siempre: muchas pruebas rápidas y deterministas abajo, y pocas pruebas con el modelo real arriba. Las pruebas deterministas se ejecutan en cada cambio; las del modelo, antes de cada entrega.

```python
def test_reintenta_503():
    respuestas = iter([httpx.Response(503), httpx.Response(200, json={"id": "FARO-1"})])
    cliente = ClienteBacklog("http://api", transporte=httpx.MockTransport(lambda p: next(respuestas)),
                             dormir=lambda s: None)
    assert cliente.obtener("FARO-1") == {"id": "FARO-1"}
```

---

## Errores frecuentes

| Error | Síntoma | Solución |
| --- | --- | --- |
| Una herramienta genérica tipo `ejecutar_sql` | El agente puede hacer cualquier cosa | Herramientas específicas y de mínimo privilegio |
| Ejecutar sin validar los argumentos | Errores raros o acciones peligrosas | Pydantic antes de ejecutar |
| Lanzar la excepción al bucle | El agente se cae | Devolver el error como resultado |
| Reintentar operaciones no idempotentes | Datos duplicados | Reintentar solo lecturas e idempotentes |
| No poner timeout | Agente colgado | Timeout en todas las llamadas |
| Probar solo con el modelo real | Pruebas lentas y que fallan al azar | Pruebas deterministas con dobles |

## Para saber más

- Guía de tool calling de OpenAI (formato que siguen Ollama, LM Studio y vLLM): [platform.openai.com/docs/guides/function-calling](https://platform.openai.com/docs/guides/function-calling)
- Documentación de HTTPX, transportes y pruebas: [www.python-httpx.org](https://www.python-httpx.org/)
- Documentación de Pydantic: [docs.pydantic.dev](https://docs.pydantic.dev/)
