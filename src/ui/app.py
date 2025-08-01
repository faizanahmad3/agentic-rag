import streamlit as st
from src.ingestion.pdf_loader import load_pdf
from src.indexing.index_builder import build_qdrant_index
from src.utils.config import Config
import os
from src.agent.agent_runner import create_agent
from src.tools.qdrant_helper import client
from src.utils.llm_setup import contains_arabic

# Title
st.title("Agentic RAG Chat App")

# Sidebar for file upload
st.sidebar.header("Upload PDFs")
uploaded_files = st.sidebar.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

# Collection name (optional)
collection_name = st.sidebar.text_input("Collection Name", "rag_collection")

# Create agent
agent = create_agent(collection_name)

# Button to process files
if uploaded_files and st.sidebar.button("Process Documents"):
    st.sidebar.write("Processing uploaded PDFs...")

    # Save uploaded files temporarily
    os.makedirs("data/uploads", exist_ok=True)
    pages_data = []
    for file in uploaded_files:
        file_path = os.path.join("data/uploads", file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        # Load and add to pages_data
        pages_data.extend(load_pdf(file_path))

    # Build Qdrant Index
    build_qdrant_index(pages_data, collection_name=collection_name)
    st.sidebar.success("Documents indexed successfully!")
    # Recreate agent with updated Qdrant data
    st.session_state.agent = create_agent(collection_name)

# Chat Section
st.header("Ask a Question")

# Initialize agent with memory in session state
if "agent" not in st.session_state:
    st.session_state.agent = create_agent(collection_name)

question = st.text_input("Enter your question:")

if st.button("Get Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        # Use agent from session (preserves memory)
        if contains_arabic(question):
            question = f"(شرح مفصل) {question}"
        response = st.session_state.agent.chat(question)

        # Display answer
        st.write(f"**Answer:** {response.response}")

        # Show sources (if any)
        if response.source_nodes:
            st.write("**Sources:**")
            for node in response.source_nodes:
                meta = node.metadata
                file_name = meta.get("file_name", "Unknown File")
                page_number = meta.get("page_number", "N/A")
                st.write(f"- {file_name} (Page {page_number})")


# Optional: Show chat history
if st.button("Show Conversation History"):
    st.write(st.session_state.agent.memory.get())

# Clear database button
if st.sidebar.button("Clear Database"):
    try:
        client.delete_collection(collection_name)  # Drops the collection
        st.sidebar.success(f"Collection '{collection_name}' cleared!")
    except Exception as e:
        st.sidebar.error(f"Error clearing database: {str(e)}")

