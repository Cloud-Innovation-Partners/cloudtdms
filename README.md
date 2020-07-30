# CloudTDMS

CloudTDMS - Test Data Management Service

# Installation

1. Clone the repo using github url
    
        git clone https://github.com/Cloud-Innovation-Partners/cloudtdms.git
    
2. If you want to install `cloudtdms` inside python virtual environment then follow `Step 2` else you can skip this step
    
    
    - Create a virtual environment inside the folder `cloudtdms`, using below command
    
            virtualenv -p /usr/bin/python .env
      
      You will see a folder named `.env` inside `cloudtdms` folder
    
    - Open `activate` file Using nano 
    
            nano .env/bin/activate
    
    - Edit `.env/bin/activate` file, add the below line to the end of the file, 
      
      
      > **Note** : Remember to replace **`<YOUR_PROJECT_PATH>`** with absolute path of parent directory of `cloudtdms` folder
           
           export AIRLFOW_HOME=<YOUR_PROJECT_PATH>/cloudtdms/system
    
    - Activate the `virtualenv`, with the following command
            
           source .env/bin/activate
           
3. `cd` to the project directory and install project dependencies using `requirements.txt` file inside `cloudtdms` folder using following command

        python -m pip install -r requirements.txt
        
4. Set `AIRFLOW_HOME` as environment variable, open file `/etc/environment` and add the below line to the end of the file

   > **Note** : Remember to replace **`<YOUR_PROJECT_PATH>`** with absolute path of parent directory of `cloudtdms` folder**


        AIRFLOW_HOME=<YOUR_PROJECT_PATH>/cloudtdms/system
        
5. Initialize Airflow Database

        airflow initdb
    
6. Start airflow webserver

        airflow webserver
    
7. Start airflow scheduler

        airflow scheduler
