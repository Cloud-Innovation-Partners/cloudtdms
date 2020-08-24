#!/usr/bin/python

#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import sys
import os
import pwd
import subprocess

AIRFLOW_HOME = f"{os.path.abspath(os.path.dirname(__file__))}/system"

TEMPLATE = """
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# “License”); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# “AS IS” BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
[Unit]
Description={{ DESCRIPTION }}
After=network.target {{ AFTER }}
Wants={{ WANTS }}
[Service]
EnvironmentFile=/etc/environment
User={{ USER }}
Group={{ GROUP }}
Type=simple
ExecStart= {{ EXE }}
Restart={{ RESTART }}
RestartSec=5s
PrivateTmp=true
[Install]
WantedBy=multi-user.target
"""


def check_python_version():
    if sys.version_info.major >= 3:
        print("Python version : {}.{}.{}".format(
            sys.version_info.major, sys.version_info.minor, sys.version_info.micro
        ))
    else:
        print("""
_______________________________________________________________
                INSTALLATION TERMINATED                        
_______________________________________________________________
You have Python version : {}.{}.{}
cloudtdms uses latest version of Airflow, which requires you to have
python 3.6 or above, please make sure you have requirements full filled
for further details checkout the docs section
""".format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro).upper())
        exit(1)


def install_packages_from_requirement_file():
    print('Installing requirements...')
    basepath = os.path.abspath(os.path.dirname(__file__))
    subprocess.check_call(["sudo", "-H", "/usr/bin/python", "-m", "pip", "install", "-r", f"{basepath}/requirements.txt"])


def set_airflow_home_as_environment():

    global AIRFLOW_HOME

    os.environ["AIRFLOW_HOME"] = AIRFLOW_HOME

    subprocess.Popen(["sed -i '/AIRFLOW_HOME/d' /etc/environment"],
                     universal_newlines=True, stdout=subprocess.PIPE, shell=True,
                     executable="/bin/bash").communicate()

    subprocess.Popen(["sed -i '0,/PATH/ a\\AIRFLOW_HOME=\\\"{}\\\"' /etc/environment".format(AIRFLOW_HOME)],
                     universal_newlines=True, stdout=subprocess.PIPE, shell=True,
                     executable="/bin/bash").communicate()

    subprocess.Popen(["source /etc/environment"],
                     universal_newlines=True, stdout=subprocess.PIPE, shell=True,
                     executable="/bin/bash").communicate()


def airflow_resetdb():
    print('Resetting airflow meta-database')
    subprocess.Popen(["airflow resetdb -y"],
                     universal_newlines=True, stdout=subprocess.PIPE, shell=True,
                     executable='/bin/bash').communicate()


def airflow_initdb():
    print('Initializing airflow meta-database')
    env = os.environ
    env['AIRFLOW_HOME'] = AIRFLOW_HOME
    subprocess.Popen(["airflow initdb"], cwd=os.getcwd(), env=env,
                     universal_newlines=True, stdout=subprocess.PIPE, shell=True,
                     executable='/bin/bash').communicate()


def create_service_user_group():
    print('Creating group cloudtdms...')
    subprocess.Popen(["groupadd -r --system cloudtdms"],
                     universal_newlines=True, stdout=subprocess.PIPE, shell=True,
                     executable='/bin/bash').communicate()

    print('Creating user cloudtdms...')
    subprocess.Popen(["useradd --shell=/bin/false --no-create-home -g cloudtdms -r cloudtdms"],
                     universal_newlines=True, stdout=subprocess.PIPE, shell=True,
                     executable='/bin/bash').communicate()

    user_id = os.environ['SUDO_UID']
    subprocess.Popen([f"usermod -aG cloudtdms {pwd.getpwuid(int(user_id)).pw_name}"],
                     universal_newlines=True, stdout=subprocess.PIPE, shell=True,
                     executable='/bin/bash').communicate()


def change_ownership_permissions():
    dirname = os.getcwd()
    subprocess.Popen([f"chown -R cloudtdms:cloudtdms {dirname} & chmod -R ug+rw {dirname}"],
                     universal_newlines=True, stdout=subprocess.PIPE, shell=True,
                     executable='/bin/bash').communicate()


def create_system_service_entries():
    from jinja2 import Template
    import shutil

    with open('/etc/systemd/system/airflow-webserver.service', 'w') as f:
        template = Template(TEMPLATE)

        output = template.render(

            DESCRIPTION='airflow web server service',
            USER="cloudtdms",
            GROUP="cloudtdms",
            EXE=str(shutil.which('airflow')) + ' webserver',
            RESTART='on-failure'
        )

        f.write(output)

    with open('/etc/systemd/system/airflow-scheduler.service', 'w') as f:
        template = Template(TEMPLATE)

        output = template.render(

            DESCRIPTION='airflow scheduler service',
            USER="cloudtdms",
            GROUP="cloudtdms",
            EXE=str(shutil.which('airflow')) + ' scheduler',
            RESTART='always'
        )

        f.write(output)


def reload_enable__airflow_webserver_service():
    print("Enabling Airflow Web Server....")

    subprocess.Popen(["systemctl daemon-reload ; systemctl enable airflow-webserver.service"],
                     universal_newlines=True, stdout=subprocess.PIPE, shell=True,
                     executable='/bin/bash').communicate()


def reload_enable_airflow_scheduler_service():
    print("Enabling Airflow Scheduler....")

    subprocess.Popen(["systemctl daemon-reload ; systemctl enable airflow-scheduler.service"],
                     universal_newlines=True, stdout=subprocess.PIPE, shell=True,
                     executable='/bin/bash').communicate()


def start_airflow():
    print("starting CloudTDMS...")
    subprocess.Popen(["service airflow-webserver start"],
                     universal_newlines=True, stdout=subprocess.PIPE, shell=True,
                     executable='/bin/bash').communicate()
    subprocess.Popen(["service airflow-scheduler start"],
                     universal_newlines=True, stdout=subprocess.PIPE, shell=True,
                     executable='/bin/bash').communicate()


def modify_configuration():
    print("replacing values in configuration...")
    basepath = os.path.abspath(os.path.dirname(__file__))
    subprocess.Popen(["sed -i 's|/opt/cloudtdms|{}|g' system/airflow.cfg".format(basepath)],
                     universal_newlines=True, stdout=subprocess.PIPE, shell=True,
                     executable='/bin/bash').communicate()


if __name__ == "__main__":
    check_python_version()
    install_packages_from_requirement_file()
    set_airflow_home_as_environment()
    modify_configuration()
    create_service_user_group()
    change_ownership_permissions()
    if os.path.exists(f"{AIRFLOW_HOME}/airflow.db"):
        airflow_resetdb()
    else:
        airflow_initdb()
    change_ownership_permissions()
    create_system_service_entries()
    reload_enable__airflow_webserver_service()
    reload_enable_airflow_scheduler_service()
    start_airflow()
