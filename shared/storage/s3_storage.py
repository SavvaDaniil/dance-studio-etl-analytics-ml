from typing import Optional
import pandas as pd
from pandas import DataFrame
from minio import Minio
from shared.config.minio_configuration import MINIO_BUCKET_NAME
from io import BytesIO
from pathlib import Path

def s3_upload_file(minio_client: Minio, s3_prefix: str, local_dir: str, object_name: str):
    
    minio_client.fput_object(
        bucket_name=MINIO_BUCKET_NAME,
        object_name=f"{s3_prefix}/{object_name}.parquet",
        file_path=str(Path(f"{local_dir}/{object_name}.parquet")),
    )

def s3_upload_file_with_dataFrame(minio_client: Minio, s3_prefix: str, df: DataFrame):
    
    buffer = BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)
    minio_client.put_object(
        MINIO_BUCKET_NAME,
        s3_prefix,
        buffer,
        length=buffer.getbuffer().nbytes,
        content_type="application/octet-stream"
    )

def s3_download_dataframe(minio_client: Minio, object_name: str, s3_prefix: str) -> DataFrame:

    response = minio_client.get_object(
        MINIO_BUCKET_NAME,
        f"{s3_prefix}/{object_name}.parquet"
    )
    try:
        return pd.read_parquet(BytesIO(response.read()))
    finally:
        response.close()
        response.release_conn()