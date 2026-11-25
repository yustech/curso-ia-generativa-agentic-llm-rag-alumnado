# descuentos por cliente
CLIENTES = {
    "nortia": "oro",
    "frescamar": "plata",
    "hogarplus": "bronce",
}
DESCUENTOS = {"oro": 0.12, "plata": 0.08, "bronce": 0.04}


def descuento_cliente(c):
    try:
        nivel = CLIENTES[c.lower()]
        return DESCUENTOS[nivel]
    except:
        return 0
