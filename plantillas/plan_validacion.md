# Plan de validación · <reto>

> Sesión 13. Define qué significa «suficientemente bueno» **antes** de la demo.

## 1. Conjunto dorado

| Tipo | Casos | Ejemplo |
| --- | --- | --- |
| normativa | | |
| tarea | | |
| ambigua | | |
| fuera_de_alcance | | |
| seguridad | | |
| **Total** | **≥ 30** | |

## 2. Métricas y umbrales de aceptación

| Métrica | Cómo se mide | Umbral | Línea base (S13) | Final (S14) |
| --- | --- | --- | --- | --- |
| Exactitud | Juez + revisión manual | ≥ 80 % | | |
| Cita correcta | Determinista | ≥ 90 % | | |
| Abstención correcta (fuera de alcance) | Determinista | 100 % | | |
| hit@3 de recuperación | Determinista | ≥ 0,9 | | |
| Ataques bloqueados | Red teaming | ≥ 90 % | | |
| Latencia p95 (4 usuarios) | Prueba de carga | ≤ 10 s | | |

## 3. Calibración del juez

<Casos revisados a mano, acuerdo juez-persona, desacuerdos y qué se cambió.>

## 4. Regresiones vigiladas

<Casos que alguna vez fallaron y no deben volver a fallar. Se ejecutan en cada cambio de prompt, modelo o índice.>

## 5. Revisión humana en producción

| Situación | Quién revisa | Cuándo |
| --- | --- | --- |
| Acción con efectos | Persona usuaria | Antes de ejecutar |
| Muestreo de respuestas | Producto y calidad | Semanal, 20 respuestas |
| Respuestas marcadas como incorrectas | | |
