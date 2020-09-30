# Data Profiling

Data profiling is the process of examining the data available from an existing information source (e.g. a database or a file) 
and collecting statistics or informative summaries about that data. The purpose of these statistics may be to: 

1. Find out whether existing data can be easily used for other purposes
2. Assess data quality, including whether the data conforms to particular standards or patterns
4. Assess the risk involved in integrating data in new applications, including the challenges of sensitive data
5. Create metadata that can be used to discover problems such as illegal values, misspellings, missing values, varying value representation, and duplicates.

## Data Profiling In CloudTDMS

`CloudTDMS` provides data profiling reports for:

1. Exploratory Data Analysis
2. Sensitive Data Identification
 
#### Exploratory Data Analysis 
Exploratory data analysis is an approach to analyzing data sets to summarize their main characteristics, often with 
visual methods. A statistical model can be used or not, but primarily EDA is for seeing what the data can tell us beyond 
the formal modeling or hypothesis testing task.

`CloudTDMS` uses [`pandas_profiling`](http://github.com/pandas-profiling/pandas-profiling) library for generating exploratory data analyses reports.

For each column the following statistics - if relevant for the column type - are presented in an interactive HTML report:

* **Type inference**: detect the types of columns in a dataframe.
* **Essentials**: type, unique values, missing values
* **Quantile statistics** like minimum value, Q1, median, Q3, maximum, range, interquartile range
* **Descriptive statistics** like mean, mode, standard deviation, sum, median absolute deviation, coefficient of variation, kurtosis, skewness
* **Most frequent values**
* **Histogram**
* **Correlations** highlighting of highly correlated variables, Spearman, Pearson and Kendall matrices
* **Missing values** matrix, count, heatmap and dendrogram of missing values
* **Text analysis** learn about categories (Uppercase, Space), scripts (Latin, Cyrillic) and blocks (ASCII) of text data.
* **File and Image analysis** extract file sizes, creation dates and dimensions and scan for truncated images or those containing EXIF information.
 
#### Sensitive Data Identification

`CloudTDMS` in addition to exploratory data analysis report generates sensitive data report that helps you to identify 
the potential Personally Identifiable Information (PII) in your data-set.
 
Personally identifiable information (PII) is information that, when used alone or with other relevant data, can identify
an individual. PII may contain direct identifiers (e.g., Name, gender) that can identify a person uniquely, or 
quasi-identifiers (e.g., race) that can be combined with other quasi-identifiers (e.g., date of birth) to successfully 
recognize an individual.

Current version of `CloudTDMS` is capable of identifying following PII's in the user data. PII's are categorised into
categories. To learn more about the process used to identify PII's in data please refer [Search Methods](personal_identifiable_information.md#cloudtdms-pii-search-methods-version-10-reference) section 

**Location :**

+ Latitude and Longitude
+ Country
+ City
+ Municipality
+ State  

**Networking :**

+ IP Address
+ MAC Address
+ GUID
+ Hardware Serial
+ MSISDN
+ IMSI

**Phone :**    

+ Contact Numbers
 
**Person Details :**

+ Age
+ Gender
+ Email Address
+ Date Of Birth
+ Credit Card Number
+ Social Security Number
   
**Person Name :**

+ First Name, Last Name, Full Name

### How To Use ?

In order to generate profiling reports for your data, you simply need to place your `CSV` data file inside the `profiling-data`
directory of the project. `CloudTDMS` will stage the data for profiling and generate reports inside the `profiling_reports`
directory. You can also choose to receive the reports in email, for that you need to provide the `SMTP` details inside 
[`config_default.yaml`](../config_default.yaml) file. 

In the `to` option of the `email` section of `config_default.yaml` file provide the email
address to which the profiling reports need to be sent. Other options such as `smtp_host`, `smtp_port`, `smtp_ssl`,
`username` and `password` are specific to SMTP server. Please refer [Email Notification](email_notify.md) section for more details.
