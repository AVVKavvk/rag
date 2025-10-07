import boto3
import os
from dotenv import load_dotenv
from io import BytesIO
import logging

load_dotenv()

s3 = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

BUCKET = os.getenv("S3_ASS_BUCKET_NAME")


def upload_file_to_s3(org_id: str, file_data: bytes, filename: str, content_type: str):
    """
    Uploads a file to S3.
    Args:
        file_data (bytes): The file data to upload.
        filename (str): The filename to use for the upload.
        content_type (str): The content type of the file.
    """
    try:
        key = f"{org_id}/documents/{filename}"
        logging.info(f"Uploading {filename} to s3 bucket {BUCKET} with key {key}")

        s3.upload_fileobj(
            Fileobj=BytesIO(file_data),
            Bucket=BUCKET,
            Key=key,
            ExtraArgs={"ContentType": content_type},
        )

        logging.info(f"Uploaded {filename} to s3 bucket {BUCKET} with key {key}")
        return key

    except Exception as e:
        logging.error(f"Failed to upload {filename} to s3 bucket {BUCKET}: {e}")
        raise


def download_file_from_s3(s3_key: str, local_path: str):
    """
    Downloads a file from S3.
    Args:
    s3_key (str): The key of the file to download.
    local_path (str): The path to save the file to.
    """
    try:
        logging.info(f"Downloading {s3_key} from s3 bucket {BUCKET} to {local_path}")

        s3.download_file(BUCKET, s3_key, local_path)

        logging.info(f"Downloaded {s3_key} from s3 bucket {BUCKET} to {local_path}")

    except Exception as e:
        logging.error(f"Failed to download {s3_key} from s3 bucket {BUCKET}: {e}")
        raise e


def delete_file_from_local(local_path: str):
    try:
        logging.info(f"Deleting {local_path}")
        os.remove(local_path)
        logging.info(f"Deleted {local_path}")
    except Exception as e:
        logging.error(f"Failed to delete {local_path}: {e}")
        raise
