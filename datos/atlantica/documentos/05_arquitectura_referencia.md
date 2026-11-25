---
titulo: Arquitectura de referencia de aplicaciones
codigo: ATL-ARQ-005
version: 2.4
fecha: 2026-04-02
propietario: Oficina de Arquitectura
clasificacion: Interno
---

# Arquitectura de referencia de aplicaciones

## 1. Principios

1. **Arquitectura hexagonal.** La lógica de negocio no depende de frameworks, bases de datos ni servicios externos. Se comunica con ellos a través de puertos (interfaces) y adaptadores.
2. **Servicios pequeños con un propietario claro.** Cada servicio tiene un equipo responsable y su propia base de datos.
3. **Todo por API.** Los servicios se comunican mediante API REST documentadas con OpenAPI o mediante eventos.
4. **Observabilidad desde el inicio.** Todo servicio expone métricas, trazas y registros estructurados.

## 2. Pila tecnológica estándar

| Capa | Tecnología |
| --- | --- |
| Lenguaje de servicios | Python 3.12 |
| Framework de API | FastAPI |
| Base de datos relacional | PostgreSQL 16 |
| Mensajería y eventos | RabbitMQ |
| Caché | Redis |
| Contenedores y orquestación | Docker y Kubernetes |
| Observabilidad | OpenTelemetry, Prometheus y Grafana |
| Integración continua | GitLab CI |

Cualquier tecnología fuera de esta tabla requiere un registro de decisión de arquitectura (ADR) aprobado por la Oficina de Arquitectura.

## 3. Estructura de un servicio

```
servicio/
├── dominio/         Entidades y reglas de negocio (sin dependencias externas)
├── aplicacion/      Casos de uso
├── adaptadores/     API, base de datos, colas, clientes externos
└── tests/           Pruebas unitarias y de integración
```

## 4. Componentes de IA generativa

Los servicios que usan modelos de lenguaje acceden a ellos **solo a través de la pasarela de Faro-IA**, que ofrece una API compatible con OpenAI, registra las peticiones y aplica los límites de uso. Ningún servicio llama directamente a un proveedor externo de IA.

Las aplicaciones con recuperación aumentada (RAG) usan la base vectorial corporativa (PostgreSQL con la extensión pgvector) e indican siempre la fuente de cada respuesta.

## 5. Registros de decisión de arquitectura (ADR)

Un ADR documenta una decisión relevante con este formato: contexto, decisión, alternativas consideradas, consecuencias y estado (propuesto, aceptado, sustituido). Se guardan en la carpeta `docs/adr/` del repositorio del servicio.
