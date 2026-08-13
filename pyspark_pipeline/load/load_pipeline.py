

import os, sys

from datetime import datetime, date
from shared.db.database_session import get_engine
from shared.db.database_base import PosgtreBase
from sqlalchemy import text
from shared.models.style import Style
from shared.models.teacher import Teacher
from shared.models.group import Group
from shared.models.schedule import Schedule
from shared.models.group_single import GroupSingle
from shared.models.visit import Visit
from shared.config.database_configuration import DatabaseConfiguration, get_database_configuration
from minio import Minio
from shared.config.minio_configuration import MINIO_BUCKET_NAME


import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame


def write_table(
    df: DataFrame,
    table_name: str,
    databaseConfiguration: DatabaseConfiguration,
    jdbc_url: str,
) -> None:
    (
        df.write
        .format("jdbc")
        .option("url", jdbc_url)
        .option("dbtable", table_name)
        .option("user", databaseConfiguration.username)
        .option("password", databaseConfiguration.password)
        .option("driver", "org.postgresql.Driver")
        .mode("append")
        .save()
    )

def read_parquet(spark: SparkSession, extract_at_str: str, object_name: str, is_using_S3: bool) -> DataFrame:
    if is_using_S3:
        return read_parquet_from_S3(spark=spark,extract_at_str=extract_at_str, object_name=object_name)
    else:
        return read_parquet_local(spark=spark,extract_at_str=extract_at_str, object_name=object_name)

def read_parquet_local(spark: SparkSession, extract_at_str: str, object_name: str) -> DataFrame:
    return spark.read.parquet(f"./data/staging/{extract_at_str}/{object_name}.parquet")

def read_parquet_from_S3(spark: SparkSession, extract_at_str: str, object_name: str) -> DataFrame:
    return spark.read.parquet(f"s3a://{MINIO_BUCKET_NAME}/staging/{extract_at_str}/{object_name}")



def load(spark: SparkSession, extract_at: datetime, is_using_S3: bool) -> None:
    extract_at_str: str = extract_at.strftime("%Y-%m-%d")
    
    # df_styles: DataFrame = spark.read.parquet(f'./data/staging/styles/{extract_at_str}')
    # df_teachers: DataFrame = spark.read.parquet(f'./data/staging/teachers/{extract_at_str}')
    # df_groups: DataFrame = spark.read.parquet(f'./data/staging/groups/{extract_at_str}')
    # df_schedules: DataFrame = spark.read.parquet(f'./data/staging/schedules/{extract_at_str}')
    # df_group_singles: DataFrame = spark.read.parquet(f'./data/staging/group_singles/{extract_at_str}')
    # df_visits: DataFrame = spark.read.parquet(f'./data/staging/visits/{extract_at_str}')
    df_styles: DataFrame = read_parquet(spark=spark, extract_at_str=extract_at_str, object_name='styles', is_using_S3=is_using_S3)
    df_teachers: DataFrame = read_parquet(spark=spark, extract_at_str=extract_at_str, object_name='teachers', is_using_S3=is_using_S3)
    df_groups: DataFrame = read_parquet(spark=spark, extract_at_str=extract_at_str, object_name='groups', is_using_S3=is_using_S3)
    df_schedules: DataFrame = read_parquet(spark=spark, extract_at_str=extract_at_str, object_name='schedules', is_using_S3=is_using_S3)
    df_group_singles: DataFrame = read_parquet(spark=spark, extract_at_str=extract_at_str, object_name='group_singles', is_using_S3=is_using_S3)
    df_visits: DataFrame = read_parquet(spark=spark, extract_at_str=extract_at_str, object_name='visits', is_using_S3=is_using_S3)

    engine = get_engine()
    PosgtreBase.metadata.create_all(bind=engine)

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE styles CASCADE"))
        conn.execute(text("TRUNCATE TABLE teachers CASCADE"))
        conn.execute(text("TRUNCATE TABLE groups CASCADE"))
        conn.execute(text("TRUNCATE TABLE schedules CASCADE"))
        conn.execute(text("TRUNCATE TABLE group_singles CASCADE"))
        conn.execute(text("TRUNCATE TABLE visits CASCADE"))


    databaseConfiguration: DatabaseConfiguration = get_database_configuration()
    jdbc_url = (
        f"jdbc:postgresql://"
        f"{databaseConfiguration.host}:"
        f"{databaseConfiguration.port}/"
        f"{databaseConfiguration.database_name}"
    )


    # (
    #     df_styles.write
    #     .format("jdbc")
    #     .option("url", jdbc_url)
    #     .option("dbtable", "styles")
    #     .option("user", databaseConfiguration.username)
    #     .option("password", databaseConfiguration.password)
    #     .option("driver", "org.postgresql.Driver")
    #     .mode("append")
    #     .save()
    # )
    write_table(df=df_styles, table_name="styles", databaseConfiguration=databaseConfiguration, jdbc_url=jdbc_url)
    write_table(df=df_teachers, table_name="teachers", databaseConfiguration=databaseConfiguration, jdbc_url=jdbc_url)
    write_table(df=df_groups, table_name="groups", databaseConfiguration=databaseConfiguration, jdbc_url=jdbc_url)
    write_table(df=df_schedules, table_name="schedules", databaseConfiguration=databaseConfiguration, jdbc_url=jdbc_url)
    write_table(df=df_group_singles, table_name="group_singles", databaseConfiguration=databaseConfiguration, jdbc_url=jdbc_url)
    write_table(df=df_visits, table_name="visits", databaseConfiguration=databaseConfiguration, jdbc_url=jdbc_url)



if __name__ == "__main__":

    os.environ["PATH"] = (
        os.path.join(os.environ["HADOOP_HOME"], "bin")
        + ";"
        + os.environ["PATH"]
    )
    os.environ["PYSPARK_PYTHON"] = sys.executable
    if "HADOOP_HOME" not in os.environ:
        raise RuntimeError(
            "HADOOP_HOME is not configured. Please configure Hadoop before running Spark."
        )
    
    spark = (
        SparkSession
        .builder
        .config(
            "spark.jars",
            "drivers/postgresql-42.7.7.jar"
        )
        .appName("DanceStudioETL")
        .getOrCreate()
    )
    load(spark=spark, extract_at=date(2026, 7, 29))
    spark.stop()
    