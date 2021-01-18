# Administration of CloudTDMS
In this section we shall describe the ways you can administrate `CloudTDMS`. Administration will depend on the type of installation you have chosen.
please refer to corresponding sections below that are relevant to your installation type.

## If you have installed CloudTDMS as Service via INSTALL script:
If you have chosen to install CloudTDMS as Service on your server using INSTALL script then you will have two services running on your machine

- airflow-webserver.service
- airflow-scheduler.service

In order to have up and running CloudTDMS, you must have both the services running on your system. To check the state of these services you can use following commands

#### To check the status of the services
Use following commands to find the status of the services on your machine

    $ sudo service airflow-webserver status
    $ sudo service airflow-scheduler status
    
Your services may be either in `running` (start) or `inactive` (stopped) state

The output of the above commands will look like this, If they are active and in running state

For Webserver:

    ● airflow-webserver.service - airflow web server service
      Loaded: loaded (/etc/systemd/system/airflow-webserver.service; enabled; vendor preset: enabled)
      Active: active (running) since Thu 2021-01-14 05:31:54 UTC; 28s ago

For Scheduler:

    ● airflow-scheduler.service - airflow scheduler service
      Loaded: loaded (/etc/systemd/system/airflow-scheduler.service; enabled; vendor preset: enabled)
      Active: active (running) since Thu 2021-01-14 05:31:54 UTC; 7min ago

If the services are not active or are stopped then the output will appear somewhat like this

For Webserver:

    ● airflow-webserver.service - airflow web server service
      Loaded: loaded (/etc/systemd/system/airflow-webserver.service; enabled; vendor preset: enabled)
      Active: inactive (dead) since Thu 2021-01-14 05:44:41 UTC; 3s ago

For Scheduler:

    ● airflow-scheduler.service - airflow scheduler service
      Loaded: loaded (/etc/systemd/system/airflow-scheduler.service; enabled; vendor preset: enabled)
      Active: inactive (dead) since Thu 2021-01-14 05:48:05 UTC; 2s ago


There may be cases when your service might be disabled, which means they are yet to be loaded by the `systemd` on the backgroud services list. If your services
are disabled you cant start or stop them unless you enable them first. 

To check if the service is enabled or disable you can again use the same commands but this time in output you need to check this line

    Loaded: loaded (/etc/systemd/system/airflow-scheduler.service; disabled; vendor preset: enabled)
    
Notice the difference between the different outputs. You will find the Loaded state shows disabled instead of enabled

Inorder to enable a service use following commands

    $ sudo systemctl enable airflow-webserver.service
    $ sudo systemctl enable airflow-scheduler.service


#### To start the services
Once you have checked the state of the services, You can use the following commands to start the services

    $ sudo service airflow-webserver start
    $ sudo service airflow-scheduler start
    
#### To stop the services
Use following commands to stop the services.

    $ sudo service airflow-webserver stop
    $ sudo service airflow-scheduler stop
    

## Logs
To check the logs of the services you can use following commands

#### check logs of airflow-webserver.service
To check `tail` of the webserver log file, use following command

    $ journalctl -u airflow-webserver.service

To check the running logs use following command

    $ journalctl -f -u airflow-webserver.service
    

#### check logs of airflow-scheduler.service
To check `tail` of the scheduler log file, use following command

    $ journalctl -u airflow-scheduler.service

To check the running logs use following command

    $ journalctl -f -u airflow-scheduler.service














