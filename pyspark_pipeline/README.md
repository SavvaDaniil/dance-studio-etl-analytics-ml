# Dance Studio Analytics Pipeline (PySpark + Airflow)

ETL pipeline built with **PySpark**, **Apache Airflow**, **MinIO**, **PostgreSQL**, and **Docker**.

This is the PySpark implementation of the Dance Studio Analytics project. It uses the shared extraction logic together with PySpark for data transformation and Apache Airflow for workflow orchestration.

## Features

* Data extraction from CRM REST API
* Shared extraction logic with the Pandas pipeline
* Data transformation using PySpark
* RAW and STAGING layers stored as Parquet
* S3-compatible object storage using MinIO
* PostgreSQL data warehouse
* Workflow orchestration with Apache Airflow
* Manual and scheduled ETL execution
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
docker compose --project-name 8count-data-analytics up airflow-init
```

Build the PySpark ETL image:

```bash
docker compose --project-name 8count-data-analytics --profile build build etl_eda
```

Start the services:

```bash
docker compose up --project-name 8count-data-analytics -d
```

The infrastructure includes:
- Apache Airflow
- Airflow scheduler
- Airflow webserver
- PostgreSQL
- MinIO

The ETL image is built using the build Docker Compose profile, but the ETL container is not started as a permanent service.

Open Airflow:

```text
http://localhost:8080
```

Default credentials:

```text
Username: admin
Password: admin
```

### Trigger the ETL pipeline
1. Open the Airflow web interface.
2. Find the dance_studio_etl DAG.
3. Enable the DAG if it is paused.
4. Click Trigger DAG.

Airflow uses DockerOperator to start a temporary ETL container.

The container executes:

```text
pyspark_pipeline.etl_pipeline
```

and is automatically removed after the task finishes.

## Storage

The PySpark pipeline uses MinIO as an S3-compatible object storage.

MinIO stores the raw and staging Parquet datasets.

```text
MinIO
  ├── raw/
  │   └── YYYY-MM-DD/
  │
  └── staging/
      └── YYYY-MM-DD/
```

## Data Flow

```text
                    ┌───────────────┐
                    │   CRM API     │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    Extract    │
                    │ Python/Pandas │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  RAW Parquet  │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    MinIO      │
                    │     S3        │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   Transform   │
                    │    PySpark    │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │STAGING Parquet│
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │     Load      │
                    │    PySpark    │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  PostgreSQL   │
                    │ Data Warehouse│
                    └───────────────┘
```

## Airflow

The DAG is located in:

```text
dags/dance_studio_pipeline.py
```

The DAG uses DockerOperator to execute the ETL pipeline in an isolated Docker container.

The ETL container is not started automatically by Docker Compose. It is created by Airflow only when the DAG is triggered.

The pipeline can be triggered:
- manually from the Airflow UI;
- automatically according to the configured schedule.

## Architecture

The project separates the ETL image from the Airflow infrastructure.

```text
Docker Compose
│
├── Airflow
│   ├── Webserver
│   └── Scheduler
│
├── PostgreSQL
│
├── MinIO
│
└── ETL image
    │
    └── started on demand by Airflow
        │
        └── DockerOperator
            │
            └── PySpark ETL
```

The ETL image is not run as a long-lived service. Airflow creates a temporary container from the image when the ETL task is executed and removes it after completion.

## Project Structure

The PySpark implementation is located in the pyspark_pipeline/ directory:

```text
pyspark_pipeline/
│
├── etl_pipeline.py
├── transform/
├── load/
├── requirements.txt
└── README.md
```

The Docker and Airflow infrastructure is defined in the project root:

```text
8count-data-analytics/
│
├── dags/
│   └── dance_studio_pipeline.py
├── docker-compose.yml
├── Dockerfile.airflow
├── Dockerfile
├── pyspark_pipeline/
├── shared/
└── ...
```

## Related Implementation

The repository also contains a lightweight Pandas implementation:

```text
pandas_pipeline/
```

Both implementations use the same shared extraction logic but differ in their processing and orchestration approach:

```text
Pandas:
Extract → Local Parquet → Pandas Transform → PostgreSQL

PySpark:
Extract → MinIO/S3 → PySpark Transform → PostgreSQL
                       ↑
                    Airflow
```