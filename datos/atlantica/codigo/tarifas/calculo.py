# Modulo de calculo de tarifas de transporte (Faro, version 2019)
# OJO: codigo heredado. Funciona en produccion pero no tiene tests.
from tarifas.descuentos import *

PRECIOS_KM = {"furgoneta": 0.62, "rigido": 0.95, "trailer": 1.38, "frigorifico": 1.62}
RECARGO_COMBUSTIBLE = 7.5   # porcentaje


def calc(tipo, km, kg, cliente=None, urgente=False):
    # calcula el precio de un envio
    if tipo not in PRECIOS_KM:
        print("tipo de vehiculo no valido: " + tipo)
        return None
    if km <= 0:
        print("km incorrectos")
        return None
    p = PRECIOS_KM[tipo] * km
    # recargo por peso: a partir de 1000 kg, 0.02 por kg adicional y km
    if kg > 1000:
        p = p + (kg - 1000) * 0.02 * km / 100
    # minimo por servicio
    if p < 45:
        p = 45
    p = p + p * RECARGO_COMBUSTIBLE / 100
    if urgente == True:
        p = p * 1.25
    if cliente != None:
        d = descuento_cliente(cliente)
        p = p - p * d
    return round(p, 2)


def calc_iva(precio):
    return round(precio * 1.21, 2)


def tabla(tipo, kms):
    res = []
    for k in kms:
        res.append((k, calc(tipo, k, 500)))
    return res
