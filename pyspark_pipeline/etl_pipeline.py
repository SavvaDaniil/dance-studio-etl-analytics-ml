import os, sys
from datetime import date, datetime, timezone
from dateutil.relativedelta import relativedelta

from shared.extract.extract_pipeline import extract
from pyspark_pipeline.transform.transform_pipeline import transform
from pyspark_pipeline.load.load_pipeline import load

from pyspark.sql import SparkSession
from minio import Minio
from shared.config.minio_configuration import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET_NAME

packages_for_hadoop: list[str] = [
    "org.apache.hadoop:hadoop-aws:3.5.0",
]

def main(extract_at: datetime, visit_date_from: datetime, visit_date_to: datetime) -> None:

    minio_client: Minio = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )
    if not minio_client.bucket_exists(MINIO_BUCKET_NAME):
        minio_client.make_bucket(MINIO_BUCKET_NAME)

    spark = (
        SparkSession
        .builder
        .config(
            "spark.jars",
            "drivers/postgresql-42.7.7.jar"
        )
        .config(
            "spark.jars.packages", 
            ",".join(packages_for_hadoop)
        )
        .config(
            "spark.hadoop.fs.s3a.endpoint",
            os.environ["MINIO_ENDPOINT"] #"http://minio:9000" # without docker localhost:9000, with docker minio:9000
        )
        .config(
            "spark.hadoop.fs.s3a.access.key",
            os.environ["AWS_ACCESS_KEY_ID"]
        )
        .config(
            "spark.hadoop.fs.s3a.secret.key",
            os.environ["AWS_SECRET_ACCESS_KEY"]
        )
        .config(
            "spark.hadoop.fs.s3a.path.style.access",
            "true"
        )
        .config(
            "spark.hadoop.fs.s3a.connection.ssl.enabled",
            "false"
        )
        .appName("DanceStudioETL")
        .getOrCreate()
    )

    # print("Spark:", spark.version)
    # print("Hadoop:", spark.sparkContext._jvm.org.apache.hadoop.util.VersionInfo.getVersion())

    # print("S3A:", spark.sparkContext._jsc.hadoopConfiguration().get("fs.s3a.impl"))
    # print("LOCAL TEST")

    # df_local = spark.read.parquet("./data/raw/2026-08-13/styles.parquet")
    # print(df_local.schema)
    # print("S3 TEST")

    # df_s3 = spark.read.parquet(f"s3a://{MINIO_BUCKET_NAME}/raw/2026-08-13/styles.parquet")
    # print(df_s3.schema)
    
    print("Start extracting")
    extract(
        extract_at=extract_at, 
        visit_date_from=visit_date_from, 
        visit_date_to=visit_date_to, 
        minio_client=minio_client
    )

    # print(spark.sparkContext._jsc.hadoopConfiguration().get("fs.s3a.impl"))
    # print(spark.version)
    print("--- finish extract\nStart transforming")
    transform(spark=spark, extract_at=extract_at, is_using_S3=True)

    print("--- finish transforming\nStart loading")
    load(spark=spark, extract_at=extract_at, is_using_S3=True)
    spark.stop()

    print("--- finish loading")

if __name__ == "__main__":

    # without docker remove comment
    # if "HADOOP_HOME" not in os.environ:
    #     raise RuntimeError(
    #         "HADOOP_HOME is not configured. Please configure Hadoop before running Spark."
    #     )
    # os.environ["PATH"] = (
    #     os.path.join(os.environ["HADOOP_HOME"], "bin")
    #     + ";"
    #     + os.environ["PATH"]
    # )

    os.environ["PYSPARK_PYTHON"] = sys.executable
    #print("PATH contains Hadoop:", any("hadoop" in p.lower() for p in os.environ["PATH"].split(";")))

    extract_at: datetime = datetime(2026, 8, 13) #datetime.now(timezone.utc)
    visit_date_to: datetime = extract_at.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )
    visit_date_from = (visit_date_to - relativedelta(months=2))

    main(
        extract_at=extract_at, #datetime(2026, 7, 29),#datetime.now(timezone.utc), 
        visit_date_from=visit_date_from, #datetime(2024, 1, 1), 
        visit_date_to=visit_date_to, #datetime(2026, 7, 1)
    )

# 2026 7 29 - 6 months