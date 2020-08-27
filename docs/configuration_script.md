# Configuration script version 0.1 reference

### Reference and guidelines

These topics describe `version 0.1` of the configuration script file format. This is the newest version.

### Configuration Reference
The `CloudTDMS` script file is a `python` file that defines what type of data is to be generated.

The default path for a `script` file is `./scripts/<file_name>.py`. 
Each `script` file must have a variable named `STREAM` defined in it, This variable must be of type `dictionary`. It's this
variable that represents a configuration for synthetic data generation and masking. This variable contains `configuration`
attributes as key value pair. 

**`./scripts/example.py`**

```python
STREAM = {

}
```

A `script` file represents a stream of data. When a script is defined it must have some mandatory attributes defined in it
like, `frequency`. frequency defines how often data is to be generated. If a stream has frequency `hourly` it means that data would be 
generated each hour, With this approach user can generate data in streams. Like `frequency`  there are other mandatory attributes
that must be defined in order to get data generated. In the subsequent sections we shall define all the configuration attributes
supported by current version

#### Configuration Attributes  

This section contains a list of all configuration options supported by `CloudTDMS` in current version.

**Mandatory Attributes :**

Following configuration attributes are mandatory for a `script` file, Absence of any one of the attributes will not lead to 
data generation.

+ **`number`** : This attribute defines how many number of records need to be generated. The generated output file will have 
                 this many records stored in it.
 ```python
STREAM = {
    "number" : 1000
 }
 ```
                 
+ **`title`** : This attribute is used to provide a name to the output file. If you want your output file to be named say,
                `example.csv` then you will set value to this attribute as `example`

```python
STREAM = {
    "title" : "example"
 }
 ```   
+ **`format`** : This attribute is used to specify the format for the output file.

> **Note** : currently only `csv` format is supported

```python
STREAM = {
    "format" : "csv"
 }
 ```   
+ **`frequency`** : This attribute is used to specify how often should data be generated, `CloudTDMS` uses scheduler to 
                    to run scripts inside the `scripts` folder. `frequency` defines how often should scheduler run your
                    script to generate random data for you. It can take cron values like
                    
    - `once` : This will run script only once
    - `hourly` : This will run script each hour
    - `daily` : This will run script daily at `00:00:00` hours.
    - `monthly` : This will run script on 1st of every month at `00:00:00` hours
```python
STREAM = {
    "frequency" : "once"
 }
 ``` 

**Optional Mandatory (Data Masking only)**                    
+ **`source`** : If you are using `CloudTDMS` for data masking purpose, then this attribute is mandatory else for synthetic 
                 data generation this is not necessary. For data masking you must specify the name of the data file as value to this
                 attribute, from which data needs to be read and masked. The file must be in `user-data` folder of `cloudtdms`.
                 All data-masking attributes require this attribute to be set.
                 As an example suppose, I want to mask data from file named `transaction_daily.csv` which is inside the
                 `user-data` folder of `cloudtdms`, Then my `source` attribute will have value as follows

>**Note** : Files inside `user-data` should be `.csv` files only, As of now only `csv` files are supported
                 
```python
STREAM = {
    "source" : "transaction_daily"
 }
 ```             

**Data Masking Attributes :**
Following are configuration attributes that user can use to mask his data using `cloudtdms`. For
more details about data masking feature provided by `CloudTDMS` please refer to data masking section [Data Masking](data_masking.md).

>**Note** : Each of the data masking attribute requires `source` attribute to be present.

+ **`substitute`** : This attribute is used to anonymize personally identifiable information in the user data. In order to
                     perform anonymization, user can choose a compatible `generator` function from various functions available
                     under `providers` of `CloudTDMS`. User can use `substitute` attribute to specify which column values in
                     the production data file must be substituted with the values from the generator function. for example:
                     Suppose my production data has `Surname`, `Age` columns which I would require to anonymize. The compatible
                     generator functions `last_name` and `random_number` are available are under `personal` and `basics` provider
                     respectively. With respect to this example `substitute` attribute will take following values.
                     
```python
STREAM = {
    "source" : "production_data",
    "substitute" : {
        "Surname" : {"type" : "personal.last_name"},
        "Age" : {"type" :  "basics.random_number", "start" :  23, "end" :  45}
    }
 }
 ```          
+ **`encrypt`** : This attribute is used to encrypt values of the columns. `CloudTDMS` provides various encryption techniques
                  that can be used to encrypt any number of columns in data. Please refer to  [Data Masking](data_masking.md) section
                  for more details about encryption techniques available.
                  
```python
STREAM = {
    "source" : "production_data",
    "encrypt": {
            "columns": ["EstimatedSalary", "Balance"],
            "type" : "ceaser",
            "encryption_key": "Jd28hja8HG9wkjw89yd"
    }
 }
 ```    

+ **`nullying`** : This attribute is used to make column values `null` i.e It would make column/column's empty. It takes
                   any array of column names as value, Each column in the list will be made `null` / empty in output file.
                   
```python
STREAM = {
    "source" : "production_data",
    "nullying" : ["RowNumber", "Tenure"]
 }
 ```                                             

+ **`delete`** : This attribute takes a list of columns as value, And any column in this list will not be present in the
                 output file. The column/columns will not take part in data masking operation. 
                 
```python
STREAM = {
    "source" : "production_data",
    "delete" : ["CustomerID", "CreditScore"]
 }
 ```                                      

+ **`shuffle`** : This attribute takes a list of columns as value, each column inside this list will be shuffled randomly
                  before writing it to the output file.
                  
```python
STREAM = {
    "source" : "production_data",
    "shuffle" : ["NoOfProducts", "PurchasedItems"]
 }
 ```                   
**Realistic Synthetic Data attribute :**                     
Following are the configuration attributes required for generating realistic synthetic data.

+ **`schema`** : In order to use `CloudTDMS` for realistic synthetic data generation, You need to use `schema` attribute
                 inside your `STREAM` variable to define the schema of the output data file. As the name suggests in this
                 attribute you define the schema of the output data to be generated. The schema of the data to be generated is 
                 defined using the `generator` functions available under different `providers` of `CloudTDMS`. 
                 `CloudTDMS` provides various `generator` functions inside different `providers` for example, In `personal`
                 provider `first_name`, `last_name`, `gender`, `full_name`, `username` etc. are various generator functions
                 which generate corresponding synthetic data. Please refer to [Providers](providers.md) sections to get a
                 list of all `providers` and corresponding `generator` functions available in `CloudTDMS`.

**example script**
   
```python
STREAM = {
        "number": 1000,
        "title": 'synthetic_data',
        "format": "csv",
        "frequency": "once",
        "schema": [
            {"field_name" :  "id", "type" :  "basics.auto_increment", "prefix" :  "INC", "suffix" :  "NZD", "start":  2000, "increment" :  1},
            {"field_name": "fname", "type": "personal.first_name"},
            {"field_name": "lname", "type": "personal.last_name",},
            {"field_name": "sex", "type": "personal.gender"},
            {"field_name": "email", "type": "personal.email_address"},
            {"field_name": "country", "type": "location.country"},
            {"field_name": "city", "type": "location.city"},
        ]
       }
```
`schema` attribute takes a list of `generator` functions as value. Each `generator` function is defined using a dictionary
object and represents a column in the output data file. The dictionary object contains different attributes depending upon 
the `generator` function. In the example above, we see 7 dictionary objects inside the `schema` list. It means we are supposed
to generate data for 7 columns. First column will be name `id` as the `field_name` of the object is set value `id`. The `id`
is to be generated using `auto_increment` generator fucntion available inside `basics` provider.

Which `generator` function to use is defined using `type` attribute of the dictionary object. The other attributes like `prefix`,
`suffix`, `start` etc. are specific to a particular `generator` function. All attributes specified in the dictionary object
are passed as arguments to the functions. Different `generator` functions have different attributes available to tweak their
data generation settings.

In the example above we are generating `id` which is an integer value starting from 2000 and for each record it will be 
incremented by 1. Similarly we have `fname` which is generated using `first_name` function and like wise other are defined.

The output of the above script would be something like this:

|id    | fname | lname | sex | email | country | city |
|------|-------|-------|-----|-------|---------|------|                
| 2000 | David |Savage |Male |d.savage87@gmail.com | United States of America | New York
| 2001 | Paul  |Winter |Male |p_winter234@outlook.com | United Kingdom | London |
| 2002 | Christopher|Metcalfe|Male |c.metcalfe901@mail.com | United Kingdom | Manchester |

---                 