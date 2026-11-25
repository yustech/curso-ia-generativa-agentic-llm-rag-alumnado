# Equipos y retos

Doce personas en **tres equipos de cuatro**. Cada equipo trabaja un reto durante todo el curso, sobre los datos de Atlántica Logística (ficticios).

| Equipo | Reto | Ámbito | Herramientas preparadas |
| --- | --- | --- | --- |
| Equipo 1 | **R1 · DevAssist** | Desarrollo de software | [`e1_devassist/herramientas.py`](e1_devassist/herramientas.py) |
| Equipo 2 | **R2 · InfraPilot** | Infraestructura como código | [`e2_infrapilot/herramientas.py`](e2_infrapilot/herramientas.py) |
| Equipo 3 | **R3 · PMO Copilot** | Gestión de proyectos TI | [`e3_pmo_copilot/herramientas.py`](e3_pmo_copilot/herramientas.py) |

## Roles (rotan en cada hito)

| Rol | Responsabilidades |
| --- | --- |
| Producto y calidad | Representa al cliente, prioriza el backlog, mantiene la ficha del reto, el conjunto dorado y las métricas |
| Ingeniería de IA | Prompts, selección de modelo y parámetros, análisis de errores del modelo |
| Ingeniería de conocimiento | Ingesta, RAG y calidad de la recuperación |
| Ingeniería de integración | Herramientas, servidores MCP, orquestación, interfaz y despliegue |

## Los retos

### R1 · DevAssist

Asistente para el equipo de Desarrollo de Atlántica que responde dudas sobre la guía de estilo (`04_guia_estilo_python.md`) y la arquitectura de referencia, revisa código contra la guía y propone pruebas unitarias. Materia prima: el módulo heredado `datos/atlantica/codigo/tarifas/`. Herramientas: leer ficheros del repositorio (solo lectura), comprobar el estilo de forma determinista, ejecutar pruebas en un directorio aislado y ejecutar el cálculo de tarifas actual.

### R2 · InfraPilot

Asistente para el equipo de Plataforma que recibe peticiones de entornos en lenguaje natural, recoge los datos que faltan, propone los recursos del catálogo aprobado, valida la propuesta contra la política de infraestructura, estima el coste, genera el Terraform y registra la solicitud de cambio **para que una persona la apruebe**. Nunca aplica cambios. Peticiones de ejemplo en `datos/atlantica/infra/peticiones.jsonl`.

### R3 · PMO Copilot

Asistente para la Oficina de Proyectos que convierte las actas de reunión en acciones e historias de usuario conformes a la metodología, mantiene el backlog (con confirmación humana para los cambios), detecta riesgos a escalar y redacta el informe de estado semanal con sus fuentes. Datos: `datos/atlantica/proyectos/`. La API simulada del backlog se arranca con `python -m comun.api_backlog`.

## Crear el repositorio del equipo

1. Copiad la carpeta `equipos/plantilla_proyecto/` fuera de este repositorio y renombradla (`asistente-devassist`, `asistente-infrapilot` o `asistente-pmo-copilot`).
2. Inicializad Git y subidlo a un repositorio del equipo en GitHub o GitLab. Dad acceso al docente.
3. El repositorio del curso se usa como biblioteca: en el `.env` del equipo, `CURSO_RAIZ` apunta a la carpeta del repositorio del curso para poder importar `comun` y las herramientas del reto (ver el README de la plantilla).

## Las herramientas del reto

Los ficheros `herramientas.py` representan los **sistemas del cliente**: ya están programados y probados (`pytest equipos`). Vuestro trabajo es integrarlos en el asistente con contratos, validación y permisos (sesión 9), no reescribirlos. Fijaos en que son deterministas: el LLM no calcula costes ni decide si algo cumple la política, sino que llama a estas funciones.
