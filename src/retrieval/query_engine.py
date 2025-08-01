from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
from src.utils.config import Config
import src.utils.llm_setup  # ensures Settings is configured
from llama_index.core.tools import QueryEngineTool
from llama_index.core import SummaryIndex
from src.tools.qdrant_helper import client


def get_query_engine(collection_name="rag_collection"):
    """
    Create a query engine connected to Qdrant.
    """

    # Use Qdrant as Vector Store
    vector_store = QdrantVectorStore(client=client, collection_name=collection_name)

    # Storage context
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Load index from storage
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        storage_context=storage_context
    )

    # Create query engine
    query_engine = index.as_query_engine(
        similarity_top_k=3,  # retrieve top 3 chunks
        response_mode="compact"  # concise answers
    )

    return query_engine

def query_with_citations(question, collection_name="rag_collection"):
    """
    Query Qdrant and return answer with citations.
    """
    query_engine = get_query_engine(collection_name)
    response = query_engine.query(question)

    # Extract sources (file name + page number)
    sources = []
    for node in response.source_nodes:
        meta = node.metadata
        file_name = meta.get("file_name", "Unknown File")
        page_num = meta.get("page_number", "N/A")
        sources.append(f"{file_name} (Page {page_num})")

    # Remove duplicates
    sources = list(set(sources))

    # If no sources, mark as "No answer found"
    if not sources or not response.response.strip():
        return "No answer found", []

    return response.response, sources

def get_retrieval_tool(collection_name="rag_collection"):
    """
    Wrap Qdrant retrieval as a tool for agent.
    """
    vector_store = QdrantVectorStore(client=client, collection_name=collection_name)

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)

    query_engine = index.as_query_engine(similarity_top_k=3, response_mode="compact")

    # Wrap as Tool
    retrieval_tool = QueryEngineTool.from_defaults(
        query_engine=query_engine,
        name="DocumentSearch",
        description="Search and retrieve information from uploaded documents"
    )
    return retrieval_tool

def get_summarizer_tool(documents):
    """
    Creates a summarizer tool that summarizes all documents.
    """
    # Build summary index
    summary_index = SummaryIndex(documents)

    # Convert to query engine
    query_engine = summary_index.as_query_engine(response_mode="tree_summarize",
                                                 text_qa_template="Summarize clearly and highlight key points:\n\n{context_str}")

    return query_engine