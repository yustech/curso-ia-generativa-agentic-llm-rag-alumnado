"""Sesión 2 - Ejercicio 1: matriz de riesgos y controles."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Categoria = Literal["privacidad", "sesgo", "seguridad", "alucinacion", "autonomia", "propiedad_intelectual",
                    "transparencia", "cumplimiento", "operacional"]


class Riesgo(BaseModel):
    """Un riesgo de un caso de uso de IA."""

    id: str
    descripcion: str
    categoria: Categoria
    probabilidad: int = Field(ge=1, le=5)
    impacto: int = Field(ge=1, le=5)
    controles: list[str] = Field(default_factory=list)


def exposicion(riesgo: Riesgo) -> int:
    """Probabilidad × impacto (de 1 a 25)."""
    raise NotImplementedError("Completa este bloque")


def nivel(valor_exposicion: int) -> str:
    """Nivel según la metodología de Atlántica: «bajo» hasta 6, «medio» de 7 a 14, «alto» desde 15."""
    raise NotImplementedError("Completa este bloque")


def ordenar(riesgos: list[Riesgo]) -> list[Riesgo]:
    """Devuelve los riesgos de mayor a menor exposición; a igual exposición, por id."""
    raise NotImplementedError("Completa este bloque")


def sin_control(riesgos: list[Riesgo]) -> list[str]:
    """Ids de los riesgos de nivel medio o alto que no tienen ningún control."""
    raise NotImplementedError("Completa este bloque")


def a_markdown(riesgos: list[Riesgo]) -> str:
    """Tabla Markdown ordenada por exposición.

    Columnas: | Id | Riesgo | Categoría | P | I | Exposición | Nivel | Controles |
    Los controles se separan con «; ». Si no hay, se escribe «(ninguno)».
    """
    raise NotImplementedError("Completa este bloque")


def riesgos_ejemplo() -> list[Riesgo]:
    """Matriz de ejemplo: chatbot de seguimiento de envíos para tiendas de clientes."""
    return [
        Riesgo(id="R1", descripcion="El chatbot inventa una hora de llegada o una compensación", categoria="alucinacion",
               probabilidad=4, impacto=4, controles=["Responder solo con datos de Faro", "Plantilla de respuesta para compensaciones"]),
        Riesgo(id="R2", descripcion="Muestra la matrícula o el nombre del conductor", categoria="privacidad",
               probabilidad=2, impacto=4, controles=["Filtrar campos personales antes de enviarlos al modelo"]),
        Riesgo(id="R3", descripcion="La tienda no sabe que habla con una IA", categoria="transparencia",
               probabilidad=3, impacto=2, controles=["Mensaje de bienvenida que indica que es un asistente de IA"]),
        Riesgo(id="R4", descripcion="Un usuario logra que revele datos de otras tiendas", categoria="seguridad",
               probabilidad=2, impacto=5, controles=[]),
    ]


if __name__ == "__main__":
    print(a_markdown(riesgos_ejemplo()))
    print("\nRiesgos medios o altos sin control:", sin_control(riesgos_ejemplo()))
