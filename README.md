<pre>
  ____ _                 _ _____ ____  __  __ ____  
 / ___| | ___  _   _  __| |_   _|  _ \|  \/  / ___| 
| |   | |/ _ \| | | |/ _` | | | | | | | |\/| \___ \ 
| |___| | (_) | |_| | (_| | | | | |_| | |  | |___) |
 \____|_|\___/ \__,_|\__,_| |_| |____/|_|  |_|____/    version 0.1
</pre>

![license](https://img.shields.io/badge/license-Apache2-blue) ![Github docs](https://img.shields.io/badge/docs-passing-green) ![python](https://img.shields.io/badge/python-3.6-blue)


### CloudTDMS - Test Data Management Service
CloudTDMS is a test data management tool that lets you generate realistic synthetic data in real-time. Besides synthetic 
data generation, `CloudTDMS` can be used as a potential tool for data masking and obfuscation of production data. 

### What is it for?
With `CloudTDMS` you can?
+ Generate Realistic Synthetic Data
+ Generate Synthetic Data From Custom Seed File
+ Identify Personally Identifiable Information In Data
+ Anonymize Personally Identifiable Information (PII) In Data
+ Mask Sensitive Data To Ensure Compliance & Security
+ Encrypt Private Data 
+ Generate Synthetic Data In Real-Time.
+ Generate Data Profiling Reports

# Table of Contents

**First Steps**

* **[Installation](docs/installation.md)**
    - [Prerequisites](docs/installation.md#pre-requisite)
    - [Installation](docs/installation.md#installation)
        - [Docker Installation](docs/installation.md#docker-image)
        - [Installation Script](docs/installation.md#installation-script)
        - [Manual Installation](docs/installation.md#manual-installation)
    
**Getting Started**

* **[How To Use](README.md#how-to-use-)**
* **[Configuration](docs/configuration_script.md)**
* **[Providers](docs/providers.md)**
* **[Data Masking](docs/data_masking.md)**
* **[Data Profiling](docs/data_profiling.md)**
* **[Email Notifications](docs/email_notify.md)**
* **[Advanced Users & Troubshooting](docs/installation.md#advanced-users--troubleshooting)**



## How To Use?

### Synthetic Data Generation

Create a file with `.py` extension inside the `config` directory of `cloudtdms`. 

>**Note :** `config` directory can be found inside the `cloudtdms` project folder, But if you have installed the solution via INSTALLATION script. The `config` directory will be present @ `/home/cloudtdms`

This file will serve as a configuration 
to generate synthetic data. `CloudTDMS` expects a python script with a `STREAM` variable of type dictionary containing key-value 
pairs of configuration attributes defining your data generation scheme. Below is an example configuration containing various
configuration attributes that are used to define the data generation process. You can find the details of all the configuration
attributes supported by this version of cloudtdms in the [Configuration Attributes](docs/configuration_script.md) section.

Here we shall quickly go through the example configuration below to get the idea of data generation script.  

**example configuration**
   
```python
STREAM = {
        "number": 1000,
        "title": 'synthetic_data',
        "format": "csv",
        "frequency": "once",
        "schema": [
            {"field_name": "fname", "type": "personal.first_name"},
            {"field_name": "lname", "type": "personal.last_name",},
            {"field_name": "sex", "type": "personal.gender"},
            {"field_name": "email", "type": "personal.email_address"},
            {"field_name": "country", "type": "location.country"},
            {"field_name": "city", "type": "location.city"},
        ]
       }
```

+ `number` defines the number of records to be generated, In this case, we ask `cloudtdms` to generate 1000 records
+ `title` defines the name of the generated file, In this case, the generated data file will be inside `data` folder of 
          `cloudtdms` and it will be named as `synthetic_data.csv`.
+ `format` defines the format for the output file. the current version supports data generation only in `CSV` format.
+ `frequency` defines how often data should be generated, It takes a cron value such as `once`, `hourly`, `daily`, `monthly` etc.
+ `schema` defines the schema of the output data file, each entry corresponds to a specific data generator defined in `CloudTDMS`. Here 
           the list contains six entries, means output file will have six columns with names `fname`, `lname`, `sex`, `email`
           `country`, `city`. The values for each column will be generated by a generator function defined in the `type` attribute
           of the list entry. that means value for `fname` will be generated by **`first_name`** generator function from the 
           **`personal`** provider, similarly, the value for `country` will be generated by **`country`** generator function from the
           **`location`** provider. A list of all the **providers** and available generators can be found in the [Providers](docs/providers.md) section
       
### Data Profiling

In order to generate profiling reports for your data, you simply need to place your `CSV` data file inside the `profiling-data`
directory of the project. `CloudTDMS` will stage the data for profiling and generate reports inside the `profiling_reports`
directory. Please refer [Data Profiling](docs/data_profiling.md) section for details about the types of reports generated.

>Note : profiling reports are generated for CSV data only, CloudTDMS supports CSV files only in current version


>**Note :** `profiling_data` directory can be found inside the `cloudtdms` project folder, But if you have installed the solution via INSTALLATION script. The `profiling_data` directory will be present @ `/home/cloudtdms`

### Data Masking

With `CloudTDMS` you can perform various data masking operations besides generating synthetic data. You can:

+ Anonymize sensitive data with synthetic data
+ Encrypt data with available encryption techniques
+ Perform masking using pseudo characters
+ Shuffle data
+ Perform nullying and deletion operations

Please refer [Data Masking](docs/data_masking.md) section for details about the usage and different masking operations available.


# License
Copyright 2020 [Cloud Innovation Partners](http://cloudinp.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
