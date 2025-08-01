import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Qdrant (Cloud or Local)
    QDRANT_HOST = os.getenv("QDRANT_HOST")  # Example: https://your-cluster-url.qdrant.io
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")  # Required for Qdrant Cloud

