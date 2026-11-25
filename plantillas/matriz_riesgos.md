# Matriz de riesgos · <reto>

> Sesión 2 (se actualiza en las sesiones 8, 13 y 14). Probabilidad e impacto de 1 a 5; exposición = probabilidad × impacto. Con 15 o más se escala (metodología de Atlántica).

| ID | Riesgo | Categoría | Prob. | Impacto | Exposición | Control | Responsable | Estado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | Respuesta inventada presentada como cierta | Alucinación | | | | RAG + citas + abstención | | |
| R2 | Instrucción oculta en un documento recuperado | Inyección indirecta (OWASP LLM01) | | | | | | |
| R3 | Datos personales en prompts o trazas | Privacidad (RGPD) | | | | | | |
| R4 | Acción con efectos sin supervisión | Agencia excesiva (OWASP LLM06) | | | | Confirmación humana | | |
| R5 | Sesgo o lenguaje inadecuado | Uso responsable | | | | | | |
| R6 | Dependencia de un modelo o proveedor | Operación | | | | | | |
| R7 | Latencia inaceptable con varios usuarios | Rendimiento | | | | | | |

Categorías de referencia: OWASP Top 10 for LLM Applications 2025, Reglamento Europeo de IA, RGPD.
