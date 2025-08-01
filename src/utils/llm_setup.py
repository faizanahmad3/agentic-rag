from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from src.utils.config import Config
import re


Settings.llm = OpenAI(model="gpt-4o", api_key=Config.OPENAI_API_KEY)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small", api_key=Config.OPENAI_API_KEY)

def contains_arabic(text):
    return bool(re.search(r'[\u0600-\u06FF]', text))

