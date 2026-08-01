from pathlib import Path
import os, sys
import pandas as pd
import numpy as np
from datetime import datetime, date

import subprocess
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    from_unixtime,
    unix_timestamp,
    to_timestamp,
    month,
    dayofweek,
    quarter,
    when
)

    
def save_staging(df: DataFrame, entity_name: str, extract_at_str: str) -> None:
    parquet_path: Path = Path(f"./data/staging/{entity_name}/{extract_at_str}")
    #parquet_path.mkdir(parents=True, exist_ok=True)

    (
        df.write
        .mode("overwrite")
        .parquet(str(parquet_path))
    )

def transform(spark: SparkSession, extract_at: datetime):
    extract_at_str: str = extract_at.strftime("%Y-%m-%d")

    df_styles = spark.read.parquet(f"./data/raw/styles/{extract_at_str}/styles.parquet")
    df_styles = df_styles.drop(
        "_ingested_at",
        "entity",
        "fotoFileName",
        "fotoUrl",
        "fotoThumbUrl"
    )


    df_teachers: DataFrame = spark.read.parquet(f'./data/raw/teachers/{extract_at_str}/teachers.parquet')
    df_teachers = (
        df_teachers
        .withColumnRenamed("lastName", "last_name")
        .drop(
            "_ingested_at", "rating", "address", "annotation", "inn", "post", "reviews", "birthDate", "email", "socialPage", "entity", "fotoFileName", "fotoUrl", "fotoThumbUrl", "phone", "middleName", "age", "man"
        )
    )


    df_groups: DataFrame = spark.read.parquet(f'./data/raw/groups/{extract_at_str}/groups.parquet')
    df_groups = (
        df_groups
        #.withColumn("teacher_id", col("teacher1.id"))
        .withColumn("teacher_id", col("teacher1")["id"])
        .withColumn("style_id", col("style")["id"])
        .drop(
            "_ingested_at", 
            "age", 
            "number", 
            "placeCount", 
            "showInWidget", 
            "teacher2", 
            "entity", 
            "annotation", 
            "style", 
            "teacher1"
        )
    )


    df_schedules: DataFrame = spark.read.parquet(f'./data/raw/schedules/{extract_at_str}/schedules.parquet')
    df_schedules = (
        df_schedules
        .withColumn("group_id", col("group.id"))
        .withColumnRenamed("minutesBegin", "minutes_begin")
        .withColumnRenamed("minutesEnd", "minutes_end")
        .drop("group", "target", "branch", "teacher", "teacher1", "teacher2", "style", "entity", "client", "date", "regular", "created", "creator", "hall", "color", "type", "note", "payment", "wage", "typeTitle", "deleted", "_ingested_at", "dateBegin", "dateEnd")
    )



    df_group_singles: DataFrame = spark.read.parquet(f"./data/raw/group_singles/{extract_at_str}/group_singles.parquet")
    df_group_singles = (
        df_group_singles
        .withColumn("group_id", col("group.id"))
        .withColumn("style_id", col("group.style.id"))
        .withColumn("teacher_id", col("group.teacher1.id"))
        .withColumn("client_id", col("client.id"))
        .withColumn("visit_date", to_timestamp(from_unixtime(col("visitDate"))))
        #.withColumn("visit_date", to_timestamp(from_unixtime(unix_timestamp(col("visit_date")))))
        .withColumn("month", month(col("visit_date")))
        .withColumn("quarter", quarter(col("visit_date")))
        .withColumn("weekday", ((dayofweek(col("visit_date")) + 6) % 7))
        .withColumn("is_weekend", col("weekday") > 4)
        .withColumn(
            "season",
            when(col("month").isin(12, 1, 2), "winter")
            .when(col("month").isin(3, 4, 5), "spring")
            .when(col("month").isin(6, 7, 8), "summer")
            .otherwise("autumn")
        )
        .withColumnRenamed("typeName", "type_name")
        .withColumnRenamed("minutesBegin", "minutes_begin")
        .withColumnRenamed("minutesEnd", "minutes_end")
        .drop("_ingested_at", "id", "group", "target", "entity", "branch", "hall", "group", "archived", "annotation", "device", "deleted", "creator", "free", "service", "typeColor", "updated", "updater", "created", "shift", "clientOrder", "client", "visitDate", "duration", "payBox", "discount", "discountCurrency", "debt", "refund", "total", "paid")
    )
    




    df_visits: DataFrame = spark.read.parquet(f'./data/raw/visits/{extract_at_str}/visits.parquet')
    df_visits = (
        df_visits
        .withColumn("group_id", col("group.id"))
        .withColumn("style_id", col("group.style.id"))
        .withColumn("teacher_id", col("group.teacher1.id"))
        .withColumn("client_id", col("client.id"))
        .withColumn("visit_date", to_timestamp(from_unixtime(col("visitDate"))))
        .withColumn("month", month(col("visit_date")))
        .withColumn("quarter", quarter(col("visit_date")))
        .withColumn("weekday", ((dayofweek(col("visit_date")) + 6) % 7))
        .withColumn("is_weekend", col("weekday") > 4)
        .withColumn(
            "season",
            when(col("month").isin(12, 1, 2), "winter")
            .when(col("month").isin(3, 4, 5), "spring")
            .when(col("month").isin(6, 7, 8), "summer")
            .otherwise("autumn")
        )
        .withColumnRenamed("minutesBegin", "minutes_begin")
        .withColumnRenamed("minutesEnd", "minutes_end")
        .withColumn("group_account_id", col("groupAccount.id"))
        .withColumn("group_account_cost", col("groupAccount.cost"))
        .withColumn("group_account_trainings_total", col("groupAccount.trainingsTotal"))
        .withColumn("group_account_is_unlimited", col("groupAccount.trainingsTotal") == -1)
        .withColumn(
            "lesson_cost",
            when(
                col("groupAccount.trainingsTotal") > 0,
                col("groupAccount.cost") /
                col("groupAccount.trainingsTotal")
            ).otherwise(None)
        )
        .drop("_ingested_at", "id", "free", "type", "burned", "entity", "_ingested_at", "client", "branch", "creator", "deleted", "target", "created", "cost", "service", "teacher", "hall", "rentAccount", "individualAccount", "selfAccount", "group", "visitDate", "duration", "groupAccount")
    )

    #df_group_singles.printSchema()
    #df_group_singles.select("visit_date").show(5, False)

    save_staging(df=df_styles, entity_name="styles", extract_at_str=extract_at_str)
    save_staging(df=df_teachers, entity_name="teachers", extract_at_str=extract_at_str)
    save_staging(df=df_groups, entity_name="groups", extract_at_str=extract_at_str)
    save_staging(df=df_schedules, entity_name="schedules", extract_at_str=extract_at_str)
    save_staging(df=df_group_singles, entity_name="group_singles", extract_at_str=extract_at_str)
    save_staging(df=df_visits, entity_name="visits", extract_at_str=extract_at_str)


if __name__ == "__main__":

    os.environ["PATH"] = (
        os.path.join(os.environ["HADOOP_HOME"], "bin")
        + ";"
        + os.environ["PATH"]
    )

    os.environ["PYSPARK_PYTHON"] = sys.executable
    #print("PATH contains Hadoop:", any("hadoop" in p.lower() for p in os.environ["PATH"].split(";")))

    
    if "HADOOP_HOME" not in os.environ:
        raise RuntimeError(
            "HADOOP_HOME is not configured. Please configure Hadoop before running Spark."
        )
    spark = (SparkSession.builder.appName("DanceStudioETL").getOrCreate())
    transform(spark=spark, extract_at=date(2026, 7, 29))
    spark.stop()


"""
.str["id"]	col("column.id")
.astype(int)	.cast("int")
.map()	when()
np.where()	when(...).otherwise(...)
fillna()	na.fill()
dropna()	na.drop()
rename()	withColumnRenamed()
drop(columns=...)	drop(...)


# for check

# print(os.path.exists(
#     os.path.join(os.environ["HADOOP_HOME"], "bin", "hadoop.dll")
# ))
# spark = (
#     SparkSession.builder
#     .master("local[*]")
#     .appName("test")
#     .getOrCreate()
# )

# df = spark.createDataFrame(
#     [(1, "a"), (2, "b")],
#     ["id", "name"]
# )

# df.show()
# Path("tmp").mkdir(exist_ok=True)
# df.write.mode("overwrite").parquet("tmp/test")
# spark.stop()
"""