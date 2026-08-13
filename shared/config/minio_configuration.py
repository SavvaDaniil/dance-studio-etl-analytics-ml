import os

from dotenv import load_dotenv

load_dotenv()

MINIO_ENDPOINT: str = os.environ["MINIO_ENDPOINT"]
MINIO_ACCESS_KEY: str = os.environ["MINIO_ACCESS_KEY"]
MINIO_SECRET_KEY: str = os.environ["MINIO_SECRET_KEY"]
MINIO_BUCKET_NAME: str = os.environ["MINIO_BUCKET_NAME"]