# Dance Studio Analytics Pipeline

A complete ETL and analytics pipeline built for processing dance studio CRM data and forecasting class attendance.

Features
- Data extraction from CRM REST API
- ETL pipeline
- Raw and staging layers stored as Parquet
- Data transformation with Pandas
- PostgreSQL data warehouse
- SQL analytics
- Exploratory Data Analysis (EDA)
- Attendance forecasting using Machine Learning

Technology Stack
- Python
- Pandas
- PostgreSQL
- SQLAlchemy
- Docker
- Parquet
- Jupyter Notebook
- Scikit-learn
- Analytics

The project includes analytical reports such as:
- attendance by weekday;
- attendance by class time;
- teacher ranking;
- revenue by dance style;
- cumulative revenue analysis.

Machine Learning

Built regression models to predict attendance.

Models:
- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor

Best model: Linear Regression

## Pipeline

CRM API (ImpulseCRM)
    ↓
Extract (python/requests)
    ↓
RAW Parquet
    ↓
Transform (pandas)
    ↓
STAGING Parquet
    ↓
Load (pandas)
    ↓
PostgreSQL
    ↓
SQL / Jupyter EDA / Analytics
    ↓
Machine Learning

## Run

#### From project root

docker compose -f pandas_pipeline/docker-compose.yml up -d

python pandas_pipeline/etl_pipeline.py