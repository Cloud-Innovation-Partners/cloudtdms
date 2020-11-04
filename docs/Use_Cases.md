
Below are mentioned some real world use-cases of `CLOUDTDMS`

#####1. loading datafrom SERVICENOW to MySQL DATABASE:
Currently `CLOUDTDMS` supports `MySQL`, `MSSQL` and `POSTGRES` as a database storages.

The below configuration downloads the data from `servicenow` and load it into the `MySQL` database storage.
 
```markdown
STREAM = {
    "title": "load_servicenow_to_mysql_database",
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
         ]
    },
    "output_schema": {
        "servicenow.development.incident.number",
        "servicenow.development.incident.description",
        "servicenow.development.incident.short_description",
        "servicenow.development.incident.caller_id",
    }
}
```

In above configuration `servicenow` is specified under the `source` attribute, from which we have to download the data.
`mysql` is specified under the `destination` attribute, to which we load the data.
For `servicenow` and `mysql` there are `connection`, `table` attributes associated.
`connection` represents the `entry in .yaml file` and `table` represents storage table name.

The entry in `config_default.yaml` file for `servicenow` looks like:
```markdown
servicenow:
  development:
    host: "dev007"
    username: "YOUR USERNAME IN BASE64 ENCRYPTED HERE"
    password: "YOUR PASSWORD IN BASE64 ENCRYPTED HERE"
```

Similarly for `mysql` the entry in `config_default.yaml` file looks like:
```markdown
mysql:
  mysql_development:       
    host: "127.0.0.1"          
    database: "YOUR DATABASE NAME"      
    username: "YOUR USERNAME IN BASE64 ENCRYPTED HERE"     
    password: "YOUR PASSWORD IN BASE64 ENCRYPTED HERE"      
    port:  3306 
```     

Now when the data is downloaded from the `servicenow`, we have to specify what columns are to be saved in the `mysql` database. For that purpose we use `output_schema` attribute in the configuration.
Once the columns are specified in the `output_schema` that much number of columns will be saved in the `mysql` database

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




