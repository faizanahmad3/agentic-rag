from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from src.utils.config import Config


Settings.llm = OpenAI(model="gpt-4o", api_key=Config.OPENAI_API_KEY)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small", api_key=Config.OPENAI_API_KEY)
# Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
# Settings.num_output = 512
# Settings.context_window = 3900

