FROM python:3.10-slim

USER root

RUN apt-get update && \
    apt-get install -y default-jre && \
    apt-get clean

WORKDIR /app

COPY pyspark_pipeline/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# COPY . .
COPY .env .
COPY drivers ./drivers
COPY pyspark_pipeline ./pyspark_pipeline
COPY shared ./shared

# CMD ["python", "etl_pipeline.py"]
CMD ["python", "-m", "pyspark_pipeline.etl_pipeline"]