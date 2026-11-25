# Sesión 14. Ejercicio

Completa el fichero sustituyendo los `raise NotImplementedError` por tu código. Comprueba tu trabajo con:

```bash
pytest sesion_14_proyecto_final -v
```

## Ejercicio 1. Verificador de la entrega (en la finalización, 20 min)

Fichero: `s14_ej1_verificar_entrega.py`

Un pequeño programa que revisa automáticamente si el repositorio de tu equipo cumple los requisitos de entrega. Es el tipo de comprobación que se pone en un pipeline de integración continua.

1. `comprobar_documentos(raiz)`: los seis documentos existen y no están vacíos.
2. `comprobar_golden(raiz, minimo)`: 30 o más casos válidos y los cinco tipos.
3. `contar_pruebas(raiz)`: cuenta funciones `test_*` con `ast`, sin ejecutarlas.
4. `buscar_secretos(raiz)`: ni `.env` ni patrones de claves en el código.
5. `verificar(raiz)` e `informe(filas)`.

Ejecútalo sobre el repositorio de tu equipo antes de etiquetar la `v1.0`:

```bash
python sesion_14_proyecto_final/ejercicios/s14_ej1_verificar_entrega.py ../repositorio-del-equipo
```

## Práctica de equipo

La práctica de hoy es el proyecto final: [`PRACTICA_14.md`](PRACTICA_14.md).
