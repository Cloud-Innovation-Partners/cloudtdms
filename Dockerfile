# Base Image
FROM apache/airflow

# Create Project Directory

RUN rm -r /opt/airflow/dags
RUN rm -r /opt/airflow/logs

WORKDIR /opt/airflow

##Install Dependencies
RUN pip install --user faker
#
## Copy selected subdirectories only
#
RUN mkdir scripts
RUN mkdir system
COPY system/dags system/dags
COPY system/airflow.cfg system/airflow.cfg
COPY system/cloudtdms system/cloudtdms
COPY system/__init__.py system/__init__.py
COPY __init__.py .
RUN mkdir user-data
RUN mkdir data
## Environment
ENV AIRFLOW_HOME="/opt/airflow/system"


RUN airflow initdb
