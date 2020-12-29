# Data Sources & Destinations
This sections provides information about the supported data sources and destination in `CloudTDMS`.
`sources` represent the entities that are used to feed data into the process and destinations 
represent the entities that are used to store the resultant data. 

## Supported Sources And Destinations

### Static Files
`CloudTDMS` provides support for CSV, XML and JSON files to be used as a sources and destinations, This means you can use any
CSV or XML or JSON file to feed data to the configuration and Also save the resultant data as CSV or XML or JSON. In order to use a CSV or XML
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
xml:
  my_connection_name_one:
    source: "/home/user/xml-data-one/example-one.xml"
    target: "/home/user/some-other-folder"
  my_connection_name_two:
    source: "/home/user/xml-data-two/example-two.xml"


```
The `config_default.yaml` file contains entry for each source type, all connections related to CSV will be registered inside
`csv:` key. Above example has two connections named as `my_connection_name_one` and `my_connection_name_two` registered 
inside `csv:` key. Here `my_connection_one` and `my_connection_two` represent connection names, You can choose any name for representation
purpose. For `csv:`, `xml:` and `json:` under each connection name you have two keys `source` and `target`. `source` key takes an absolute
path of CSV or XML or JSON file present on your local machine to be used as a source file, While `target` key takes absolute directory path as a value
to represent the destination folder inside which resultant masked or synthetic data file must be stored.

Your connection name can act as both source as well as destination, depending upon the keys `source` and `target`. When
you use connection name in `source` attribute of configuration file then the file defined with`source` key in the particular connection name
is used as a source data, While as when you use connection name in `destination` attribute of configuration file then the
directory defined with the `target` key in the connection name is used as a destination for result data.

>**Note :** In case `target` is not defined `data` directory of `cloudtdms` folder will be used as a destination folder for 
> generated data. 

*Example* :
Below is an example snippet of configuration file using above CSV, XML and JSON connections as source and destinations
```python
STREAM = {
    "source": {
        "csv": [
            {"connection": "my_connection_name_one", "delimiter": ","},
            {"connection": "my_connection_name_two", "delimiter": ","},
        ],
        "xml": [
                {"connection": "my_connection_name"},
            ],
        "json": [
            {"connection": "my_connection_name", "type": "lines"}
        ]            
    },
    "destination": {
        "json": [
            {"connection": "my_connection_name", "type": "array"}
        ], 
         "xml": [
                    {"connection": "my_connection_name","root_tag":"employees", "record_tag":"employee"},
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

In case of destination connection in `xml`, there are `root_tag` and `record_tag` as an additional attributes.
`root_tag` specifies the tag name for the root in the xml file and `record_tag` specifies the tag name for each record in xml file.
If the destination for xml looks like : 

```markdown
 "xml": [
          {"connection": "my_connection_name","root_tag":"employees", "record_tag":"employee"},
        ]
```
The XMl file looks like:
```markdown
<employees>
    <employee>
        ...
    </employee>
   
    <employee>
        ...
    </employee>

</employees>
```

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

>**Note :** Values for `username` and `password` for database connections must be Base64 encoded.

>**Note :** To encode `username` and `password` to `Base64` you can use already existing `base64` utility in linux environment. Use following commands to get your encrypted string.

    echo YOUR_USERNAME | base64
    
or
    
    echo YOUR_PASSWORD | base64

```yaml
mysql:
  mysql_test_connection:
    host: "127.0.0.1"
    database: "test"
    username: ""         # MySQL username Base64 Encrypted   
    password: ""         # MySQL password Base64 Encrypted
    port: "3306"
  mysql_dev_connection:
    host: "127.0.0.1"
    database: "dev"
    username: ""         # MySQL username Base64 Encrypted
    password: ""         # MySQL password Base64 Encrypted
    port: "3306"

postgres:
  postgres_test:
    host: "127.0.0.1"
    database: ""
    username: ""        # Postgres username Base64 Encrypted
    password: ""        # Postgres password Base64 Encrypted
    port: "5432"
mssql:
  mssql_test:
    host: "127.0.0.1"
    database: ""
    username: ""        # MSSQL username Base64 Encrypted
    password: ""        # MSSQL password Base64 Encrypted
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
            {"connection": "mysql_test_connection", "table": "users", "order": "desc"},
            {"connection": "mysql_dev_connection", "table": "account", "order": "rand", "where": "city='New York'"},
        ],
        "postgres": [
            {"connection": "postgres_test", "table": "users","order": "rand", "where": "city='New York'"}
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

Besides `table` you can specify the values to `order` and `where` attributes that are used to **`ORDER BY`** and apply **`WHERE`** condition on the resulting
SQL query. The `order` attribute can take one of the following values.

- `asc` : This is used to fetch initial records from the table.
- `desc` : This is used to fetch lastest records from the table.
- `rand` : (`default`) Fetch random records from table.


> **Note:** Credentials for a database inside `config_default.yaml` file must have requisite permissions to create tables and alter schemas.

### ServiceNow
`CloudTDMS` supports data retrieval and ingestion from a servicenow instance. You can use servicenow instance both as source 
as well as destination. Before using servicenow instance as a source or destination, in configuration
you need to register connections for the same inside `config_default.yaml` file. Connection can be registered under respective
key `servicenow:` present in `config_default.yaml` file.

A typical instance of `config_default.yaml` file containing connection entries for servicenow looks something like this.
Each servicenow connection must have `host`, `username` and `password` defined. The `host` represent servicenow instance
name, If your servicenow instance has url `https://dev1234.service-now.com` you need to provide the instance name as
a value to `host` not the full url.

>**Note :** Values for `username` and `password` for servicenow connections must be Base64 encoded. 

```yaml
servicenow:
  production:
    host: "dev1234"
    username: ""        # ServiceNow username Base64 Encrypted
    password: ""        # ServiceNow password Base64 Encrypted
  development:
    host: "dev5678"
    username: ""        # ServiceNow username Base64 Encrypted
    password: ""        # ServiceNow password Base64 Encrypted
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
servicenow instance to be used as source or destination. In above configuration script `incident` table of one instance 
is used as a source and of another instance is used as destination

> **Note:** credentials for a servicenow inside `config_default.yaml` file must have requisite permissions for reading and writing data.

### SalesForce
`CloudTDMS` supports data retrieval and ingestion from a salesforce instance. You can use salesforce instance both as source 
as well as destination. Before using salesforce instance as a source or destination, in configuration
you need to register connections for the same inside `config_default.yaml` file. Connection can be registered under respective
key `salesforce:` present in `config_default.yaml` file.

A typical instance of `config_default.yaml` file containing connection entries for salesforce looks something like this.
Each salesforce connection must have `host`, `username`, `password` and `security_token` defined. The `host` represent salesforce instance
name, If your salesforce instance has url `https://mn12.salesforce.com` you need to provide the instance name `mn12` as
a value to `host` not the full url.

>**Note :** Values for `username`, `password` and `security_token` for salesforce connections must be Base64 encoded. 

```yaml
salesforce:
  production:
    host: "mn12"
    username: ""        # Salesforce username Base64 Encrypted
    password: ""        # Salesforce password Base64 Encrypted
    security_token: ""  # Salesforce security_token Base64 Encrypted
  development:
    host: "um12"
    username: ""        # Salesforce username Base64 Encrypted
    password: ""        # Salesforce password Base64 Encrypted
    security_token: ""  # Salesforce security_token Base64 Encrypted
```

The above snippet of `config_default.yaml` shows 2 salesforce connection registered named as `production` and `development`. 
The `production` connection refers to instance `https://mn12.salesforce.com` and `development` connection refers to
`https://um12.salesforce.com`

You can use the connections registered inside the `config_default.yaml` file in your configuration
scripts. Below is an example snippet of configuration file using above salesforce connections as source and destinations

*Example:*
```python
STREAM = {
    "source": {
        "salesforce": [
            {"connection": "production", "table": "Account"},
        ],         
    },
    "destination": {
        "salesforce": [
            {"connection": "development", "table": "Account"}
        ]            
    }   
}
```
Each connection entry for salesforce must have `table` attribute value set. This attribute specifies the Object name in 
Salesforce instance to be used as source or destination. In above configuration script `Account` Object of one instance 
is used as a source and of another instance is used as destination

> **Note:** Credentials for a salesforce inside `config_default.yaml` file must have requisite permissions for reading and writing data via REST Bulk API.

### Network Storages

### SFTP
`CloudTDMS` supports data retrieval and upload data to/from `sftp`. You can use `sftp` both as source 
as well as destination. Before using `sftp` as a source or destination, in configuration
you need to register connections for the same inside `config_default.yaml` file. Connection can be registered under respective
key `sftp:` present in `config_default.yaml` file.

A typical instance of `config_default.yaml` file containing connection entries for `sftp` looks something like this.
Each `sftp` connection must have `host`, `username`, `password`, `port`, `ssh_public_key` and `passphrase`  defined.

>**Note :** Values for `username`, `password`, `ssh_public_key` and `passphrase` for sftp connections must be Base64 encoded. 


```yaml
sftp:
  production:       
    host: "10.0.1.5"          
    username: ""        # SFTP username Base64 Encrypted     
    password: ""        # SFTP password Base64 Encrypted
    port: "22"         
    ssh_public_key: ""  # path to ssh public key
    passphrase: ""      # SFTP passphrase Base64 Encrypted

   development:       
    host: "10.0.1.4"          
    username: ""        # SFTP username Base64 Encrypted     
    password: ""        # SFTP password Base64 Encrypted      
    port: "22"         
    ssh_public_key: ""  # path to ssh public key
    passphrase: ""      # SFTP passphrase Base64 Encrypted

```
The above snippet of `config_default.yaml` shows 2 `sftp` connections registered named as `production` and `development`.
The `production` connection refers to server with ip `10.0.1.5` and the `development` connection refers to server with
 ip `10.0.1.4`.

You can use the connections registered inside the `config_default.yaml` file in your configuration
scripts. Below is an example snippet of configuration file using above sftp connections as source and destinations

*Example:*
```python
STREAM = {
    "source": {
        "sftp": [
            {"connection": "development", "file": "REMOTE_PATH_OF_FILE"},
        ],         
    },
    "destination": {
        "sftp": [
            {"connection": "development", "file": "PATH_TO_SAVE","overwrite":True}
        ]            
    }   
}
```
Each connection entry for sftp must have `file` attribute value set. This attribute specifies the file path in 
sftp to be used as source or destination. The sftp destination can also have an optional attribute `overwirte`.
If the `overwrite` attribute is set to `True` it will overwrite the existing file on the sftp server otherwise not.
By default it is set to `False`.

> **Note:** Credentials for a sftp inside `config_default.yaml` file must have requisite permissions for reading and writing data.


### REDSHIFT
`CloudTDMS` supports data retrieval and upload data to/from `Redshift`. You can use `Redshift` both as source 
as well as destination. Before using `Redshift` as a source or destination, in configuration
you need to register connections for the same inside `config_default.yaml` file. Connection can be registered under respective
key `redshift:` present in `config_default.yaml` file.

A typical instance of `config_default.yaml` file containing connection entries for `Redshift` looks something like this.
Each `Redshift` connection must have `host`,`database`, `username`, `password`, and  `port` defined.

>**Note :** `host` must be the `Endpoint` of the Redshift. 


>**Note :** Values for `username`, `password` for  redshift must be Base64 encoded. 


```yaml
redshift:
  production:                         # Connection Name
    host: "redshift-cluster-1.aaaaaaa7dddd.us-west-9.redshift.amazonaws.com"                    # Redshift endpoint  (Don't  use full url)
    database: ""
    username: ""                # Redshift username Base64 Encrypted
    password: ""                # Redshift password Base64 Encrypted
    port: "5432"


  development:                         # Connection Name
    host: "redshift-cluster-2.aaaaaaa7dddd.us-west-9.redshift.amazonaws.com"                    # Redshift endpoint  (Don't  use full url)
    database: ""
    username: ""                # Redshift username Base64 Encrypted
    password: ""                # Redshift password Base64 Encrypted
    port: "5432"

```
The above snippet of `config_default.yaml` shows 2 `Redshift` connections registered named as `production` and `development`.
The `production` connection refers to cluster `redshift-cluster-1` on redshift server and the `development` connection refers to `redshift-cluster-2` on the redshift server.

You can use the connections registered inside the `config_default.yaml` file in your configuration
scripts. Below is an example snippet of configuration file using above redshift connections as source and destinations

*Example:*
```python
STREAM = {
    "source": {
        "redshift": [
            {"connection": "development", "table": "redshift_table_test", "order":"desc"}
        ],         
    },
    "destination": {
         "redshift": [
             {"connection": "production", "table":"redshift_table_test", "order":"rand"},
         ]           
    }   
}
```
Each connection entry for redshift must have `table` attribute value set. This attribute specifies the table name inside the 
database to be used as source or destination. If you are using redshift as `destination` entity, the table need not to be created, but database must be created prior using it. Tables are created by `CloudTDMS` dynamically.

Besides `table` you can specify the values to `order` and `where` attributes that are used to **`ORDER BY`** and apply **`WHERE`** condition on the resulting
SQL query. The `order` attribute can take one of the following values.

- `asc` : This is used to fetch initial records from the table.
- `desc` : This is used to fetch lastest records from the table.
- `rand` : (`default`) Fetch random records from table.
