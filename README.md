# Dance Studio Analytics Pipeline

A complete data engineering project built for processing dance studio CRM data, creating analytical datasets, and forecasting class attendance.

The repository contains **two independent ETL implementations** built on the same business logic.

## Project Structure

```text
8count-data-analytics/
│
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

A production-oriented implementation using PySpark and Apache Airflow.

Features:

* CRM REST API extraction
* Distributed data processing with PySpark
* Parquet raw and staging layers
* PostgreSQL data warehouse
* Workflow orchestration with Apache Airflow
* Docker-based deployment

Run:

```bash
docker compose --project-name 8count-data-analytics -f pyspark_pipeline/docker-compose.yml up -d
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
* Parquet
* Scikit-learn
* Jupyter Notebook

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





