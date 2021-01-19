# Contributions

## Extending CloudTDMS with Source & Destination.
CloudTDMS supports data retrieval and ingestion from multiple sources and destinations. Some supported source's and destinations are:

- Amazon S3
- MySQL
- Postgres etc.

Providing support for additional source's and destinations involves following steps.

1. **Determine how to represent the connection in configuration file :**
   As, an example In order to add support for MySQL database we have to support following attribute (`mysql`) and value in configuration file
   
       "sources": {
           "mysql": [
               {"connection": "mysql_test", "table": "ExampleTable"}
           ]
       }
   
   The above snippet shows that when a connection entry for MySQL is made user needs to pass a `connection` name and also some addtional attributes like
   `table` name. Once you have determined representation go to step 2.
   
2. **Create a module file inside `extras` package of `cloudtdms` for the Source & Destination entity :**
   Create a module file say, `mysql.py` inside `system/cloudtdms/extras` directory. This module is going to hold code for ingestion and retreival of data for the
   respective platform. Each module must contain two functions `download` and `upload`. The naming convention for upload and download function must be following
   
       def [PREFIX]_upload(**kwargs):
           # TODO upload logic
           
       def [PREFIX]_download(**kwargs):
           # TODO download logic
           
   The `PREFIX` is the attribute name used in configuration to represent the source and destination platform. In case of MySQL we use `mysql` as attribute name
   to represent a connection in configuration file, So `PREFIX` for MySQL will be `mysql`. Provide the implementation logic for the repective functions.
   
       def mysql_upload(**kwargs):
           # TODO upload logic
           
       def mysql_download(**kwargs):
           # TODO download logic
           
3. **Add new source entry in `synthetic_data_dag_source_tasks.py.j2` template file:**
   
   Add the `PREFIX` of the newly add source in `supported_sources` list of `synthetic_data_dag_source_tasks.py.j2` template file
   
       {% set supported_sources = ['csv', 'mysql', 'servicenow', 'salesforce', 'json', 'mssql','postgres', 'sftp'] %}

   Also provide an `elif` statement for the new source inside the `if-else` ladder of the template file. For MySQL it would be something like this
   
       {% elif key == 'mysql' %}

       # Initialize task for MySQL db Extract {{ item.connection }} and table {{ item.table }}
       {{ key }}_{{ item.connection }}_kwargs['connection'] = "{{ item.connection}}"
       {{ key }}_{{ item.connection }}_kwargs['table_name'] = "{{ item.table }}"
       {{ key }}_{{ item.connection }}_kwargs['order'] = "{{ item.order }}"
       {{ key }}_{{ item.connection }}_kwargs['where'] = "{{ item.where }}"
       {{ key }}_{{ item.connection }} = PythonOperator(task_id="Extract_MySQL_{{ item.connection }}_{{ item.table }}", python_callable=mysql_download, op_kwargs={{ key }}_{{ item.connection }}_kwargs, dag=dag)

  Any attribute that user passes alongwith the connection entry in configuration file must be accepted here by following statement:
  
       {{ key }}_{{ item.connection }}_kwargs['table_name'] = "{{ item.table}}"
       
  In Step 1 we provide `table` value inside the MySQL connection entry that option will be accepted here by accessing it via `item.table` and then same is passed
  to the corresponding `download` function as `table_name`
  
  
4. **Add new destination entry in `synthetic_data_dag_destination_tasks.py.j2` template file:**  
   
   Similar to Step 3, Add the `PREFIX` of the newly add destination in `supported_destination` list of `synthetic_data_dag_destination_tasks.py.j2` template file
   
        {% set supported_destinations = ['csv', 'json', 'mysql', 'servicenow', 'salesforce', 'json', 'postgres', 'mssql', 'sftp'] %}

   Also provide the `elif` statement for the new destination inside the `if-else` ladder of the template file. For MySQL it would be something like this
   
       {% elif key == 'mysql' %}

       # Initialize task for MySQL db Upload for {{ item.connection }} and table {{ item.table }}
       {{ key }}_{{ item.connection }}_kwargs['connection'] = "{{ item.connection}}"
       {{ key }}_{{ item.connection }}_kwargs['table_name'] = "{{ item.table }}"
       {{ key }}_{{ item.connection }} = PythonOperator(task_id="Load_MySQL_{{ item.connection }}", python_callable=mysql_upload, op_kwargs={{ key }}_{{ item.connection }}_kwargs, dag=dag)

  
   Any attribute that user passes alongwith the connection entry in configuration file must be accepted here by following statement:

       {{ key }}_{{ item.connection }}_kwargs['table_name'] = "{{ item.table}}"

   In Step 1 we provide `table` value inside the MySQL connection entry that option will be accepted here by accessing it via `item.table` and then same is passed
   to the corresponding `upload` function as `table_name`
   
5. **Add a connection key entry inside `config_default.yaml` file:**
   
   Provide a connection key entry for the new source and destination inside the `config_default.yaml` file. For Example. In case of MySQL it is
   
         # MySQL
          mysql:
            mysql_test:         # Connection Name
              host: ""          # MySQL host name
              database: ""      # MySQL database name
              username: ""      # MySQL username Base64 Encrypted
              password: ""      # MySQL password Base64 Encrypted
              port: "3306"      # MySQL port default is 3306



       
