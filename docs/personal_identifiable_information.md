## Search Methods
Searching **Personally Identifiable Information (PII)** in a data-set is acheived in two ways by `CloudTDMS`:
1. Searching on `column_name` basis
2. Searching on `column_data` basis

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




