import os
import io
import pandas as pd
from minio import Minio
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_USER     = os.getenv("MINIO_ROOT_USER")
MINIO_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD")

POSTGRES_HOST    = os.getenv("POSTGRES_HOST")
POSTGRES_PORT    = "5432"
POSTGRES_USER    = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD= os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB      = os.getenv("POSTGRES_DB")

def read_silver():
    client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_USER,
        secret_key=MINIO_PASSWORD,
        secure=False
    )

    objects = client.list_objects("silver", prefix="tournaments/results.parquet/", recursive=True)
    
    dfs = []
    for obj in objects:
        if obj.object_name.endswith(".parquet"):
            response = client.get_object("silver", obj.object_name)
            dfs.append(pd.read_parquet(io.BytesIO(response.read())))
            response.close()
            response.release_conn()

    df = pd.concat(dfs, ignore_index=True)
    print(f"Silver load : {len(df)} tournois")
    return df

def load_to_postgres(df):
    engine = create_engine(
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    with engine.begin() as conn:
        conn.execute(text("DROP VIEW IF EXISTS gold.gold_results CASCADE"))
    df.to_sql("silver_results", engine, schema="public", if_exists="replace", index=False)
    print(f"PosgreSQL load : {len(df)} tournois")

def main():
    df = read_silver()
    load_to_postgres(df)


if __name__ == "__main__":
    main()