# Installation

**`CloudTDMS`** uses [Apache Airflow](http://airflow.apache.org/) to orchestrate data generation work-flows. Installation 
of `CloudTDMS` requires installation of apache airflow. `CloudTDMS` has helper scripts associated for installation, You can
choose any mode of installation that suits your requirement. We recommend docker installation as its simple and easy to use.

Each installation method will run apache airflow `scheduler` in background as a container or as a service 
depending upon the type of installation you choose.

`CloudTDMS` runs Apache Airflow scheduler in background. Airflow webserver is not started by default. You can start the 
webserver if you desire to, In that case please ensure port 8080 is secured by firewall configuration. For more details
please refer [Advanced Users & Troubleshooting](installation.md#advanced-users--troubleshooting) section.   
  
## Recommended Server Spec
Its recommended to have a server with following specs

**Operating system :** Linux (Ubuntu 18.04 / Ubuntu 20.04)

**Size :** 1 vCPUs, 2 GiB memory, 10GiB storage

If your server has less then 2GiB of RAM ensure you have `swap` space initialized.


## Pre-Requisite 


`CloudTDMS` requires `python3` and `pip3` for installation, in-case you have `python2` please follow the steps specified to install `python3`

**Install python3 on Ubuntu 18.04 / 20.04**
+ Run update command

        sudo apt update
        
+ If you are using Ubuntu 18.04 or 20.04, there is a possibility you already have `python3` installed. By default Ubuntu has `python2` as default python
  interpreter but it also has `python3` installed. In case `python3` is not available you can install it with following command
        
        sudo apt install python3
        
+ Once `python3` is installed you need to set it as default python, for this hit the following commands inside your terminal with `sudo` privileges

        sudo unlink /usr/bin/python
        sudo ln -s /usr/bin/python3 /usr/bin/python

+ To install `pip3` hit the below command inside your terminal

        sudo apt install python3-pip
        
## Installation:
You can use anyone of the methods to install and run the service.

### Docker Image

**(Recommended Method)**

You can start using `CloudTDMS` with docker, ensure you have `docker-compose` installed. For details about the 
installation of `docker-engine` and `docker-compose` please refer to [Docker Site](https://docs.docker.com/engine/install/)

1. Simply clone the repo from the github:

         git clone https://github.com/Cloud-Innovation-Partners/cloudtdms.git
         
2. Change directory to `cloudtdms`

         cd cloudtdms
         
3. Build and run the service using following command

         sudo docker-compose up --build
                  
4. To stop the container your either press `CTRL+C` or run following command

         sudo docker-compose down   
                        
         
### Installation Script

>**Note :** *Installation script is available for Ubuntu 18.04 and 20.04 use only, In case you are using any other OS, you can go for either
             manual or docker installation.*
             
The installation script is used to install and run `CloudTDMS` as a service on Ubuntu server. It will create a separate
`user:group` named `cloudtdms` which will be used by the service to process and store your data. You need to place your
`configuration` files and data in the corresponding directories under `/home/cloudtdms`

1. Simply clone the repo from the github:

         git clone https://github.com/Cloud-Innovation-Partners/cloudtdms.git
         
2. Change directory to `cloudtdms`

         cd cloudtdms
         
3. Run the install script inside `cloudtdms` directory

         sudo ./INSTALL
         
4. Check the status of the airflow scheduler service using
 
         sudo service airflow-scheduler status
         
5. You can stop the service using

         sudo service airflow-scheduler stop
   
   and `restart` by replacing `stop` with `start` in above command                          

### Manual Installation

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
    
7. Start airflow scheduler

        airflow scheduler

### Advanced Users & Troubleshooting

`CloudTDMS` uses [Apache Airflow](http://airflow.apache.org/) in the backend to schedule and run your data generation scripts (`configuration`)
For each configuration file a DAG is created to run the data profiling and synthetic data generation tasks. In order to troubleshoot or rerun 
any synthetic data process you can access airflow GUI via https://127.0.0.1:8080 where you can access the logs and details about
your `configuration` such as failure status and running processes etc. 

Airflow uses port 8080 for its webserver component and it is an essential component for troubleshooting and monitoring the running
processes and tasks. `CloudTDMS` as a part of its installation does not start the airflow webserver service directly as it 
will expose 8080 port on the machine. In case you want to access airflow webserver UI, access to port `8080` must be restricted 
by filtering the inbound connections to your machine using firewall setting and port mapping.

Depending on your type of installation, use following commands to run the webserver

#### Installation Script
Installation script creates a service entry for airflow-webserver but it does not start it by default. To start the airflow
webserver you can use below command

    $ sudo service airflow-webserver start
    
To stop the webserver use following command

    $ sudo service airflow-scheduler stop    
    
#### Docker Image
If you are using docker then you can start the webserver by following commands

    $ docker exec -it <container_id> airflow webserver

You can get the running container list using following command

    $ docker ps

Example:

    $ docker exec -it 257fe4b4b9ee airflow webserver

To stop the container use `docker stop <container_id>` command

#### Manual Installation
If you have manually installed `CloudTDMS` than you can simple run following command to start the webserver

    $ airflow webserver 

#### Things To Do If Your Data or Profiling Reports are Not Generated

In such case you can follow few steps to identify the problem.

1. check your `configuration` file for syntax errors. This can be done by running your `configuration` file via a `validator`
   script provided under `validate` folder inside the project directory. place your configuration file inside the validate 
   folder and run `validate.sh` with `configuration` file as argument
   
   > **Note :** You must place your configuration file inside `validate` directory before running the validate.sh
   
       $ ./validate.sh my_configuration.py
       
   If your configuration has any syntax issues that will be identified here.
   
2. Check the log files generated by the `CloudTDMS` service. If you are using docker container to run `CloudTDMS` then check the
   logs of the container using `docker-compose logs`, The container should be running
   
       $ cd cloudtdms
       $ docker-compose logs  
       
   If you are installing `CloudTDMS` as a service on your machine then you can check the logs from `syslog` of the system
   
       $ tail -f /var/log/syslog
       
   In logs you should check If there are any `ERROR` message logged.
   
3. Check the Airflow Task logs. Hit http://127.0.0.1:8080 inside your browser you will get Airflow UI.
   click on the DAG which has DAG_ID same as `title` of your configuration file. click on the `GraphView` tab, 
   This shows you a DAG for your configuration. If any of the tasks in DAG is bordered RED that means failure
   has occurred at Task level. click on the red bordered task a pop will appear click on the `ViewLog` tab
   to see the logs of the data generating task. Check out any ERROR message to get the debug information.    
  
