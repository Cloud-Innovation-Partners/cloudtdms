# Base Image
FROM python:3.6-stretch

COPY entrypoint.sh /entrypoint.sh

# Create Project Directory
RUN mkdir /opt/cloudtdms
WORKDIR /opt/cloudtdms

# Copy requirements.txt
COPY requirements.txt /requirements.txt

#Install Dependencies
RUN pip install -r /requirements.txt

# Copy selected subdirectories only
RUN mkdir config
RUN mkdir system
COPY system/dags system/dags
COPY system/airflow.cfg system/airflow.cfg
COPY system/cloudtdms system/cloudtdms
COPY system/__init__.py system/__init__.py
COPY __init__.py .
COPY config_default.yaml .
RUN mkdir user-data
RUN mkdir data
RUN mkdir profiling_reports
RUN mkdir profiling_data

# Environment
ENV AIRFLOW_HOME="/opt/cloudtdms/system"

ENTRYPOINT ["/entrypoint.sh"]
CMD ["scheduler"]
