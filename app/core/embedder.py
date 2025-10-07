from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from pydantic import SecretStr
from langchain.embeddings.base import Embeddings
from dotenv import load_dotenv

load_dotenv()

GEMINI_EMBEDDING_MODEL: str = os.getenv("GEMINI_EMBEDDING_MODEL") or ""
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY") or ""

if not GEMINI_API_KEY:
    raise Exception("GEMINI_API_KEY is not set")

if not GEMINI_EMBEDDING_MODEL:
    raise Exception("GEMINI_EMBEDDING_MODEL is not set")

gemini_embedding: Embeddings = GoogleGenerativeAIEmbeddings(
    model=GEMINI_EMBEDDING_MODEL,
    google_api_key=SecretStr(GEMINI_API_KEY)
)
