## Search Methods
Searching **Personally Identifiable Information (PII)** in a data-set is acheived in two ways by `CloudTDMS`:
1. Searching on **`column_name`** basis
2. Searching on **`column_data`** basis

**Searching On `column_name` Basis :**

This search method involves searching the name of `column_header` of data-set with a list containing synonym words for the PII.
For Example : In order to identify `Gender` in a data-set as PII, following list of gender synonym words are used for searching
`['gender', 'sex', 'kind', 'sexuality', 'male', 'female', 'identity', 'neuter']`. If there is a match then the particular matched
column name of data-set will be identified as `Gender` PII and the matching score for the column will be set to `90%`.

**Searching On `column_data` Basis :**

This search method involves matching the column data of the data-set using either a regular-expression or sample data. 
PII's like `email_address`, `phone_numbers`, `IP address` etc are identified using regular-expressions, while PII's such as
`Name`, `Country`, `City`, `Municipality` etc are identified by matching the column data with the corresponding sample data of the entity.
`CloudTDMS` has sample data associated with it which is used for Synthetic Data Generation, Same data is being used to identify
the PII's on data basis.  

For Example : In order to identify `email_address` in a data-set as PII, following regular-expression `^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$`
is being used for searching. Each column entry is tested against the regular expression and list of boolean values is generated
in which a `True` value specifies a match otherwise `False`. A score value is generated based on the number of `True` values
and total records tested (maximum=10000) 

    score = (Number of True Values / Total Records Tested) * 100 

If the score value exceeds `5%` threshold the column will be identified as `email_address` PII.

Besides regular-expression sample data may also be used in searching certain PIIs like `Country`. While using sample data 
again each column entry will be tested to its existence in sample data and a score will be generated same as above.
 
## CloudTDMS PII Search Methods version 1.0 reference

### Person Name

1. **Name :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `Name` PII in data-set
```python
[
'first_name', 'last_name', 'fname', 'f_name', 'lname', 
'l_name', 'surname', 'middle_name', 'family_name', 'sname', 
's_name', 'forename', 'name', 'full_name', 'given_name',
'maiden_name', 'mname', 'g_name', 'm_name', 'initial_name', 'initial'
]
```
+ `on column_data basis` : Following Sample data is being used to identify the `Name` PII [Sample Data](../system/cloudtdms/providers/personal/person.csv) 


### Person Detail

1. **Age :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `Age` PII in data-set
```python
['age', 'maturity', 'seniority', 'years', 'duration', 'age_group', 'oldness']
```
+ `on column_data basis` : Any column data whose values are within the range [18,81] will be tagged as `Age` PII


2. **Gender :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `Gender` PII in data-set
```python
['gender', 'sex', 'kind', 'sexuality', 'male', 'female', 'identity', 'neuter']
```
+ `on column_data basis` : Following sample data is being used to identify the `Gender` PII.
```python
['male', 'female']
['m','f']
```

3. **Email :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `Email` PII in data-set
```python
['email', 'mail', 'e-mail', 'message', 'electronic_mail', 'post', 
'correspondence','send', 'mailing', 'memo', 'mailbox', 'write']
```
+ `on column_data basis` : Following regular-expression is being used to identify the `Email` PII.
```python
'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
```

4. **DOB :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `DOB` PII in data-set
```python
[
'dob','date_of_birth',
'birth_date','birth date',
'date of birth','D.O.B',
'DOB'
]
```
+ `on column_data basis` : Following regular-expression is being used to identify the `DOB` PII.
```python
'^\d{,2}[-/.]\d{,2}[-/.](17|18|19|20)\\d\\d$'
```

5. **Credit Card :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `Credit Card` PII in data-set
```python
[
'credt_card_num','credit_card_number',
'credit_card','credit card'
]
```
+ `on column_data basis` : Following regular-expression is being used to identify the `Credit Card` PII.
```python
'^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$'
```

6. **Social Security Number :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `Social Security Number` PII in data-set
```python
[
'ssn','social_security_number',
'social security number','National ID number',
'National_ID_number',' national id number',
'national_id_number'
]
```
+ `on column_data basis` : Following regular-expression is being used to identify the `Social Security Number` PII.
```python
'^(?!666|000|9\\d{2})\\d{3}(-)?(?!00)\\d{2}(-)?(?!0{4})\\d{4}$'
```

7. **Blood Group :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `Blood Group` PII in data-set
```python
[
'bg','blood group',
'blood_group','blood Group',
'Blood_Group'
]
```
+ `on column_data basis` : Following regular-expression is being used to identify the `Blood Group` PII.
```python
'^(A|B|AB|O)[+-]$'
```

### Networking

1. **IP address :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `IP address` PII in data-set
```python
[
'ipaddress', 'ip address', 'ip_address', 'ipadd', 
'ip add', 'ip_add','Internet Protocol address','Internet_Protocol_address',
'host identity', 'host_identity', 'IP number', 'IP_number','network identity',
'network_identity', 'network identification','network_identification'
]
```
+ `on column_data basis` :  Following regular-expression is being used to identify the `IP address` PII.
```python
'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
```

2. **MAC address :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `MAC address` PII in data-set
```python
[
'mac', 'mac address', 
'mac_address', 'mac_add'
]
```
+ `on column_data basis` :  Following regular-expression is being used to identify the `MAC address` PII.
```python
'[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$'
```

3. **MSISDN :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `MSISDN` PII in data-set
```python
[
'imeis','msidn','iccids',
'tmsis','msidsn','msidsns',
'esns','msin','misdn','MSISDN'
]
```

4. **IMSI :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `IMSI` PII in data-set
```python
['imsi','IMSI','International Mobile Subscriber Identity',
'International_Mobile_Subscriber_Identity',
'international mobile subscriber identity',
'international_mobile_subscriber_identity'
]
```

5. **GUID :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `GUID` PII in data-set
```python
[
'guid','GUID','Globally_Unique_Identifier',
'Globally Unique Identifier',
'GloballyUniqueIdentifier',
'globally_unique_identifier',
'globally unique identifier'
]
```
+ `on column_data basis` :  Following regular-expression is being used to identify the `GUID` PII.
```python
'^{?[0-9a-f]{8}-?[0-9a-f]{4}-?[1-5][0-9a-f]{3}-?[89ab][0-9a-f]{3}-?[0-9a-f]{12}}?$'
```

6. **Hardware Serial :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `Hardware Serial` PII in data-set
```python
[
'Serial Number','Serial_Number','serial_number'
,'serial number', 'hardware_serial_number',
'hardware serial number','Hardware_Serial_Number',
'Hardware Serial Number'
]
```
+ `on column_data basis` :  Following regular-expression is being used to identify the `Hardware Serial` PII.
```python
'^{?[0-9a-f]{8}-?[0-9a-f]{4}-?[1-5][0-9a-f]{3}-?[89ab][0-9a-f]{3}-?[0-9a-f]{12}}?$'
```
### Phone Number

1. **Phone Number :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `Phone Number` PII in data-set
```python
[
'phone_number', 'phone number',
 'contact', 'contact_number',
'contact number','number'
]
```
+ `on column_data basis` :  Following regular-expression is being used to identify the `Phone Number` PII.
```python
'^((\+)?([0-9]{,3}))?(-|\s)?(\()?[0-9]{3}(\))?(-|\s)?[0-9]{3}(-|\s)?[0-9]{4}$'
```

### Location

1. **Latitude :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `Latitude` PII in data-set
```python
[
'latitude',
'lat',
'altitude'
]
```
+ `on column_data basis` :  Following regular-expression is being used to identify the `Latitude` PII.
```python
'^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$'
```

2. **Longitude :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `Longitude` PII in data-set
```python
[
'longitude',
'long'
]
```
+ `on column_data basis` :  Following regular-expression is being used to identify the `Longitude` PII.
```python
'^\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$'
```

3. **Country :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `Country` PII in data-set
```python
[
'country','homeland',
'native land','native_land',
'grass roots','grass_roots',
'land'
]
```
+ `on column_data basis` : Following Sample data is being used to identify the `Country` PII [Sample Data](../system/cloudtdms/providers/location/airport.csv) 


4. **City :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `City` PII in data-set
```python
[
'city','capital','center',
'metropolis','downtown',
'place','port','polis','urbs'
]
```
+ `on column_data basis` : Following Sample data is being used to identify the `City` PII [Sample Data](../system/cloudtdms/providers/location/airport.csv) 

5. **Municipality :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `Municipality` PII in data-set
```python
[
'municipality','community',
'district','town','township'
,'village','borough','precinct'
]
```
+ `on column_data basis` : Following Sample data is being used to identify the `Municipality` PII [Sample Data](../system/cloudtdms/providers/location/airport.csv) 

6. **Postal Code  :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `Postal Code` PII in data-set
```python
[
'zip','pincode','pin_code',
'pin code','postalcode', 
'postal_code','postal code', 
'post'
]
```
+ `on column_data basis` : Following Sample data is being used to identify the `State` PII [Sample Data](../system/cloudtdms/providers/location/airport.csv) 

7. **State  :**
 
+ `on column_name basis` : Following list of synonym words are used for searching `State` PII in data-set
```python
[
'state'
]
```
+ `on column_data basis` : Following Sample data is being used to identify the `State` PII [Sample Data](../system/cloudtdms/providers/location/airport.csv) 
