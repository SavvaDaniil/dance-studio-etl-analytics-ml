# Dance Studio Analytics Pipeline (PySpark + Airflow)

Production-ready ETL pipeline built with **PySpark**, **Apache Airflow**, **PostgreSQL**, and **Docker**.

## Features

* Data extraction from CRM REST API
* ETL pipeline orchestrated by Apache Airflow
* Distributed data processing with PySpark
* Raw and staging layers stored as Parquet
* PostgreSQL data warehouse
* SQL analytics
* Docker deployment

## Technology Stack

* Python
* PySpark
* Apache Airflow
* PostgreSQL
* SQLAlchemy
* Docker
* Parquet

## Pipeline

```text
CRM API (ImpulseCRM)
        ↓
Extract (Python / Requests / Pandas)
        ↓
RAW Parquet
        ↓
Transform (PySpark)
        ↓
STAGING Parquet
        ↓
Load (PySpark)
        ↓
PostgreSQL
        ↓
SQL Analytics
```

## Run

From the project root:

```bash
docker compose \
    --project-name 8count-data-analytics \
    -f pyspark_pipeline/docker-compose.yml up -d
```

Open Airflow:

```text
http://localhost:8080
```

Default credentials:

```text
Username: admin
Password: admin
```

To trigger the pipeline:

1. Open the Airflow web interface.
2. Enable the DAG.
3. Click **Trigger DAG**.

The ETL pipeline automatically:

* extracts CRM data;
* transforms datasets using PySpark;
* loads the processed data into PostgreSQL.

## Project Structure

```text
pyspark_pipeline/
│
├── dags/
├── Dockerfile
├── docker-compose.yml
├── etl_pipeline.py
├── transform/
├── load/
└── README.md
```
