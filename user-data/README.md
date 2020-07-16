### user-data
Have existing data you want reference in your scripts?

Place your CSV datasets in this folder (user-data), 
then import columns into your scripts using the Dataset Column name.

**example**
Suppose your CSV data file is named as **my_custom.csv**, and look something like this

|serial    |amount   |teams       |mixed                 |
|----------|---------|------------|----------------------|
|5000      |2000     |HR          |2000-HR#5000          |
|5001      |2222     |Account     |2222-Account#5001     |
|5002      |2431     |Development |2431-Development#5002 | 
 
then your schema entry will look like as this

```python
{"field_name" :  "column1", "type" :  "my_custom.serial"}
{"field_name" :  "column2", "type" :  "my_custom.teams"}
```