<pre>
  ____ _                 _ _____ ____  __  __ ____  
 / ___| | ___  _   _  __| |_   _|  _ \|  \/  / ___| 
| |   | |/ _ \| | | |/ _` | | | | | | | |\/| \___ \ 
| |___| | (_) | |_| | (_| | | | | |_| | |  | |___) |
 \____|_|\___/ \__,_|\__,_| |_| |____/|_|  |_|____/    version 0.1
</pre>

![license](https://img.shields.io/badge/license-Apache2-blue) ![Github docs](https://img.shields.io/badge/docs-passing-green) ![python](https://img.shields.io/badge/python-3.6-blue)


### CloudTDMS - Test Data Management Service
CloudTDMS is a test data management tool that let's you generate realistic synthetic data in real time. Besides synthetic 
data generation `CloudTDMS` can be used as a potential tool for data masking and obfuscation of production data. 

### What is it for?
With `CloudTDMS` you can ?
+ Generate Realistic Synthetic Data
+ Generate Synthetic Data From Custom Seed File
+ Anonymize Personal Identifiable Information (PII) In Data
+ Mask Sensitive Data To Ensure Compliance & Security
+ Encrypt Private Data 
+ Generate Synthetic Data In Real Time.

# Installation

**Pre-Requisite :** 

`CloudTDMS` requires `python3` and `pip3` for installation, in-case you have `python2` please follow the steps specified to install `python3`

**Install python3 on Ubuntu18.04**
+ If you are using Ubuntu18.04, there is a possibility you already have `python3` installed. By default Ubuntu has `python2` as default python
  interpreter but it also has `python3` installed. In case `python3` is not available you can install it with following command
        
        sudo apt install python3
        
+ Once `python3` is intalled you need to set it as default python, for this hit the following commands inside your terminal with `sudo` privileges

        sudo mv /usr/bin/python /usr/bin/python_bk
        sudo ln -s /usr/bin/python3 /usr/bin/python

+ To install `pip3` hit the below command inside your terminal

        sudo apt install python3-pip
        
### Installation Steps :
You can use anyone of the methods to install and run the service.

**Docker Image :**

You can start using `CloudTDMS` with docker, ensure you have `docker-compose` installed.

1. Simply clone the repo from the github:

         git clone https://github.com/Cloud-Innovation-Partners/cloudtdms.git
         
2. Change directory to `cloudtdms`

         cd cloudtdms
         
3. Build and run the service using following command

         docker-compose up --build
         
**Installation Script :**

>**Note :** *Installation script is available for Ubuntu 18.04 only, In case you are using any other OS, you can go for either
             manual or docker installation.*
             
`CloudTDMS` accompanies an installation script that can be used to install and run the service on Ubuntu 18.04. The script
will run as a service on ubuntu machine.

1. Simply clone the repo from the github:

         git clone https://github.com/Cloud-Innovation-Partners/cloudtdms.git
         
2. Change directory to `cloudtdms`

         cd cloudtdms
         
3. Run the install script inside `cloudtdms` directory

         sudo ./INSTALL

**Manual Installation :**

1. Clone the repo using github url
    
        git clone https://github.com/Cloud-Innovation-Partners/cloudtdms.git
    
2. If you want to install `cloudtdms` inside python virtual environment then follow `Step 2` else you can skip this step
        
    - Create a virtual environment inside the folder `cloudtdms`, using below command
    
            virtualenv -p /usr/bin/python .env
      
      You will see a folder named `.env` inside `cloudtdms` folder
    
    - Open `activate` file Using nano 
    
            nano .env/bin/activate
    
    - Edit `.env/bin/activate` file, add the below line to the end of the file, 
      
      >**Note** : Remember to replace **`<YOUR_PROJECT_PATH>`** with absolute path of parent directory of `cloudtdms` folder
           
           export AIRLFOW_HOME="<YOUR_PROJECT_PATH>/cloudtdms/system"
    
   - Activate the `virtualenv`, with the following command
            
           source .env/bin/activate
           
3. `cd` to the project directory and install project dependencies using `requirements.txt` file inside `cloudtdms` folder using following command

        python -m pip install -r requirements.txt
        
4. If you are using python virtual environment as described in `Step2` then you can skip this step.
   
   - Set `AIRFLOW_HOME` as environment variable, open file `/etc/environment` and add the below line to the end of the file

     > **Note** : Remember to replace **`<YOUR_PROJECT_PATH>`** with absolute path of parent directory of `cloudtdms` folder**

         AIRFLOW_HOME="<YOUR_PROJECT_PATH>/cloudtdms/system"
         
   - Update your session with environment changes
         
         source /etc/environment
           
5. Initialize Airflow Database

        airflow initdb
    
6. Start airflow webserver

        airflow webserver
    
7. Start airflow scheduler

        airflow scheduler
        

## How To Use ?

Place your data generation scripts inside `scripts` folder and your corresponding output data files will be generated inside `data` folder.

   *example script*
   
        STREAM = {
        "number": 1000,
        "title": 'Stream2',
        "format": "csv",
        "frequency": "once",
        "schema": [
            {"field_name": "fname", "type": "personal.first_name", "locale": "fa_IR"},
            {"field_name": "lname", "type": "personal.last_name",},
            {"field_name": "sex", "type": "personal.gender"},
            {"field_name": "email", "type": "personal.email_address"},
            {"field_name": "user", "type": "personal.username"},
            {"field_name": "univ", "type": "personal.university"},
            {"field_name": "lang", "type": "personal.language"},
        ]
       }

9. You can access the UI of the AIRFLOW via http://127.0.0.1:8080
