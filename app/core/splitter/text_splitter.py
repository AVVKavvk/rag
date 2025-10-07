import os
import uuid
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.core.utils.s3 import download_file_from_s3, delete_file_from_local
from app.utils.logger import logger

TEMP_DIR = "/tmp/rag_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

CHUNK_SIZE = os.getenv("CHUNK_SIZE") or 700
CHUNK_OVERLAP = os.getenv("CHUNK_OVERLAP") or 200


def load_and_split_from_s3(s3_key: str, filename: str):
    """
    Load a document from S3, convert content to lowercase,
    split it into individual pages, and return the pages as a list of strings.
    """
    try:
        # Create full local path including the filename
        local_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}-{filename}")
        logger.info(f"Downloading {s3_key} to {local_path}")

        download_file_from_s3(s3_key, local_path)

        logger.info(f"Downloaded {s3_key} to {local_path}")

        file_ext = filename.lower()
        if file_ext.endswith(".pdf"):
            loader = PyMuPDFLoader(local_path)
        elif file_ext.endswith(".txt"):
            loader = TextLoader(local_path)
        else:
            raise ValueError("Unsupported file type")

        logger.info(f"Splitting {s3_key} into chunks of 500 tokens with 100 token overlap")

        docs = loader.load()

        # Convert content to lowercase
        for doc in docs:
            doc.page_content = doc.page_content.lower()

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_documents(docs)

        logger.info(f"Split {s3_key} into {len(chunks)} chunks")

        for chunk in chunks:
            chunk.metadata["source"] = filename

        delete_file_from_local(local_path)
        return chunks

    except Exception as e:
        logger.error(f"Failed to load and split {s3_key}: {e}")
        raise e
