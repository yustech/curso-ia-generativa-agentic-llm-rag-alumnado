# Código heredado: módulo `tarifas`

Fragmento del sistema Faro que calcula el precio de un envío. Es código real de producción (en la ficción del curso): funciona, pero incumple casi todos los puntos de la Guía de estilo de Python (ATL-DES-004) y no tiene pruebas.

Es la materia prima del **Reto 1 (DevAssist)**: el asistente del Equipo 1 debe ser capaz de explicar el código, detectar los incumplimientos de la guía, proponer pruebas unitarias y una refactorización segura.

## Reglas de negocio (documentadas por el equipo de Faro)

1. El precio base es `precio por km del vehículo × km`. Precios por km: furgoneta 0,62 €, rígido 0,95 €, tráiler 1,38 €, frigorífico 1,62 €.
2. Si la carga supera 1.000 kg, se suma `(kg − 1000) × 0,02 × km / 100`.
3. El precio mínimo por servicio es de 45 € (se aplica antes del recargo de combustible).
4. Recargo de combustible: 7,5 % sobre el precio anterior.
5. Servicio urgente: +25 %.
6. Descuento por nivel de cliente sobre el total: oro 12 %, plata 8 %, bronce 4 %.
7. El resultado se redondea a 2 decimales.

Comprueba el comportamiento actual:

```bash
cd datos/atlantica/codigo
python -c "from tarifas.calculo import calc; print(calc('rigido', 120, 1500, 'Nortia', urgente=True))"
```
