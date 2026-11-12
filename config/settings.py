import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from groq import Groq


# =========================================================
# 1. CONFIGURATION
# =========================================================

load_dotenv()

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
CHROMA_DIR = DATA_DIR / "chroma_db"
DB_PATH = DATA_DIR / "gapfinder.db"
TOPICS_PATH = DATA_DIR / "topics.json"
REPORT_PATH = DATA_DIR / "latest_report.json"

MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)

# LangChain embedding model and persistent Chroma vector store.
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY missing. Configure it in .env"
    )

client = Groq(api_key=API_KEY)

for directory in [DATA_DIR, UPLOAD_DIR, CHROMA_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

vector_store = None
retriever = None