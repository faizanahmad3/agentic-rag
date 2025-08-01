from qdrant_client import QdrantClient
from src.utils.config import Config
from llama_index.core import Document

client = QdrantClient(
    url=Config.QDRANT_HOST,
    api_key=Config.QDRANT_API_KEY
)


from qdrant_client.http.exceptions import UnexpectedResponse

def fetch_documents_from_qdrant(collection_name="rag_collection"):
    # Check if collection exists
    collections = client.get_collections()
    collection_names = [c.name for c in collections.collections]

    if collection_name not in collection_names:
        return []  # No collection yet

    documents = []
    offset = None

    while True:
        points, next_page_offset = client.scroll(
            collection_name=collection_name,
            limit=100,
            offset=offset
        )

        if not points:
            break

        for point in points:
            payload = point.payload or {}
            text = payload.get("text") or payload.get("page_content") or ""
            metadata = payload.get("metadata") or payload.get("extra_info") or {}

            documents.append(Document(text=text, metadata=metadata))

        if next_page_offset is None:
            break
        offset = next_page_offset

    return documents

fetch_documents_from_qdrant()