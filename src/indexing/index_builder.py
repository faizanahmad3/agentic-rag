from llama_index.core import Document, VectorStoreIndex, StorageContext, ServiceContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from src.utils.config import Config
import src.utils.llm_setup

def build_qdrant_index(pages_data, collection_name="rag_collection"):
    """
    Build Qdrant-backed LlamaIndex using OpenAI embeddings.
    """
    # Convert pages to LlamaIndex Documents
    documents = []
    for page in pages_data:
        metadata = {
            "file_name": page["file_name"],
            "page_number": page["page_number"]
        }
        documents.append(Document(text=page["text"], metadata=metadata))

    # Connect to Qdrant
    client = QdrantClient(host=Config.QDRANT_HOST, port=Config.QDRANT_PORT)

    # Create Qdrant Vector Store
    vector_store = QdrantVectorStore(client=client, collection_name=collection_name)

    # Storage Context
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Build index
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context)

    return index
