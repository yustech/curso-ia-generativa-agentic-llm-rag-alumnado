"""Agente ReAct de referencia (equivalente a tu ejercicio 1 de la sesión 8).

Acepta un ``ejecutor(nombre, argumentos_json) -> str`` para que puedas enchufar
cualquier forma de ejecutar herramientas: un diccionario de funciones, un
registro con validación (sesión 9) o un cliente MCP (sesión 10).
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any, Callable

from comun import llm
from comun.herramientas import ejecutar_herramienta
from comun.trazas import Traza

Ejecutor = Callable[[str, str], str]


@dataclass
class Resultado:
    respuesta: str
    terminado: bool
    motivo: str
    pasos: list[dict] = field(default_factory=list)
    llamadas_modelo: int = 0
    segundos: float = 0.0


def ejecutor_de(registro: dict[str, Callable[..., Any]]) -> Ejecutor:
    return lambda nombre, argumentos: ejecutar_herramienta(nombre, argumentos, registro)


class AgenteReAct:
    def __init__(self, ejecutor: Ejecutor | dict[str, Callable[..., Any]], herramientas: list[dict], sistema: str,
                 max_pasos: int = 6, max_repeticiones: int = 2, nombre_traza: str = "agente",
                 autorizar: Callable[[str, str], tuple[bool, str]] | None = None) -> None:
        self.ejecutor = ejecutor_de(ejecutor) if isinstance(ejecutor, dict) else ejecutor
        self.herramientas, self.sistema = herramientas, sistema
        self.max_pasos, self.max_repeticiones = max_pasos, max_repeticiones
        self.autorizar = autorizar
        self.traza = Traza(nombre_traza)

    @staticmethod
    def clave_llamada(nombre: str, argumentos: str) -> str:
        try:
            argumentos = json.dumps(json.loads(argumentos or "{}"), sort_keys=True, ensure_ascii=False)
        except json.JSONDecodeError:
            pass
        return f"{nombre}:{argumentos}"

    def ejecutar(self, objetivo: str | list[dict[str, Any]]) -> Resultado:
        inicio = time.perf_counter()
        self.traza.registrar("inicio", objetivo=objetivo if isinstance(objetivo, str) else objetivo[-1].get("content"))
        mensajes = llm.como_mensajes(objetivo, self.sistema)
        resultado = Resultado("", False, "max_pasos")
        vistas: dict[str, int] = {}
        for _ in range(self.max_pasos):
            mensaje = llm.chat_completo(mensajes, herramientas=self.herramientas or None, temperatura=0).choices[0].message
            resultado.llamadas_modelo += 1
            llamadas = mensaje.tool_calls or []
            self.traza.registrar("modelo", herramientas=[c.function.name for c in llamadas])
            if not llamadas:
                resultado.respuesta, resultado.terminado, resultado.motivo = (mensaje.content or "").strip(), True, "respuesta"
                break
            mensajes.append(mensaje.model_dump(exclude_none=True))
            for llamada in llamadas:
                nombre, argumentos = llamada.function.name, llamada.function.arguments
                clave = self.clave_llamada(nombre, argumentos)
                if vistas.get(clave, 0) >= self.max_repeticiones:
                    resultado.motivo, resultado.respuesta = "bucle", "He detenido la tarea: el agente repetía la misma acción."
                    self.traza.registrar("fin", motivo="bucle")
                    resultado.segundos = time.perf_counter() - inicio
                    return resultado
                vistas[clave] = vistas.get(clave, 0) + 1
                if self.autorizar:
                    permitido, motivo = self.autorizar(nombre, argumentos)
                    salida = self.ejecutor(nombre, argumentos) if permitido else f"ERROR: acción no autorizada ({motivo})"
                else:
                    salida = self.ejecutor(nombre, argumentos)
                mensajes.append({"role": "tool", "tool_call_id": llamada.id, "content": salida})
                paso = {"herramienta": nombre, "argumentos": argumentos, "resultado": salida}
                resultado.pasos.append(paso)
                self.traza.registrar("herramienta", **paso)
        if resultado.motivo == "max_pasos":
            resultado.respuesta = "No he podido completar la tarea en el número máximo de pasos."
        self.traza.registrar("fin", motivo=resultado.motivo)
        resultado.segundos = time.perf_counter() - inicio
        return resultado
