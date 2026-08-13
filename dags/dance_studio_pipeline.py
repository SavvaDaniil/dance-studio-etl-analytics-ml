from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime
# from dateutil.relativedelta import relativedelta

# from pyspark.sql import SparkSession

# from src.extract.extract_all_datas import extract
# from src.transform.transform_all_pyspark import transform
# from src.load.load_all_pyspark import load

# def run_pipeline():
#     extract_at = datetime.now()

#     visit_date_to = extract_at.replace(
#         day=1,
#         hour=0,
#         minute=0,
#         second=0,
#         microsecond=0
#     )

#     visit_date_from = visit_date_to - relativedelta(months=6)

#     extract(extract_at=extract_at, visit_date_from=visit_date_from, visit_date_to=visit_date_to)

#     spark = (
#         SparkSession.builder
#         .appName("dance-studio-etl")
#         .getOrCreate()
#     )

#     transform(spark=spark, extract_at=extract_at)
#     load(spark=spark, extract_at=extract_at)

#     spark.stop()


with DAG(
    dag_id="dance_studio_etl",
    start_date=datetime(2026,1,1),
    schedule="@daily",
    catchup=False,
):
    
    etl_task = DockerOperator(
        task_id="run_etl",
        image="8count-data-analytics-etl_eda",
        container_name="dance_etl_run",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="8count-data-analytics_default"
    )
    etl_task

    # etl_task = BashOperator(
    #     task_id="etl",
    #     bash_command="cd /opt/airflow/project && python etl_pipeline_pyspark.py",
    # )
    # etl_task

    # etl_task = BashOperator(
    #     task_id="run_etl",
    #     #python_callable=run_pipeline
    #     bash_command="python /project/etl_pipeline_pyspark.py"
    # )

    # etl_task

    # extract_task = PythonOperator(
    #     task_id="extract",
    #     python_callable=run_extract
    # )

    # transform_task = PythonOperator(
    #     task_id="transform",
    #     python_callable=run_transform
    # )

    # load_task = PythonOperator(
    #     task_id="load",
    #     python_callable=run_load
    # )

    # extract_task >> transform_task >> load_task


# docker compose up airflow-init