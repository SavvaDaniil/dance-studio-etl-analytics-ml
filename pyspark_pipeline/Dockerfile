#FROM apache/airflow:2.8.0
# FROM apache/airflow:3.0.2-python3.11

# USER root

# RUN apt-get update && \
#     apt-get install -y default-jre && \
#     apt-get clean

# USER airflow

# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# WORKDIR /opt/airflow

# COPY . .


FROM python:3.10-slim

USER root

RUN apt-get update && \
    apt-get install -y default-jre && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "etl_pipeline_pyspark.py"]