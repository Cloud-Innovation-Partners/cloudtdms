## Providers
`cloudtdms` uses concept of `provider` to generate a data. The term `provider` with reference to `cloudtdms` refers to a 
pythonic function that is capable of generating data. A provider can be as simple as 

```python
def example_provider(number_of_records, args):
    return range(int(number_of_records))
```

or it can be a complex statistical function calculating various stats from the data.

`cloudtdms` has many in-built providers that can be used for generating synthetic data for specific purpose. Here we shall
list providers that are available in cloudtdms and there syntax and control attributes that can be used to change the data 
generation process. 

### Basics
1. **boolean :** Generates a `boolean` value `true/false`, you can provide custom values instead of `default` value using
    `set_val` attribute.
    
    + *set_val* : takes a pair of words delimited by `/` as a value, word left of the `/` will be used as a value for true and word right
    of the `/` will be used as a false value 
    
    *syntax*:
    ```json
    {"field_name" : "status", "type" : "basics.boolean", "set_val": "1/0"}
    ```
    This will generate value `1` for true and `0` for false.

2. **frequency :** Generates a frequency values from the set `[Never, Seldom, Once, Often, Daily, Weekly, Monthly, Yearly]`
    
    *syntax*:
    ```json
    {"field_name" :  "freq", "type" :  "basics.frequency"}
    ```
3. **color :** Generates a random color value based on the format specified. By `default` the format is `hex-color`, and it
    will generate hex color codes such as : `#1423ab`. Other formats available are `name` and `short-hex`.
        
    + *`name`* : will generate color names such as, `Red, Blue, Green ...` etc.
    + *`short-hex`* : will generate hex color codes in short form such as `#14b, #876 ...` etc.
        
    *syntax*:
    ```json
    {"field_name" : "colour", "type" : "basics.color", "format" :  "hex-code"}
    ```
4. **words :** This generates a list of random english words. such as 
    `food character prepare outside leg`
    `house food cat rice owl`
     The number of words that need to be generated can be specified by setting the values to the attributes `atleast` and
     `atmost`.
     + *`atleast`* : used to specify at least how many words must be generated, `deafult` value is `1`
     + *`atmost`* : used to specify at most how many words can be in generated list, `default` value is `3`
    
    *syntax*:
    ```json
    {"field_name" :  "captcha", "type" :  "basics.word", "atleast" :  "5", "atmost" :  "15"}
    ```
    
5. **sentence :** This generates a collection of sentences, such as
    `Have heart cover analysis carry. Or candidate trouble listen ok. Way house answer start behind old.`
    
    The number of sentences that need to be generated can be specified by setting the values to the attributes `atleast` and
    `atmost`.
    
    + *`atleast`* : used to specify at least how many sentences must be generated, `default` value is `1` 
    + *`atmost`* : used to specify at most how many sentences can be in generated in a collection, `default` value is `10`
    
     *syntax*:
    ```json
    {"field_name" :  "text", "type" :  "basics.sentence", "atleast" :  "5", "atmost" :  "10"}
    ```
    
6. **blank :** This is used to generate `null` value always.

    *syntax*:
    ```json
    {"field_name" :  "empty", "type" :  "basics.blank"}
    ```
7. **guid :** Generates global unique identity number, a 36 charcter hex such as `ddee19bc-84fd-4627-897c-dec7c8010977`

    *syntax*:
    ```json
    {"field_name" :  "uuid", "type" :  "basics.guid"}
    ```    
8. **password :** Generates a random string of characters, the length of the string can be tweaked using the `length` attribute.
    The `default` length of the string is `8` characters
    
    *syntax*:
    ```json
    {"field_name" :  "passcode", "type" :  "basics.password", "length" :  12}
    ``` 
9. **auto_increment :** This generates a sequence of numbers with a common difference equal to the value of `increment` attribute.
    The `default` value of `increment` is `1`. Other attributes provided are:
    
    + *`prefix`* : used to append a `prefix` value before the number such as `INC2000`
    + *`suffix`* : used to append a `suffix` value after the number such as `2000PR`
    + *`start`* : used to specify the starting integer value for the sequence, the `default` start value is `1`
    
    *syntax*:
    ```json
    {"field_name" :  "id", "type" :  "basics.auto_increment", "prefix" :  "INC", "suffix" :  "NZD", "start":  2000, "increment" :  5}
    ```
10. **random_number :** This generates a sequence of random numbers between the `start` and `end` value.
    
    + *`start`* : used to specify the starting value for the sequence, no number generated will be less then this value
    + *`end`* : used to specify the end value for the sequence, no number generated will be greater then this value
    
    *syntax*:
    ```json
    {"field_name" :  "random_id", "type" :  "basics.random_number", "start" :  20, "end" :  200}
    ```
    
### Personal

1. **company_name :** Generates a random company name.
    
    *syntax*:
    ```json
    {"field_name" :  "cname", "type" :  "personal.company_name"}
    ```
    
2. **department :** Generates a department type such as `Human Resource, Accounting, Engineering, Grocery, Books ...` etc
    department names can be either of `retail` category or `coporate` category. You can specify the category type by add a value
    to `category` attribute.
    
    + *`category`* : used to specify the category type, can take two values `retail` and `corporate`, by `default` the category
    has `all` value which will generate a randomly any name out of the two categories.
    
    *syntax*:
    ```json
    {"field_name" :  "dept", "type" :  "personal.department", "category" :  "corporate"}
    ```  
 3. **duns_number :** Generates random 9 digit Data Universal Numbering System (DUNS) number such as `31-300-8468, 34-230-3150...` etc.
 
    *syntax*:
    ```json
    {"field_name":  "duns_id", "type" :  "personal.duns_number"}
    ```

4. **first_name :** Generates random First Names.
    
    + *category* : takes two values `male` and `female`, when category is set names specific to particular gender are generated.
    
    *syntax*:
    ```json
    {"field_name":  "fname", "type" :  "personal.first_name", "category" :  "male"}
    ```
   
5. **last_name :** Generates random Last Names.
    
    *syntax*:
    ```json
    {"field_name":  "lname", "type" :  "personal.last_name"}
    ```
   
6. **full_name :** Generates a Full Name having format `{first_name} {last_name}` such as `John Sarcozy` etc.
    
    + *category* : takes two values `male` and `female`, when category is set full names specific to particular gender are generated.
    
     *syntax*:
    ```json
    {"field_name":  "name", "type" :  "personal.full_name", "category" :  "female"}
    ```
7. **gender :** Generates a random value from a set `['Male', 'Female']`, you can provide custom values instead of `default` value using
    `set_val` attribute.
    
    + *set_val* : takes a pair of words delimited by `/` as a value, word left of the `/` will be used as a value for `Male` and word right
    of the `/` will be used as a `Female` value. With this you can map a value to default `Male` and `Female` words.
    
    *syntax*:
    ```json
    {"field_name":  "gender", "type" :  "personal.gender", "set_val" :  "M/F"}
    ```
   
8. **language :** Generates a random language name. such as `German, Spanish...` etc
    
    *syntax*:
    ```json
    {"field_name":  "lang", "type" :  "personal.language"}
   ```
9. **university :** Generates a random university name such as `University of Texas, Luxemborough Univeristy...` etc

    *syntax*:
    ```json
    {"field_name":  "university_name", "type" :  "personal.university"}
   ```
10. **title :** Generates a title value. such as `Mr, Ms, Dr ...` etc

    *syntax*:
    ```json
    {"field_name":  "title", "type" :  "personal.title"}
   
    ```
    
**location:**
- country
- city
- latitude
- longitude
- phone
- state
- country_code
- postal_code
- address
- timezone
- airports
- municipality
    
**commerce:**
- credit_card
- credit_card_type
- currency
- currency_code

**it:**
- ip_address_v4
- ip_address_v6
- email_address
- mac_address
- username
- sha1
- sha256
- domain_name

**advanced:**
- custom_list
- concatenate
- user_function

**statistics:**
- normal
- possion
    