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
    database: "test"      
    username: "1eW91cl91c2VybmFtZV9iYXNlNjRfZW5jb2RlZA=="   # Base64 encoded username
    password: "1eW91cl9wYXNzd29yZF9iYXNlNjRfZW5jb2RlZA=="   # Base64 encoded password    
    port:  3306     
```

## How To Load ServiceNow Incident Data to MySQL Database.
**Statement** : Load recent 100 data records from `incident` table of ServiceNow instance named `dev5786` to MySQL database named `test`. Before Loading mask the `number` column
of `incident` table.

In the above example `config_default.yaml` file we have registered a servicenow connection named `development` that points to ServiceNow instance `dev5786` and 
also we have defined a connection named `mysql_test` for database `test` located at localhost.

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
    "encrypt": {
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

#####2. loading data from SERVICENOW to all DATABASES:
In this use-case we will load the data from `servicenow` to all the available databases in `CLOUDTDMS`

```markdown
STREAM = {
    "title": "load_servicenow_to_all_databases",
    "number": 100,
    "frequency": "once",
    "source": {
        "servicenow": [
            {"connection": "development", "table": "incident"}
        ]
    },
    "destination": {
         "mysql": [
             {"connection": "mysql_development", "table": "mysql_incident"}
         ],
        "postgres": [
            {"connection": "postgres_development", "table": "postgres_incident"}
         ],
        "mssql": [
            {"connection": "mysql_developemnt", "table": "mssql_incident"}
        ]
    },
    "output_schema": {
        "servicenow.development.incident.number",
        "servicenow.development.incident.description",
        "servicenow.development.incident.short_description",
        "servicenow.development.incident.caller_id"
    }
}
```

For `mysql` the entry in `config_default.yaml` file looks like:
```markdown
mysql:
  mysql_development:       
    host: "127.0.0.1"          
    database: "YOUR DATABASE NAME"      
    username: "YOUR USERNAME IN BASE64 ENCRYPTED HERE"     
    password: "YOUR PASSWORD IN BASE64 ENCRYPTED HERE"      
    port:  3306 
```     

For `mssql` the entry in `config_default.yaml` file looks like:
```markdown
mssql:
  mssql_development:       
    host: "127.0.0.1"          
    database: "YOUR DATABASE NAME"      
    username: "YOUR USERNAME IN BASE64 ENCRYPTED HERE"     
    password: "YOUR PASSWORD IN BASE64 ENCRYPTED HERE"      
    port:  1433 
```     

For `postgres` the entry in `config_default.yaml` file looks like:
```markdown
postgres:
  postgres_development:       
    host: "127.0.0.1"          
    database: "YOUR DATABASE NAME"      
    username: "YOUR USERNAME IN BASE64 ENCRYPTED HERE"     
    password: "YOUR PASSWORD IN BASE64 ENCRYPTED HERE"      
    port:  5432 
```  

#####3. loading masked data from SERVICENOW to mysql:
In this use-case we load masked data into the `mysql` database

```markdown
STREAM = {
    "title": "load_masked_data",
    "format": "csv",
    "number": 10,
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
     "source": {
         "servicenow": [
             {"connection": "development", "table": "incident", "limit": 20}
         ],
     },
    "destination": {
         "mysql": [
             {"connection": "mysql_development", "table": "mysql_table"}
         ],
        "postgres": [
            {"connection": "postgres_development", "table": "postgres_table"}
         ],
        "mssql": [
            {"connection": "mysql_developemnt", "table": "mssql_table"}
        ]
    "substitute": {
        "servicenow.development.incident.caller_id": {"type": "advanced.custom_list",
                                                       "set_val": "System Administrator"},
    },
    "encrypt": {
        "servicenow.development.incident.description"
    },
    "mask_out": {
        "postgres.tdms_test.synthetic_source.name"
    },
    "shuffle": {
        "servicenow.development.incident.number"
    },
    "output_schema": {
        "servicenow.development.incident.caller_id",
        "servicenow.development.incident.number",
        "servicenow.development.incident.country",
        "servicenow.development.incident.description",
        "servicenow.development.incident.short_description",
        "postgres.tdms_test.synthetic_source.name"
    }

}  
```

In the above configuration, `substitute`, `encrypt`, `mask_out` and `shuffle` are used as data masking attributes.
In the beginning of the configuration script `encryption` is used as a encryption technique for `encrypt` data masking attribute.
Similarly  `mask` is used for `mask_out` data masking attribute.
Now when data is downloaded from the `servicenow`, column `description` will encrypted by using `caesar` method,
column `caller_id` will be replaced with `System Administrator`, column `name` will be masked with `*` and 
column `number` will be shuffled.
The number of columns stored in the `mysql` database depends upon the columns in `output_schema`.

In the same way we can load the `synthetic` data to the databases. The configuration is gven below:


```markdown
STREAM = {
    "title": "load_masked_data",
    "format": "csv",
    "number": 10,
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
             {"connection": "mysql_development", "table": "mysql_table"}
         ],
        "postgres": [
            {"connection": "postgres_development", "table": "postgres_table"}
         ],
        "mssql": [
            {"connection": "mysql_developemnt", "table": "mssql_table"}
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




