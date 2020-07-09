# CloudTDMS

CloudTDMS - Test Data Management Service

# Installation

Clone the repo using github url
    
    git clone https://github.com/Cloud-Innovation-Partners/cloudtdms.git
    
Create a virtual environment inside the folder `cloudtdms`

    virtualenv -p /usr/bin/python .env
    
Edit `.env/bin/activate` file, add `AIRFLOW_HOME` PATH at the end of the file

    export AIRLFOW_HOME=<YOUR_PATH_PROJECT>/cloudtdms/system
    
Activate the `virtualenv`

    source .env/bin/activate
    
Initialize Airflow DB

    airflow initdb
    
Start airflow webserver

    airflow webserver
    
Start airflow scheduler

    airflow scheduler
