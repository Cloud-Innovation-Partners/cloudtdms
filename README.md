# CloudTDMS

CloudTDMS - Test Data Management Service

# Installation

**Pre-Requisite :** 

`cloudtdms` requires `python3` and `pip3` installation, in-case you have `python2` please follow the steps specified to install `python3`

**Ubuntu18.04**
+ If you are using Ubuntu18.04, there is a possibility you already have `python3` installed. By default Ubuntu has `python2` as default python
  interpreter but it also has `python3` installed. In case `python3` is not available you can install it with following command
        
        sudo apt install python3
        
+ Once `python3` is intalled you need to set it as default python, for this hit the following commands inside your terminal with `sudo` privileges

        sudo mv /usr/bin/python /usr/bin/python_bk
        sudo ln -s /usr/bin/python3 /usr/bin/python

+ To install `pip3` hit the below command inside your terminal

        sudo apt install python3-pip
        
# Steps

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
        
8. Place your data generation scripts inside `scripts` folder and your corresponding output data files will be generated inside `data` folder.

9. You can access the UI of the AIRFLOW via http://127.0.0.1:8080
