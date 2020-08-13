# Base Image
FROM apache/airflow

# Create Project Directory
USER root

RUN mkdir -p /opt/cloudtdms
RUN chown airflow:root /opt/cloudtdms

ENV PATH="/opt/cloudtdms:${PATH}"

USER airflow

WORKDIR /opt/cloudtdms

#Install Dependencies
RUN pip install --user faker

# Copy selected subdirectories only

RUN mkdir scripts
RUN mkdir system
COPY system/dags system/dags
COPY system/cloudtdms system/cloudtdms
COPY system/__init__.py system/__init__.py
COPY __init__.py .
RUN mkdir user-data
RUN mkdir data
# Environment
ENV AIRFLOW_HOME="/opt/cloudtdms/system"

RUN airflow initdb

USER root

RUN chown -R airflow:airflow /opt/cloudtdms

USER airflow

CMD ["webserver"]