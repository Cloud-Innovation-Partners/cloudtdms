# Base Image
FROM python:3.6-stretch

COPY entrypoint.sh /entrypoint.sh

# Create Project Directory
RUN mkdir /opt/cloudtdms
WORKDIR /opt/cloudtdms

#Install Dependencies
RUN pip install faker
RUN pip install apache-airflow
RUN pip install cryptography
RUN pip install onetimepad
RUN pip install pycrypto

# Copy selected subdirectories only
RUN mkdir scripts
RUN mkdir system
COPY system/dags system/dags
COPY system/airflow.cfg system/airflow.cfg
COPY system/cloudtdms system/cloudtdms
COPY system/__init__.py system/__init__.py
COPY __init__.py .
RUN mkdir user-data
RUN mkdir data

# Environment
ENV AIRFLOW_HOME="/opt/cloudtdms/system"

ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]
