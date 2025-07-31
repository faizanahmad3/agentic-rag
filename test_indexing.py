from src.ingestion.pdf_loader import load_pdf
from src.indexing.index_builder import build_qdrant_index

# Load PDF
pages_data = load_pdf("/Users/faizan/PycharmProjects/agentic-rag/Documents/Saudi-Arabia-findings.pdf")

# Build Index in Qdrant
index = build_qdrant_index(pages_data)

print("Index built successfully and stored in Qdrant!")
