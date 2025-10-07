from app.utils.logger import logger
from app.core.embedder import gemini_embedding
from app.core.splitter.text_splitter import load_and_split_from_s3
from app.core.utils.s3 import upload_file_to_s3


class RagService():
    def __init__(self, org_id: str):
        self.logger = logger
        self.embedder = gemini_embedding
        self.org_id = org_id

    async def generate_embedding_service(self, file_data: bytes, filename: str, content_type: str):
        try:
            self.logger.info(f"Generating embedding for {filename}")
            self.logger.info("Uploading file to S3")
            s3_key = upload_file_to_s3(self.org_id, file_data, filename, content_type)
            self.logger.info("File uploaded to S3")

            self.logger.info(f"Generating chunks for {filename}")

            chunks = load_and_split_from_s3(s3_key, filename)

            self.logger.info(f"Generated chunks for {filename}")
            print(chunks)

        except Exception as e:
            self.logger.error(f"Failed to generate embedding for {filename}: {e}")
            raise
