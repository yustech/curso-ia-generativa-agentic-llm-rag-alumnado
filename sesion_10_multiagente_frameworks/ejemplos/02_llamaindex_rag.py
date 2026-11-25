"""Ejemplo 2: el RAG de la sesión 5 en diez líneas con LlamaIndex.

    python sesion_10_multiagente_frameworks/ejemplos/02_llamaindex_rag.py
"""

import sys
from pathlib import Path

from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai_like import OpenAILike

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from comun import llm  # noqa: E402
from comun.documentos import CARPETA_DOCUMENTOS  # noqa: E402

Settings.llm = OpenAILike(model=llm.MODELO_CHAT, api_base=llm.URL_BASE, api_key=llm.CLAVE_API,
                          is_chat_model=True, context_window=8192, temperature=0)
Settings.embed_model = OpenAIEmbedding(model_name=llm.MODELO_EMBEDDINGS, api_base=llm.URL_BASE, api_key=llm.CLAVE_API)

documentos = SimpleDirectoryReader(str(CARPETA_DOCUMENTOS)).load_data()
indice = VectorStoreIndex.from_documents(documentos, transformations=[MarkdownNodeParser()])
motor = indice.as_query_engine(similarity_top_k=3)

respuesta = motor.query("¿Cuáles son las ventanas de cambio en producción?")
print(respuesta.response, "\n")
for fuente in respuesta.source_nodes:
    print(f"{fuente.score:.3f}  {fuente.node.metadata.get('file_name')}  {fuente.node.get_content()[:70]!r}")
