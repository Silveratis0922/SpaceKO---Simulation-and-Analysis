import os
from minio import Minio
from dotenv import load_dotenv

load_dotenv()

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
PARQUET_SOURCE = os.getenv("PARQUET_SOURCE")
BUCKET_NAME    = "bronze"
OBJECT_NAME    = "tournaments/events.parquet"

def upload_to_bronze():
    client = Minio(
        MINIO_ENDPOINT,
        access_key=os.getenv("MINIO_ROOT_USER"),
        secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
        secure=False
    )

    client.fput_object(BUCKET_NAME, OBJECT_NAME, PARQUET_SOURCE)
    print(f"Upload done: {PARQUET_SOURCE}, {BUCKET_NAME}/{OBJECT_NAME}")

if __name__ == "__main__":
    upload_to_bronze()