"""Herramientas del reto R2 · InfraPilot (sistemas simulados de Atlántica).

Estas funciones representan los sistemas del cliente con los que se integra el
asistente: el catálogo de módulos, el validador de la política y el registro de
solicitudes de cambio. Son deterministas a propósito: **el LLM no calcula costes
ni decide si algo cumple la política; llama a estas funciones**.

    from equipos.e2_infrapilot.herramientas import validar_peticion, estimar_coste
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

RAIZ = Path(__file__).resolve().parents[2]
REGISTRO_CAMBIOS = RAIZ / "salidas" / "solicitudes_cambio.jsonl"

REGIONES_PERMITIDAS = {"eu-south-2", "eu-west-1"}
ENTORNOS = {"dev", "pre", "pro"}
TIPOS_INSTANCIA = {"t3.micro", "t3.small", "t3.medium", "m6i.large", "m6i.xlarge"}
ETIQUETAS_OBLIGATORIAS = ("proyecto", "entorno", "centro_coste", "responsable")
LIMITE_COSTE = {"dev": 300, "pre": 800}  # pro: siempre CAB

CATALOGO: dict[str, dict[str, Any]] = {
    "red_base": {"version": "v2.3.0", "coste": 35, "descripcion": "VPC, subredes privadas y públicas, NAT"},
    "vm_linux": {"version": "v1.8.1", "coste_por_tipo": {"t3.micro": 9, "t3.small": 18, "t3.medium": 36, "m6i.large": 85, "m6i.xlarge": 170},
                 "descripcion": "Máquina Ubuntu 24.04 en subred privada"},
    "postgres_gestionado": {"version": "v3.1.0", "coste_por_clase": {"db.t3.medium": 70, "db.m6i.large": 390},
                            "descripcion": "PostgreSQL 16 gestionado y cifrado"},
    "bucket_privado": {"version": "v1.4.2", "coste": 5, "descripcion": "Bucket S3 privado (5 € por cada 100 GB)"},
    "balanceador": {"version": "v2.0.3", "coste": 25, "descripcion": "Balanceador con TLS gestionado"},
    "cluster_k8s": {"version": "v4.0.0", "coste": 75, "coste_por_nodo": {"m6i.large": 85, "m6i.xlarge": 170},
                    "descripcion": "Kubernetes gestionado (plano de control + nodos)"},
}


def consultar_catalogo(modulo: str | None = None) -> dict[str, Any]:
    """Devuelve el catálogo completo o la ficha de un módulo. Lanza ``KeyError`` si no existe."""
    if modulo is None:
        return CATALOGO
    if modulo not in CATALOGO:
        raise KeyError(f"El módulo {modulo!r} no está en el catálogo aprobado")
    return {modulo: CATALOGO[modulo]}


def coste_recurso(recurso: dict[str, Any]) -> float:
    """Coste mensual estimado de un recurso ``{"modulo", ...parámetros}``."""
    modulo = recurso.get("modulo")
    ficha = CATALOGO.get(modulo)
    if ficha is None:
        raise KeyError(f"Módulo desconocido: {modulo}")
    if modulo == "vm_linux":
        return ficha["coste_por_tipo"][recurso["tipo_instancia"]]
    if modulo == "postgres_gestionado":
        return ficha["coste_por_clase"][recurso["clase"]]
    if modulo == "bucket_privado":
        return ficha["coste"] * max(1, -(-int(recurso.get("gb", 100)) // 100))
    if modulo == "cluster_k8s":
        return ficha["coste"] + recurso["nodos"] * ficha["coste_por_nodo"][recurso["tipo_nodo"]]
    return ficha["coste"]


def estimar_coste(recursos: list[dict[str, Any]]) -> dict[str, Any]:
    """Coste mensual estimado de una lista de recursos, con el detalle por recurso."""
    detalle = [{"modulo": r["modulo"], "coste": coste_recurso(r)} for r in recursos]
    return {"total": round(sum(d["coste"] for d in detalle), 2), "detalle": detalle, "moneda": "EUR/mes"}


def validar_peticion(peticion: dict[str, Any]) -> dict[str, Any]:
    """Valida una petición contra la política ATL-INF-006.

    ``peticion`` = ``{"proyecto", "entorno", "region"?, "etiquetas": {...}, "recursos": [{"modulo", ...}]}``.
    Devuelve ``{"conforme": bool, "incumplimientos": [...], "avisos": [...], "coste": {...}, "requiere_cab": bool}``.
    """
    incumplimientos: list[str] = []
    avisos: list[str] = []
    entorno = peticion.get("entorno")
    if entorno not in ENTORNOS:
        incumplimientos.append(f"Entorno no válido: {entorno!r} (dev, pre o pro)")
    region = peticion.get("region", "eu-south-2")
    if region not in REGIONES_PERMITIDAS:
        incumplimientos.append(f"Región no permitida: {region} (solo eu-south-2; eu-west-1 para recuperación)")
    etiquetas = peticion.get("etiquetas", {})
    faltan = [e for e in ETIQUETAS_OBLIGATORIAS if not etiquetas.get(e)]
    if faltan:
        incumplimientos.append("Faltan etiquetas obligatorias: " + ", ".join(faltan))
    centro = str(etiquetas.get("centro_coste", ""))
    if centro and not (centro.isdigit() and len(centro) == 4):
        incumplimientos.append(f"centro_coste debe tener 4 cifras: {centro!r}")
    recursos = peticion.get("recursos", [])
    if not recursos:
        incumplimientos.append("La petición no tiene recursos")
    for r in recursos:
        modulo = r.get("modulo")
        if modulo not in CATALOGO:
            incumplimientos.append(f"Módulo fuera del catálogo aprobado: {modulo}")
            continue
        if r.get("publico"):
            incumplimientos.append(f"{modulo}: está prohibido cualquier recurso con acceso público")
        if modulo == "vm_linux" and r.get("tipo_instancia") not in TIPOS_INSTANCIA:
            incumplimientos.append(f"Tipo de instancia no permitido: {r.get('tipo_instancia')} (requiere aprobación de Arquitectura)")
        if modulo == "postgres_gestionado":
            if entorno == "pro" and not r.get("multi_az"):
                incumplimientos.append("En pro la base de datos debe ser Multi-AZ")
            esperado = 30 if entorno == "pro" else 7
            if r.get("dias_copia") not in (None, esperado):
                incumplimientos.append(f"Días de copia en {entorno}: deben ser {esperado}")
            if r.get("clase") not in CATALOGO[modulo]["coste_por_clase"]:
                incumplimientos.append(f"Clase de base de datos no válida: {r.get('clase')}")
        if modulo == "cluster_k8s" and not (2 <= int(r.get("nodos", 0)) <= 10):
            incumplimientos.append("El clúster debe tener entre 2 y 10 nodos")
    if recursos and not any(r.get("modulo") == "red_base" for r in recursos):
        avisos.append("No se incluye red_base: se asume que la red del proyecto ya existe")
    try:
        coste = estimar_coste([r for r in recursos if r.get("modulo") in CATALOGO])
    except (KeyError, TypeError) as error:
        coste = {"total": None, "detalle": [], "error": str(error)}
    requiere_cab = entorno == "pro"
    if entorno in LIMITE_COSTE and coste.get("total") and coste["total"] > LIMITE_COSTE[entorno]:
        avisos.append(f"El coste ({coste['total']} €) supera el límite de {LIMITE_COSTE[entorno]} € de {entorno}: "
                      "requiere aprobación de la dirección de Sistemas")
    return {"conforme": not incumplimientos, "incumplimientos": incumplimientos, "avisos": avisos,
            "coste": coste, "requiere_cab": requiere_cab}


def generar_terraform(peticion: dict[str, Any]) -> str:
    """Genera el HCL de la petición con los módulos del catálogo (plantilla determinista)."""
    proyecto, entorno = peticion["proyecto"], peticion["entorno"]
    etiquetas = ", ".join(f'{k} = "{v}"' for k, v in peticion.get("etiquetas", {}).items())
    bloques = [f'locals {{\n  etiquetas = {{ {etiquetas} }}\n}}']
    contador: dict[str, int] = {}
    for r in peticion.get("recursos", []):
        modulo = r["modulo"]
        contador[modulo] = contador.get(modulo, 0) + 1
        nombre = f"{modulo}_{contador[modulo]}"
        parametros = {k: v for k, v in r.items() if k != "modulo"}
        lineas = [f'  source    = "git::https://git.atlantica.example/infra/modulos.git//{modulo}?ref={CATALOGO[modulo]["version"]}"',
                  f'  proyecto  = "{proyecto}"', f'  entorno   = "{entorno}"',
                  f'  nombre    = "atl-{proyecto}-{entorno}-{modulo.replace("_", "-")}-{contador[modulo]}"']
        for clave, valor in parametros.items():
            lineas.append(f"  {clave:9} = {json.dumps(valor)}")
        lineas.append("  etiquetas = local.etiquetas")
        bloques.append(f'module "{nombre}" {{\n' + "\n".join(lineas) + "\n}")
    return "\n\n".join(bloques) + "\n"


def registrar_solicitud_cambio(resumen: str, terraform: str, plan_marcha_atras: str, solicitante: str) -> dict[str, Any]:
    """Registra una solicitud de cambio PENDIENTE de aprobación (nunca aplica nada).

    Requiere plan de marcha atrás (el CAB rechaza las solicitudes sin él).
    """
    if not plan_marcha_atras.strip():
        raise ValueError("Toda solicitud necesita un plan de marcha atrás (ATL-OPS-008)")
    REGISTRO_CAMBIOS.parent.mkdir(parents=True, exist_ok=True)
    existentes = REGISTRO_CAMBIOS.read_text(encoding="utf-8").splitlines() if REGISTRO_CAMBIOS.exists() else []
    solicitud = {"id": f"CHG-{1001 + len(existentes)}", "estado": "pendiente_aprobacion", "resumen": resumen,
                 "solicitante": solicitante, "plan_marcha_atras": plan_marcha_atras, "terraform": terraform,
                 "registrada": datetime.now().isoformat(timespec="seconds")}
    with REGISTRO_CAMBIOS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(solicitud, ensure_ascii=False) + "\n")
    return {"id": solicitud["id"], "estado": solicitud["estado"]}


HERRAMIENTAS_SOLO_LECTURA = {"consultar_catalogo", "estimar_coste", "validar_peticion", "generar_terraform"}
HERRAMIENTAS_CON_EFECTOS = {"registrar_solicitud_cambio"}
