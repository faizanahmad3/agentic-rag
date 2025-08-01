from llama_index.agent.openai import OpenAIAgent
from src.retrieval.query_engine import get_retrieval_tool
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
from src.retrieval.query_engine import get_summarizer_tool
from src.tools.qdrant_helper import fetch_documents_from_qdrant, client
from llama_index.core.tools import QueryEngineTool


def create_agent(collection_name="rag_collection"):
    """
    Create an OpenAI Agent with document retrieval + summarizer tools and memory.
    """

    # Retrieval Tool
    retrieval_tool = get_retrieval_tool(collection_name)

    # Summarizer Tool: Load all docs from Qdrant and build summary engine
    vector_store = QdrantVectorStore(client=client, collection_name=collection_name)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    documents = fetch_documents_from_qdrant(collection_name)
    tools = [retrieval_tool]

    if documents:  # only add summarizer if docs exist
        summarizer_engine = get_summarizer_tool(documents)
        summarizer_tool = QueryEngineTool.from_defaults(
            query_engine=summarizer_engine,
            name="DocumentSummarizer",
            description="Summarize uploaded documents"
        )
        tools.append(summarizer_tool)
    # Memory
    memory = ChatMemoryBuffer.from_defaults(token_limit=3900)

    # Create agent
    agent = OpenAIAgent.from_tools(
        tools=tools,
        verbose=True,
        memory=memory
    )

    return agent
