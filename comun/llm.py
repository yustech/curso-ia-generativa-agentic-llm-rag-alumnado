"""Cliente LLM común del curso.

Todo el curso habla con un servidor compatible con la API de OpenAI. Cambiar de
motor (Ollama, LM Studio, vLLM o Colibri) consiste en cambiar la URL del fichero
``.env``; el código de los laboratorios no cambia.

Funciones principales:

- ``chat(...)``: envía mensajes y devuelve el texto de la respuesta.
- ``chat_completo(...)``: igual, pero devuelve la respuesta completa (para tool calling).
- ``estructurado(...)``: devuelve un objeto Pydantic validado (JSON Schema).
- ``embeddings(...)``: devuelve los vectores de una lista de textos.
- ``ultima_llamada``: métricas de la última llamada (tokens, segundos, modelo).

Para los tests existe ``LLMFalso``: un sustituto determinista que no necesita
ningún servidor. Se activa con ``usar_llm_falso(...)``.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence, TypeVar

from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")

URL_BASE = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
CLAVE_API = os.getenv("LLM_API_KEY", "ollama")
MODELO_CHAT = os.getenv("CHAT_MODEL", "granite4:micro")
MODELO_EMBEDDINGS = os.getenv("EMBED_MODEL", "embeddinggemma")
TIEMPO_MAXIMO = float(os.getenv("LLM_TIMEOUT", "120"))

M = TypeVar("M", bound=BaseModel)
Mensajes = Sequence[dict[str, Any]]


@dataclass
class Metricas:
    """Datos de la última llamada al modelo."""

    modelo: str = ""
    segundos: float = 0.0
    tokens_entrada: int = 0
    tokens_salida: int = 0

    @property
    def tokens_por_segundo(self) -> float:
        return self.tokens_salida / self.segundos if self.segundos else 0.0


ultima_llamada = Metricas()
_cliente = None
_falso: "LLMFalso | None" = None


# ---------------------------------------------------------------- cliente real
def cliente():
    """Devuelve (y reutiliza) el cliente OpenAI apuntando al servidor configurado."""
    global _cliente
    if _cliente is None:
        from openai import OpenAI

        _cliente = OpenAI(base_url=URL_BASE, api_key=CLAVE_API, timeout=TIEMPO_MAXIMO)
    return _cliente


def como_mensajes(entrada: str | Mensajes, sistema: str | None = None) -> list[dict[str, Any]]:
    """Convierte un texto (o una lista de mensajes) en la lista que espera la API."""
    if isinstance(entrada, str):
        mensajes: list[dict[str, Any]] = [{"role": "user", "content": entrada}]
    else:
        mensajes = [dict(m) for m in entrada]
    if sistema:
        mensajes.insert(0, {"role": "system", "content": sistema})
    return mensajes


def _registrar(respuesta: Any, modelo: str, inicio: float) -> None:
    ultima_llamada.modelo = modelo
    ultima_llamada.segundos = time.perf_counter() - inicio
    uso = getattr(respuesta, "usage", None)
    ultima_llamada.tokens_entrada = getattr(uso, "prompt_tokens", 0) or 0
    ultima_llamada.tokens_salida = getattr(uso, "completion_tokens", 0) or 0


def chat_completo(
    entrada: str | Mensajes,
    *,
    sistema: str | None = None,
    modelo: str | None = None,
    temperatura: float = 0.2,
    max_tokens: int | None = None,
    herramientas: list[dict[str, Any]] | None = None,
    formato: dict[str, Any] | None = None,
    **extra: Any,
) -> Any:
    """Llama al modelo y devuelve la respuesta completa de la API."""
    modelo = modelo or MODELO_CHAT
    if _falso is not None:
        inicio = time.perf_counter()
        respuesta = _falso.responder(como_mensajes(entrada, sistema), herramientas=herramientas, formato=formato)
        _registrar(respuesta, modelo, inicio)
        return respuesta
    parametros: dict[str, Any] = {
        "model": modelo,
        "messages": como_mensajes(entrada, sistema),
        "temperature": temperatura,
    }
    if max_tokens:
        parametros["max_tokens"] = max_tokens
    if herramientas:
        parametros["tools"] = herramientas
    if formato:
        parametros["response_format"] = formato
    parametros.update(extra)
    inicio = time.perf_counter()
    respuesta = cliente().chat.completions.create(**parametros)
    _registrar(respuesta, modelo, inicio)
    return respuesta


def chat(entrada: str | Mensajes, **opciones: Any) -> str:
    """Envía un mensaje y devuelve solo el texto de la respuesta."""
    respuesta = chat_completo(entrada, **opciones)
    return (respuesta.choices[0].message.content or "").strip()


def esquema_de(modelo_pydantic: type[BaseModel]) -> dict[str, Any]:
    """Formato ``response_format`` (JSON Schema) a partir de un modelo Pydantic."""
    return {
        "type": "json_schema",
        "json_schema": {"name": modelo_pydantic.__name__, "schema": modelo_pydantic.model_json_schema()},
    }


def extraer_json(texto: str) -> Any:
    """Extrae el primer objeto JSON de un texto (tolera bloques ```json)."""
    texto = texto.strip()
    if texto.startswith("```"):
        texto = texto.strip("`")
        texto = texto[texto.find("\n") + 1 :] if "\n" in texto else texto
    inicio = min([i for i in (texto.find("{"), texto.find("[")) if i >= 0], default=-1)
    if inicio < 0:
        raise ValueError("La respuesta no contiene JSON")
    return json.loads(texto[inicio : max(texto.rfind("}"), texto.rfind("]")) + 1])


def estructurado(
    entrada: str | Mensajes,
    modelo_pydantic: type[M],
    *,
    reintentos: int = 2,
    **opciones: Any,
) -> M:
    """Pide al modelo una salida que cumpla un esquema y la devuelve validada.

    Si la salida no valida, se reintenta enviando el error al modelo, que es la
    técnica estándar de "validar y reintentar".
    """
    mensajes = como_mensajes(entrada, opciones.pop("sistema", None))
    ultimo_error: Exception | None = None
    for _ in range(reintentos + 1):
        texto = chat(mensajes, formato=esquema_de(modelo_pydantic), temperatura=opciones.pop("temperatura", 0.0), **opciones)
        try:
            return modelo_pydantic.model_validate(extraer_json(texto))
        except (ValueError, ValidationError) as error:
            ultimo_error = error
            mensajes = mensajes + [
                {"role": "assistant", "content": texto},
                {"role": "user", "content": f"La respuesta no es válida: {error}. Devuelve solo el JSON corregido."},
            ]
    raise ValueError(f"El modelo no devolvió un JSON válido tras {reintentos + 1} intentos: {ultimo_error}")


def embeddings(textos: str | Iterable[str], modelo: str | None = None, lote: int = 32) -> list[list[float]]:
    """Devuelve un vector por texto. Procesa por lotes para no saturar el servidor."""
    if isinstance(textos, str):
        textos = [textos]
    textos = list(textos)
    if _falso is not None:
        return [_falso.vector(t) for t in textos]
    modelo = modelo or MODELO_EMBEDDINGS
    vectores: list[list[float]] = []
    for i in range(0, len(textos), lote):
        respuesta = cliente().embeddings.create(model=modelo, input=textos[i : i + lote])
        vectores.extend(d.embedding for d in respuesta.data)
    return vectores


def modelos_disponibles() -> list[str]:
    """Lista los modelos que ofrece el servidor configurado."""
    return sorted(m.id for m in cliente().models.list().data)


# ---------------------------------------------------------------- LLM falso (tests)
@dataclass
class _Funcion:
    name: str
    arguments: str


@dataclass
class _LlamadaHerramienta:
    id: str
    function: _Funcion
    type: str = "function"


@dataclass
class _Mensaje:
    content: str | None
    tool_calls: list[_LlamadaHerramienta] | None = None
    role: str = "assistant"

    def model_dump(self, **_: Any) -> dict[str, Any]:
        datos: dict[str, Any] = {"role": self.role, "content": self.content}
        if self.tool_calls:
            datos["tool_calls"] = [
                {"id": t.id, "type": "function", "function": {"name": t.function.name, "arguments": t.function.arguments}}
                for t in self.tool_calls
            ]
        return datos


@dataclass
class _Opcion:
    message: _Mensaje
    finish_reason: str = "stop"


@dataclass
class _Uso:
    prompt_tokens: int = 0
    completion_tokens: int = 0


@dataclass
class _Respuesta:
    choices: list[_Opcion]
    usage: Any = None


@dataclass
class LLMFalso:
    """Sustituto determinista del modelo para los tests.

    ``respuestas`` es una lista que se consume en orden. Cada elemento puede ser:

    - un texto: el modelo responde ese texto;
    - un dict ``{"herramienta": nombre, "argumentos": {...}}``: el modelo pide
      llamar a una herramienta;
    - una función ``f(mensajes) -> texto | dict``: respuesta calculada.

    Si se agotan las respuestas se devuelve ``por_defecto``.
    """

    respuestas: list[Any] = field(default_factory=list)
    por_defecto: str = "Respuesta simulada."
    recibidos: list[list[dict[str, Any]]] = field(default_factory=list)

    def responder(self, mensajes: list[dict[str, Any]], **_: Any) -> _Respuesta:
        self.recibidos.append(mensajes)
        salida = self.respuestas.pop(0) if self.respuestas else self.por_defecto
        if callable(salida):
            salida = salida(mensajes)
        entrada = sum(len(str(m.get("content") or "").split()) for m in mensajes)
        if isinstance(salida, dict) and "herramienta" in salida:
            llamada = _LlamadaHerramienta(
                id=f"llamada_{len(self.recibidos)}",
                function=_Funcion(salida["herramienta"], json.dumps(salida.get("argumentos", {}), ensure_ascii=False)),
            )
            return _Respuesta([_Opcion(_Mensaje(None, [llamada]), "tool_calls")], _Uso(entrada, 10))
        if not isinstance(salida, str):
            salida = json.dumps(salida, ensure_ascii=False)
        return _Respuesta([_Opcion(_Mensaje(salida))], _Uso(entrada, len(salida.split())))

    @staticmethod
    def vector(texto: str, dimension: int = 64) -> list[float]:
        """Vector determinista basado en las palabras del texto (bolsa de palabras con hash)."""
        import hashlib
        import math

        vector = [0.0] * dimension
        for palabra in texto.lower().split():
            palabra = palabra.strip(".,;:¿?¡!()\"'")
            if not palabra:
                continue
            indice = int(hashlib.md5(palabra.encode()).hexdigest(), 16) % dimension
            vector[indice] += 1.0
        norma = math.sqrt(sum(v * v for v in vector)) or 1.0
        return [v / norma for v in vector]


def usar_llm_falso(respuestas: list[Any] | None = None, **opciones: Any) -> LLMFalso:
    """Activa el LLM falso (lo usan los tests) y lo devuelve."""
    global _falso
    _falso = LLMFalso(list(respuestas or []), **opciones)
    return _falso


def es_falso() -> bool:
    """Indica si está activo el LLM falso (para no mezclar cachés de embeddings reales y simulados)."""
    return _falso is not None


def usar_llm_real() -> None:
    """Vuelve a usar el servidor real."""
    global _falso
    _falso = None


def describir_configuracion() -> str:
    return f"Servidor: {URL_BASE} · modelo de chat: {MODELO_CHAT} · modelo de embeddings: {MODELO_EMBEDDINGS}"


AccionHerramienta = Callable[..., Any]
