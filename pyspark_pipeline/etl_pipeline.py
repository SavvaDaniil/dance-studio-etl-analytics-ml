import os, sys
from datetime import date, datetime, timezone
from dateutil.relativedelta import relativedelta

from shared.extract.extract_pipeline import extract
from pyspark_pipeline.transform.transform_pipeline import transform
from pyspark_pipeline.load.load_pipeline import load

from pyspark.sql import SparkSession
import pyspark



def main(extract_at: datetime, visit_date_from: datetime, visit_date_to: datetime) -> None:

    print("Start extracting")
    extract(extract_at=extract_at, visit_date_from=visit_date_from, visit_date_to=visit_date_to)

    print("--- finish extract\nStart transforming")
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
    transform(spark=spark, extract_at=extract_at)

    print("--- finish transforming\nStart loading")
    load(spark=spark, extract_at=extract_at)
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

    extract_at: datetime = datetime.now(timezone.utc)
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