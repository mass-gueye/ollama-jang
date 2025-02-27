__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain_community.chat_models import ChatOllama
from utils.data_loader import load_documents
from embeddings.embedder import create_embeddings
from retrievers.retriever import create_retriever
from prompts.prompt_handler import before_rag, after_rag

from configs.config import URLs, MODEL_NAME, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL

model_local = ChatOllama(model=MODEL_NAME)

# 1. Charger et diviser les documents
docs_list = load_documents(URLs)
doc_splits = create_embeddings(docs_list, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL)

# 2. Créer le retriever
retriever = create_retriever(doc_splits, EMBEDDING_MODEL)

# 3. Question avant RAG
print("Before RAG\n")
print(before_rag(model_local, "Ollama"))

# 4. Question après RAG
print("\n########\nAfter RAG\n")
print(after_rag(retriever, model_local, "What is Ollama?"))
