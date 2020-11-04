# Data Sources & Destinations
This sections provides information about the supported data sources and destination in `CloudTDMS`
sources represent the entities that are used to feed data into the process and destinations 
represent the entities that are used to store the resultant data. 

## Supported Sources And Destinations

### Static Files
`CloudTDMS` provides support for CSV and JSON files to be used as a sources and destinations, This means you can use any
CSV or JSON file to feed data to the configuration and Also save the resultant data as CSV or JSON. In order to use a CSV
or JSON file as a source file, you need to create a connection entry for the same inside the `config_default.yaml`. A typical
instance of `config_default.yaml` file containing connection entries for CSV and JSON sources looks something like this.
```yaml
csv:
  my_connection_name_one:
    source: "/home/user/csv-data-one/example-one.csv"
    target: "/home/user/some-other-folder"
  my_connection_name_two:
    source: "/home/user/csv-data-two/example-two.csv"

json:
  my_connection_name:
    source: "/home/user/json-data/example.json"
    target: "/home/user/some-other-folder"
```
The `config_default.yaml` file contains entry for each source type, all connections related to CSV will be registered inside
`csv:` key. Above example has two connections named as `my_connection_name_one` and `my_connection_name_two` registered 
inside `csv:` key. Here `my_connection_one` and `my_connection_two` represent connection names, You can choose any name for representation
purpose. For both `csv:` and `json:` under each connection name you have two keys `source` and `target`. `source` key takes an absolute
path of CSV file present on your local machine to be used as a source file, While `target` key takes absolute directory path as a value
to represent the destination folder inside which resultant masked or synthetic data file must be stored.

Your connection name can act as both source as well as destination, depending upon the keys `source` and `target`. When
you use connection name in `source` attribute of configuration file then the file defined with`source` key in the particular connection name
is used as a source data, While as when you use connection name in `destination` attribute of configuration file then the
directory defined with the `target` key in the connection name is used as a destination for result data.

>**Note :** In case `target` is not defined `data` directory of `cloudtdms` folder will be used as a destination folder for 
> generated data. 

*Example* :
Below is an example snippet of configuration file using above CSV and JSON connections as source and destinations
```python
STREAM = {
    "source": {
        "csv": [
            {"connection": "my_connection_name_one", "delimiter": ","},
            {"connection": "my_connection_name_two", "delimiter": ","},
        ],
        "json": [
            {"connection": "my_connection_name", "type": "lines"}
        ]            
    },
    "destination": {
        "json": [
            {"connection": "my_connection_name", "type": "array"}
        ]            
    }   
}
``` 
Each connection entry in a list has a `connection` attribute that takes a connection name as a value. Besides `connection`
attribute we may also have some additional attributes specific to a source type such as `delimiter` etc. 

While defining a CSV data source connection inside `source` attribute of configuration. you can specific the delimiter value 
using `delimiter` attribute. By default `delimiter` is comma but you can specific any delimiter that is valid for reading 
your CSV data file. 

In case of destination connection, `delimiter` value will be used as a delimiting value for the result CSV file.

`CloudTDMS` does not support all JSON types. Only two JSON formats are valid to use. You can either use a JSON Array or
JSON lines as JSON source files. similarly, output data file can be either created in JSON Array format or as JSON Lines.
`type` attribute in a connection entry is used to define the type of JSON to be used. This attribute takes `array` or `lines` as a value

**Example of JSON Array**
```json
[{"title":"Dr","name":"Brian Reeves","country":"United States"},
{"title":"Honorable","name":"Glover Davies","country":"Venezuela, Bolivarian Republic of"},
{"title":"Rev","name":"Callum Ellis","country":"Mexico"},
{"title":"Mrs","name":"Wilson John","country":"France"},
{"title":"Rev","name":"Ben Carroll","country":"Brazil"}]
``` 

**Example of JSON Lines**
```json
{"title":"Dr","name":"Brian Reeves","country":"United States"}
{"title":"Honorable","name":"Glover Davies","country":"Venezuela, Bolivarian Republic of"}
{"title":"Rev","name":"Callum Ellis","country":"Mexico"}
{"title":"Mrs","name":"Wilson John","country":"France"}
{"title":"Rev","name":"Ben Carroll","country":"Brazil"}
``` 

### Databases
The current version of `CloudTDMS` provides support for MySQL, Postgres, Microsoft SQL Server databases. You can use 
databases both as source as well as destinations. Before using a database as a source or destination in configuration,
You need to register connections for the same inside `config_default.yaml` file. Connection can be registered under respective
keys such as `mysql:`, `postgres:`, `mssql:` present in `config_default.yaml` file.
A typical instance of `config_default.yaml` file containing connection entries for databases looks something like this.
Each database connection must have `host`, `database`, `username` , `password` and `port` defined.

>**Note :** values for `username` and `password` for database connections must be Base64 encoded. 

```yaml
mysql:
  mysql_test_connection:
    host: "127.0.0.1"
    database: "test"
    username: ""          
    password: ""
    port: "3306"
  mysql_dev_connection:
    host: "127.0.0.1"
    database: "dev"
    username: ""          
    password: ""
    port: "3306"

postgres:
  postgres_test:
    host: "127.0.0.1"
    database: ""
    username: ""
    password: ""
    port: "5432"
mssql:
  mssql_test:
    host: "127.0.0.1"
    database: ""
    username: ""
    password: ""
    port: "1433"
```
The above snippet of `config_default.yaml` shows 4 database connection registered one each for Postgres and MSSQL and 2
connections for MySQL. You can use the connections registered inside the `config_default.yaml` file in your configuration
scripts. Below is an example snippet of configuration file using above database connections as source and destinations

*Example:*
```python
STREAM = {
    "source": {
        "mysql": [
            {"connection": "mysql_test_connection", "table": "users"},
            {"connection": "mysql_dev_connection", "table": "account"},
        ],
        "postgres": [
            {"connection": "postgres_test", "table": "users"}
        ]            
    },
    "destination": {
        "mssql": [
            {"connection": "msql_test", "table": "sample"}
        ]            
    }   
}
``` 
Each connection entry for database must have `table` attribute value set. This attribute specifies the table name inside the 
database to be used as source or destination. If you are using database as `destination` entity, the table need not to be created, but database must be created prior using it. Tables are created by `CloudTDMS` dynamically.

> **Note:** credentials for a database inside `config_default.yaml` file must have requisite permissions to create tables and alter schemas.

### ServiceNow
`CloudTDMS` supports data retrieval and ingestion from a servicenow instance. You can use servicenow instance both as source 
as well as destination. Before using servicenow instance as a source or destination in configuration,
You need to register connections for the same inside `config_default.yaml` file. Connection can be registered under respective
key `servicenow:` present in `config_default.yaml` file.

A typical instance of `config_default.yaml` file containing connection entries for servicenow looks something like this.
Each servicenow connection must have `host`, `username` and `password` defined. The `host` represent servicenow instance
name, If your servicenow instance has url `https://dev1234.service-now.com` you need to provide the instance name as
a value to `host` not the full url.

>**Note :** values for `username` and `password` for servicenow connections must be Base64 encoded. 

```yaml
servicenow:
  production:
    host: "dev1234"
    username: ""
    password: ""
  development:
    host: "dev5678"
    username: ""
    password: ""
```

The above snippet of `config_default.yaml` shows 2 servicenow connection registered named as `production` and `development`. 
The `production` connection refers to instance `https://dev1234.service-now.com` and `development` connection refers to
`https://dev5678.service-now.com`

You can use the connections registered inside the `config_default.yaml` file in your configuration
scripts. Below is an example snippet of configuration file using above servicenow connections as source and destinations

*Example:*
```python
STREAM = {
    "source": {
        "servicenow": [
            {"connection": "production", "table": "incident"},
        ],         
    },
    "destination": {
        "servicenow": [
            {"connection": "development", "table": "incident"}
        ]            
    }   
}
```
Each connection entry for servicenow must have `table` attribute value set. This attribute specifies the table name in 
servicenow instance to be used as source or destination. In Above configuration script `incident` table of one instance 
is used as a source and of another instance is used as destination

> **Note:** credentials for a servicenow inside `config_default.yaml` file must have requisite permissions for reading and writing data.

### Network Storages

 
