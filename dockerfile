FROM apache/airflow:2.7.3-python3.11

USER airflow

RUN pip install --no-cache-dir \
    pandas==2.1.4 \
    pyarrow==14.0.2 \
    numpy==1.26.2 \
    openpyxl==3.1.2 \
    xlrd==2.0.1

WORKDIR /opt/airflow
