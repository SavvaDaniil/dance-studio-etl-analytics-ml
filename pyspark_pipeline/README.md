# Dance Studio Analytics Pipeline (PySpark + Airflow)

ETL pipeline built with **PySpark**, **Apache Airflow**, **MinIO**, **PostgreSQL**, and **Docker**.

## Features

* Data extraction from CRM REST API
* ETL pipeline with PySpark
* Workflow orchestration with Apache Airflow
* S3-compatible object storage using MinIO
* Raw and staging layers stored as Parquet
* PostgreSQL data warehouse
* SQL analytics
* Docker-based deployment

## Technology Stack

* Python
* PySpark
* Apache Airflow
* MinIO (S3-compatible storage)
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
MinIO (S3)
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

Run the PySpark pipeline from the project root.

Initialize the Airflow database and create the admin user:

```bash
docker compose up --project-name 8count-data-analytics airflow-init
```

Start the services:

```bash
docker compose up --project-name 8count-data-analytics -d
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

## Storage

The PySpark pipeline uses MinIO as an S3-compatible object storage.

MinIO stores the raw and staging Parquet datasets.

MinIO
  ├── raw/
  │   └── YYYY-MM-DD/
  │
  └── staging/
      └── YYYY-MM-DD/

## Project Structure

The PySpark implementation is located in the pyspark_pipeline/ directory:

```text
pyspark_pipeline/
│
├── etl_pipeline.py
├── transform/
├── load/
└── README.md
```

The Docker and Airflow infrastructure is defined in the project root:

```text
8count-data-analytics/
│
├── docker-compose.yml
├── Dockerfile.airflow
├── pyspark_pipeline/
├── shared/
└── ...
```
