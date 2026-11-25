# Sesión 12. Laboratorio guiado

Completa cada fichero sustituyendo los `raise NotImplementedError` por tu código. Comprueba tu trabajo con:

```bash
pytest sesion_12_documentacion -v
```

## Ejercicio 1. De las actas a JSON validado (laboratorio, 70 min)

Fichero: `s12_ej1_extraccion.py`

1. `normalizar_fecha(texto, anio)`: convierte los cuatro formatos que aparecen en las actas. Es determinista a propósito: el modelo copia la fecha y el código la normaliza.
2. `extraer_acta(texto)`: una llamada a `llm.estructurado` y la normalización de las fechas.
3. `aparece(nombre, texto)`: las actas usan nombres completos o solo el nombre de pila.
4. `problemas_trazabilidad(acta, texto)`.

Ejecuta el fichero con las cuatro actas reales. Fíjate en el acta del 24 de noviembre: está escrita en prosa, sin apartados. ¿Extrae bien las acciones? ¿Detecta la trazabilidad algún problema?

## Ejercicio 2. Generación documental controlada (Reto 1, 35 min)

Fichero: `s12_ej2_generacion.py`

1. `semaforo(desviacion, hito_en_peligro)` y `semaforo_general(datos)`.
2. `generar_informe(datos, resumen)`: la plantilla de la metodología de Atlántica. Todas las cifras y reglas las pone el código; el LLM solo aporta el resumen (`resumen_con_llm`, ya hecha).

Ejecuta el fichero y compara el resultado con `datos/atlantica/proyectos/informe_estado_2026-11-20.md`.

## Ejercicio 3. Validación del documento (Reto 1 y 2, 35 min)

Fichero: `s12_ej3_validacion.py`

1. `comprobaciones(informe, completados, comprometidos)`: las cuatro comprobaciones deterministas.
2. `juzgar(informe, datos_origen, rubrica)`: LLM como juez con salida estructurada.
3. `muestra_revision(elementos, porcentaje, semilla, minimo)`.
4. `informe_validacion(nombre, filas, juicio)`.

Ejecuta el fichero. Después estropea a propósito el informe (cambia una cifra del resumen o borra una sección) y comprueba qué capa lo detecta.

Ejemplos complementarios: `ejemplos/01_resumen_map_reduce.py` y `ejemplos/02_docstrings.py`.

## Práctica de equipo

El enunciado está en [`PRACTICA_12.md`](PRACTICA_12.md).
