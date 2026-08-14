# Dance Studio Analytics Pipeline

A complete data engineering project for processing dance studio CRM data, building analytical datasets, and forecasting class attendance.

The repository contains **two independent ETL implementations** built on shared business logic:

- a lightweight **Pandas** pipeline;
- a **PySpark + Apache Airflow** pipeline with S3-compatible object storage provided by MinIO.

## Project Structure

```text
8count-data-analytics/
│
├── docker-compose.yml          # PySpark + Airflow + MinIO + PostgreSQL
├── shared/                     # Shared extraction logic and common modules
├── pandas_pipeline/            # Pandas ETL implementation
├── pyspark_pipeline/           # PySpark + Airflow ETL implementation
├── 01_sql_eda.ipynb            # Exploratory data analysis
├── 02_machine_learning.ipynb   # Machine learning models
└── README.md
```

## Implementations

### 1. Pandas Pipeline

A lightweight ETL implementation using Pandas.

Features:

* CRM REST API extraction
* Parquet raw layer
* Data transformation with Pandas
* PostgreSQL data warehouse
* SQL analytics
* Machine Learning models

Run:

```bash
docker compose -f pandas_pipeline/docker-compose.yml up -d

python -m pandas_pipeline.etl_pipeline
```

Documentation:

```text
pandas_pipeline/README.md
```

---

### 2. PySpark + Airflow Pipeline

ETL pipeline built with **PySpark**, **Apache Airflow**, **MinIO**, **PostgreSQL**, and **Docker**.

Features:

* CRM REST API extraction
* Shared extraction logic with the Pandas pipeline
* Distributed data processing with PySpark
* RAW and STAGING layers stored as Parquet
* S3-compatible object storage using MinIO
* PostgreSQL data warehouse
* Workflow orchestration with Apache Airflow
* Scheduled and manual ETL execution
* Docker-based deployment

#### Start the infrastructure:

Initialize the Airflow metadata database and create the default user:

```bash
docker compose --project-name 8count-data-analytics up airflow-init
docker compose --project-name 8count-data-analytics --profile build build etl_eda
```

After successful initialization, start the services:

```bash
docker compose --project-name 8count-data-analytics up -d
```

The PySpark ETL container is **not started automatically** as a long-running service.

The ETL job is started by Apache Airflow using DockerOperator when the DAG is triggered.

Open Airflow:

```text
http://localhost:8080
```

Default credentials:

```text
Username: admin
Password: admin
```

#### Run the ETL pipeline
1. Open the Airflow web interface.
2. Find the dance_studio_etl DAG.
3. Enable the DAG if it is paused.
4. Click Trigger DAG.

Airflow starts a temporary ETL container that executes the PySpark pipeline and removes the container after completion.

The pipeline performs:

CRM API
   ↓
Extract
   ↓
RAW Parquet → MinIO
   ↓
Transform → PySpark
   ↓
STAGING Parquet → MinIO
   ↓
Load
   ↓
PostgreSQL

Documentation:

```text
pyspark_pipeline/README.md
```

## Technologies

* Python
* Pandas
* PySpark
* Apache Airflow
* PostgreSQL
* SQLAlchemy
* Docker
* MinIO / S3
* Parquet
* Jupyter Notebook
* Scikit-learn

## Analytical Reports

The project produces analytical datasets including:

* attendance by weekday;
* attendance by class time;
* teacher ranking;
* revenue by dance style;
* cumulative revenue analysis.

## Machine Learning

Attendance forecasting models:

* Linear Regression
* Decision Tree Regressor
* Random Forest Regressor

Best model:

* Linear Regression

## Architecture

The project demonstrates two approaches to the same ETL problem:

                    ┌──────────────────┐
                    │    CRM REST API  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Shared Extraction│
                    │      Logic       │
                    └────────┬─────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
     ┌─────────────────┐           ┌─────────────────┐
     │ Pandas Pipeline  │           │ PySpark Pipeline│
     │                 │           │   + Airflow     │
     └────────┬────────┘           └────────┬────────┘
              │                             │
              ▼                             ▼
       Local Parquet                  MinIO / S3
              │                             │
              ▼                             ▼
       PostgreSQL DW                  PostgreSQL DW