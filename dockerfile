FROM apache/airflow:latest
COPY requirements.txt /requirements.txt
RUN pip install  --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt


# docker build . --tag extending_airflow1:latest