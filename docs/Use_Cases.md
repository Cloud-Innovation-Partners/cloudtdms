# CloudTDMS Example Usecases

This section describes some usecases of `CloudTDMS`. Each example has a `configuration` script provided which defines
a specific usecase like uploading synthetic data to servicenow or fetching production data from servicenow for masking etc.

Below is an instance of `config_default.yaml` file with all the connections defined that are to be used in the example usecases.
In case you are using any of the configuration files below, please make sure you change the values for connections inside the provided
`config_default.yaml` file as per your need.

```yaml
email:
  to: ""                    # Receiver Email Address
  from: ""                  # Sender Email Address
  smtp_host: ""             # SMTP Host Address
  smtp_port: 587            # SMTP PORT, 465 (SSL), 587(Legacy) or 25 (some providers block port 25)
  smtp_ssl: False           # IF Smtp_port is 465 then set smtp_ssl to True
  username: ""
  password: ""
  subject: "Data Profiling"

encryption:
  type: "caesar"            # Default encryption type to be used for data_masking
  key: "CloudTDMS@2020"     # Default encryption key to be used for data_masking

mask:
  with: "x"
  characters: 6
  from: "mid"

servicenow:
  development:
    host: "dev5786"                                        # ServiceNow instance name
    username: "eW91cl91c2VybmFtZV9iYXNlNjRfZW5jb2RlZA=="   # Base64 encoded username
    password: "eW91cl9wYXNzd29yZF9iYXNlNjRfZW5jb2RlZA=="   # Base64 encoded password

mysql:
  mysql_test:       
    host: "127.0.0.1"          
    database: "mysql_db"      
    username: "1eW91cl91c2VybmFtZV9iYXNlNjRfZW5jb2RlZA=="   # Base64 encoded username
    password: "1eW91cl9wYXNzd29yZF9iYXNlNjRfZW5jb2RlZA=="   # Base64 encoded password    
    port:  3306     

mssql:
  mssql_test:       
    host: "127.0.0.1"          
    database: "mssql_db"      
    username: "1eW91cl91c2VybmFtZV9iYXNlNjRfZW5jb2RlZA=="   # Base64 encoded username
    password: "1eW91cl9wYXNzd29yZF9iYXNlNjRfZW5jb2RlZA=="   # Base64 encoded password    
    port:  1433     

postgres:
  postgres_test:       
    host: "127.0.0.1"          
    database: "postgres_db"      
    username: "1eW91cl91c2VybmFtZV9iYXNlNjRfZW5jb2RlZA=="   # Base64 encoded username
    password: "1eW91cl9wYXNzd29yZF9iYXNlNjRfZW5jb2RlZA=="   # Base64 encoded password    
    port:  5432

sftp:
  sftp_test:       
    host: "10.0.1.5"          
    username: "1eW91cl91c2VybmFtZV9iYXNlNjRfZW5jb2RlZA=="   # Base64 encoded username
    password: "1eW91cl9wYXNzd29yZF9iYXNlNjRfZW5jb2RlZA=="   # Base64 encoded password      
    port: "22"         
    ssh_public_key: ""  # path to ssh public key
    passphrase: ""

```

##How To Load ServiceNow Incident Data to MySQL Database.
**Statement** : Load recent 100 data records from `incident` table of ServiceNow instance named `dev5786` to MySQL database named `mysql_db`. Before loading mask the `number` column
of `incident` table.

In the above example `config_default.yaml` file we have registered a servicenow connection named `development` that points to ServiceNow instance `dev5786` and 
also we have defined a connection named `mysql_test` for database `mysql_db` located at localhost.

Below configuration performs the task defined by above statement:
 
```python
STREAM = {
    "title": "load_servicenow_incident_to_mysql_database",
    "number": 100,
    "frequency": "once",
    "mask": {
        "with": "x",
        "characters": 8,
        "from": "mid"
    },
    "source": {
        "servicenow": [
            {"connection": "development", "table": "incident"}
        ]
    },
    "destination": {
         "mysql": [
             {"connection": "mysql_test", "table": "mysql_incident"}
         ]
    },
    "mask_out": {
        "servicenow.development.incident.number"
    }, 
    "output_schema": {
        "servicenow.development.incident.number",
        "servicenow.development.incident.description",
        "servicenow.development.incident.short_description",
        "servicenow.development.incident.caller_id",
    }
}
```

##How To Load ServiceNow Incident Data to all Database.
**Statement** : Load recent 100 data records from `incident` table of ServiceNow instance named `dev5786` to MySQL, MSSQL and POSTGRES databases named `mysql_db`, `mssql_db`and `postgres_db` respectively. Before loading mask the `number` column
of `incident` table.

In the above example `config_default.yaml` file we have registered a servicenow connection named `development` that points to ServiceNow instance `dev5786` and 
also we have defined a connections named `mysql_test`, `mssql_test`, `postgres_test` for database `mysql_db`, `mssql_db`and `postgres_db` respectively located at localhost.

Below configuration performs the task defined by above statement:

```markdown
STREAM = {
    "title": "load_servicenow_to_all_databases",
    "number": 100,
    "frequency": "once",
     "mask": {
            "with": "x",
            "characters": 8,
            "from": "mid"
     },
    "source": {
        "servicenow": [
            {"connection": "development", "table": "incident"}
        ]
    },
    "destination": {
         "mysql": [
             {"connection": "mysql_test", "table": "mysql_incident"}
         ],
        "postgres": [
            {"connection": "postgres_test", "table": "postgres_incident"}
         ],
        "mssql": [
            {"connection": "mssql_test", "table": "mssql_incident"}
        ]
    },
  "mask_out": {
        "servicenow.development.incident.number"
    },
    "output_schema": {
        "servicenow.development.incident.number",
        "servicenow.development.incident.description",
        "servicenow.development.incident.short_description",
        "servicenow.development.incident.caller_id"
    }
}
```

##How To Load Synthetic Data to all Database.
**Statement** : Load recent 100 data records from synthetic data to MySQL, MSSQL and POSTGRES databases named `mysql_db`, `mssql_db`and `postgres_db` respectively. Before loading mask the `card` column,
encrypt the `fname` column, substitute the `ctype` column and shuffle `lname`, `passcode` of `synthetic` data.

In the above example `config_default.yaml` file we have registered connections named `mysql_test`, `mssql_test`, `postgres_test`
for database `mysql_db`, `mssql_db`and `postgres_db` respectively located at localhost.

Below configuration performs the task defined by above statement:


```python
STREAM = {
    "title": "load_synthetic_data_to_all_databases",
    "format": "csv",
    "number": 100,
    "frequency": "once",
     "encryption": {
         "type": "caesar",
         "key": "Jd28hja8HG9wkjw89yd"
     },
    "mask": {
        "with": "x",
        "characters": 4,
        "from": "end"
    },
    "synthetic":[
        {"field_name": "fname", "type": "personal.first_name", "category": "male"},
        {"field_name": "lname", "type": "personal.last_name"},
        {"field_name": "passcode", "type": "basics.password", "length": 12},
        {"field_name": "card", "type": "commerce.credit_card"},
        {"field_name": "ctype", "type": "commerce.credit_card_type"},
    ],
    "destination": {
         "mysql": [
             {"connection": "mysql_test", "table": "mysql_table"}
         ],
        "postgres": [
            {"connection": "postgres_test", "table": "postgres_table"}
         ],
        "mssql": [
            {"connection": "mysql_test", "table": "mssql_table"}
        ]
     },
    "substitute": {
        "synthetic.ctype": {"type": "advanced.custom_list",
                       "set_val": "Master Card"},
    },
    "encrypt": {
        "synthetic.fname"
    },
    "mask_out": {
        "synthetic.card"
    },
    "shuffle": {
        "synthetic.lname",
        "synthetic.passcode"
    },
    "output_schema": {
        "synthetic.fname",
        "synthetic.lname",
        "synthetic.passcode",
        "synthetic.card",
        "synthetic.ctype",
    }

}  
```

##How To Load Synthetic Data to SFTP storage.
**Statement** : Load recent 100 data records from synthetic data to SFTP server with host `10.0.1.5`. Before loading mask the `card` column,
encrypt the `fname` column, substitute the `ctype` column and shuffle `lname`, `passcode` of `synthetic` data.

In the above example `config_default.yaml` file we have registered a sftp connection named `sftp_test` for sftp server 
with host `10.0.1.5`.

Below configuration performs the task defined by above statement:


```python
STREAM = {
    "title": "load_synthetic_data_to_all_databases",
    "format": "csv",
    "number": 100,
    "frequency": "once",
     "encryption": {
         "type": "caesar",
         "key": "Jd28hja8HG9wkjw89yd"
     },
    "mask": {
        "with": "x",
        "characters": 4,
        "from": "end"
    },
    "synthetic":[
        {"field_name": "fname", "type": "personal.first_name", "category": "male"},
        {"field_name": "lname", "type": "personal.last_name"},
        {"field_name": "passcode", "type": "basics.password", "length": 12},
        {"field_name": "card", "type": "commerce.credit_card"},
        {"field_name": "ctype", "type": "commerce.credit_card_type"},
    ],
    "destination": {
         "sftp": [
             {"connection": "sftp_test", "file": "prod/test.csv"},
             {"connection": "sftp_test", "file": "dev/test.csv", "overwrite":True}
         ],
     },
    "substitute": {
        "synthetic.ctype": {"type": "advanced.custom_list",
                       "set_val": "Master Card"},
    },
    "encrypt": {
        "synthetic.fname"
    },
    "mask_out": {
        "synthetic.card"
    },
    "shuffle": {
        "synthetic.lname",
        "synthetic.passcode"
    },
    "output_schema": {
        "synthetic.fname",
        "synthetic.lname",
        "synthetic.passcode",
        "synthetic.card",
        "synthetic.ctype",
    }

}  
```



