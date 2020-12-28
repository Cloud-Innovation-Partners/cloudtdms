## Providers

`cloudtdms` uses concept of `generator` function to generate synthetic data. Each `generator` function is capable of generating
random sequence of data. A `generator` function can be as simple as 

```python
def example_provider(number_of_records, args):
    return range(int(number_of_records))
```

or it can be a complex statistical function calculating various stats from the data.

`CloudTDMS` has many in-built providers that can be used for generating synthetic data for specific purpose.
**`Providers`** in `CloudTDMS` refers to a collection of `generator` functions that generate realistic synthetic data for a
specific category. for example, **`personal`** is a provider and it is comprised of following `generator` functions `first_name`,
`last_name`, `gender` etc. **`personal`** provider can be used to generate personal data. Similarly, **`location`** provider 
can generate `location` data such as `country`, `city` etc.

Following is the list of providers available in cloudtdms.
Each provider has a collection of generator functions available that can be used to generate data related to the provider class

- ### Basics
1. **boolean :** Generates a `boolean` value `true,false`, you can provide custom values instead of `default` value using
    `set_val` attribute. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
    + *set_val* : takes a pair of words delimited by `,` as a value, word left of the `,` will be used as a value for true and word right
    of the `,` will be used as a false value
    + *completeness* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    *syntax*:
    ```json
    {"field_name" : "status", "type" : "basics.boolean", "set_val": "1,0", "completeness":"60%"}
    ```
    This will generate value `1` for true and `0` for false.

2. **frequency :** Generates a frequency values from the set `[Never, Seldom, Once, Often, Daily, Weekly, Monthly, Yearly]`. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
      + *completeness* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    *syntax*:
    ```json
    {"field_name" :  "freq", "type" :  "basics.frequency","completeness":"70%"}
    ```
3. **color :** Generates a random color value based on the format specified. By `default` the format is `hex-color`, and it
    will generate hex color codes such as : `#1423ab`. Formats available are `name`, `short-hex`, `hex-color`. You can also specify how much of the data should be present in this column by `completeness` attribute. 
       
    + *format* : used to specify the format of generated color value, Takes a value out of the following three values:
        + *`name`* : will generate color names such as, `Red, Blue, Green ...` etc.
        + *`short-hex`* : will generate hex color codes in short form such as `#14b, #876 ...` etc.
        + *`hex-color`* : will generate hex color codes such as `#1423ab`, This is default format
    
    + *completeness* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
        
    *syntax*:
    ```json
    {"field_name" : "colour", "type" : "basics.color", "format" :  "hex-code","completeness":"45%"}
    ```
4. **words :** This generates a list of random english words. such as 
    `food character prepare outside leg`
    `house food cat rice owl`
     The number of words that need to be generated can be specified by setting the values to the attributes `atleast` and
     `atmost`.  
     You can also specify how much of the data should be present in this column by `completeness` attribute. 
     
     + *`atleast`* : used to specify at least how many words must be generated, `deafult` value is `1`
     + *`atmost`* : used to specify at most how many words can be in generated list, `default` value is `3`
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    *syntax*:
    ```json
    {"field_name" :  "captcha", "type" :  "basics.words", "atleast" :  "5", "atmost" :  "15","completeness":"65%"}
    ```
    
5. **sentence :** This generates a collection of sentences, such as
    `Have heart cover analysis carry. Or candidate trouble listen ok. Way house answer start behind old.`
    
    The number of sentences that need to be generated can be specified by setting the values to the attributes `atleast` and
    `atmost`.
    You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
    + *`atleast`* : used to specify at least how many sentences must be generated, `default` value is `1` 
    + *`atmost`* : used to specify at most how many sentences can be in generated in a collection, `default` value is `10`
    + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    
     *syntax*:
    ```json
    {"field_name" :  "text", "type" :  "basics.sentence", "atleast" :  "5", "atmost" :  "10","completeness":"50%"}
    ```
    
6. **blank :** This is used to generate `null` value always.

    *syntax*:
    ```json
    {"field_name" :  "empty", "type" :  "basics.blank"}
    ```
7. **guid :** Generates global unique identity number, a 36 charcter hex such as `ddee19bc-84fd-4627-897c-dec7c8010977`. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    

    *syntax*:
    ```json
    {"field_name" :  "uuid", "type" :  "basics.guid","completeness":"40%"}
    ```    
8. **password :** Generates a random string of characters, the length of the string can be tweaked using the `length` attribute.
    The `default` length of the string is `8` characters. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
      + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    *syntax*:
    ```json
    {"field_name" :  "passcode", "type" :  "basics.password", "length" :  12,"completeness":"30%"}
    ``` 
9. **auto_increment :** This generates a sequence of numbers with a common difference equal to the value of `increment` attribute.
    The `default` value of `increment` is `1`. Other attributes provided are:
    
    + *`prefix`* : used to append a `prefix` value before the number such as `INC2000`.
    + *`suffix`* : used to append a `suffix` value after the number such as `2000PR`
    + *`start`* : used to specify the starting integer value for the sequence, the `default` start value is `1`
    + *`increment`* : used to specify the increment value `default` is 1
    + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    *syntax*:
    ```json
    {"field_name" :  "id", "type" :  "basics.auto_increment", "prefix" :  "INC", "suffix" :  "NZD", "start":  2000, "increment" :  5,"completeness":"70%"}
    ```
10. **random_number :** This generates a sequence of random numbers between the `start` and `end` value.  You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
    + *`start`* : used to specify the starting value for the sequence, no number generated will be less then this value
    + *`end`* : used to specify the end value for the sequence, no number generated will be greater then this value
    + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    *syntax*:
    ```json
    {"field_name" :  "random_id", "type" :  "basics.random_number", "start" :  20, "end" :  200,"completeness":"60%"}
    ```
    
11. **number_range :** This generates a sequence of numbers within a specified range, the range is set using attributes
    `start`, `end` and  an `increment`. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
    + *`start`* : used to specify the starting value for the sequence, no number generated will be less then this value
    + *`end`* : used to specify the end value for the sequence, no number generated will be greater then this value
    + *`increment`* : used to specify the increment value `default` is 1
    + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    *syntax*:
    ```json
    {"field_name" :  "range", "type" :  "basics.number_range", "start" :  20, "end" :  200, "increment":1, "comleteness":"80%"}
    ```

- ### Personal

1. **first_name :** Generates random First Names. You can also specify how much of the data should be present in this column by `completeness` attribute.
    
    + *category* : takes two values `male` and `female`, when category is set names specific to particular gender are generated.
    + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    *syntax*:
    ```json
    {"field_name":  "fname", "type" :  "personal.first_name", "category" :  "male", "completeness":"60%"}
    ```
   
2. **last_name :** Generates random Last Names. You can also specify how much of the data should be present in this column by `completeness` attribute.
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    *syntax*:
    ```json
    {"field_name":  "lname", "type" :  "personal.last_name", "completeness":"90%"}
    ```
   
3. **full_name :** Generates a Full Name having format `{first_name} {last_name}` such as `John Sarcozy` etc. You can also specify how much of the data should be present in this column by `completeness` attribute.
    
    + *category* : takes two values `male` and `female`, when category is set full names specific to particular gender are generated.
    + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
     *syntax*:
    ```json
    {"field_name":  "name", "type" :  "personal.full_name", "category" :  "female", "completeness":"70%"}
    ```
4. **gender :** Generates a random value from a set `['Male', 'Female']`, you can provide custom values instead of `default` value using
    `set_val` attribute. You can also specify how much of the data should be present in this column by `completeness` attribute.
    
    + *set_val* : takes a pair of words delimited by `,` as a value, word left of the `,` will be used as a value for `Male` and word right
    of the `,` will be used as a `Female` value. With this you can map a value to default `Male` and `Female` words.
    + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    *syntax*:
    ```json
    {"field_name":  "gender", "type" :  "personal.gender", "set_val" :  "M,F", "completeness":"60%"}
    ```
   
5. **username :** Generates a random username such as `dvicary3, dpomeroya...` etc. You can also specify how much of the data should be present in this column by `completeness` attribute.

    + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.

    *syntax*:
    ```json
    {"field_name" :  "username", "type" :  "personal.username", "completeness":"50%"}
    ```

6. **email_address  :** Generates an email address. such as `jslivia01@gmail.com, kwills89@yahoo.com ...` etc. You can also specify how much of the data should be present in this column by `completeness` attribute.

     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.

    *syntax*:
    ```json
    {"field_name" :  "email", "type" :  "personal.email_address", "completeness":"50%"}
    ```
   
7. **language :** Generates a random language name. such as `German, Spanish...` etc. You can also specify how much of the data should be present in this column by `completeness` attribute.

     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    *syntax*:
    ```json
    {"field_name":  "lang", "type" :  "personal.language", "completeness":"40%"}
   ```
8. **university :** Generates a random university name such as `University of Texas, Luxemborough Univeristy...` etc.  You can also specify how much of the data should be present in this column by `completeness` attribute.

      + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.

    *syntax*:
    ```json
    {"field_name":  "university_name", "type" :  "personal.university", "completeness":"40%"}
   ```
9. **title :** Generates a title value. such as `Mr, Ms, Dr ...` etc. You can also specify how much of the data should be present in this column by `completeness` attribute. 

       + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.

    *syntax*:
    ```json
    {"field_name":  "title", "type" :  "personal.title", "completeness":"70%"}
    ```
   
  
   **Localisation** :
   Localised data can be generated from `personal` provider by specifying the `locale` attribute in corresponding `generator`
   function.

   >**Note :** Before using `locale` attribute check if the localised data is available.

   *example*: 
   
   ```json
   {"field_name":  "fname", "type" :  "personal.first_name", "category" :  "male", "locale" : "en_GB"}
   ```

    
- ### Location
1. **country :** Generates a random `country` name such as `United Kingdom, Spain, Algeria...` etc. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    *syntax*:
    ```json
    {"field_name":  "country", "type" :  "location.country", "completeness":"50%"}
    ```
   
2. **city :** Generates a random `city` name such as `New York, Berlin, London...` etc. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    

    *syntax*:
    ```json
    {"field_name":  "city", "type" :  "location.city", "completeness":"40%"}
    ```
   
3. **latitude :** Generates a random `latitude` value such as `48.52469361225269, 72.26886762838888, -12.592370752117404...` etc. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    

    *syntax*:
    ```json
    {"field_name":  "lat", "type" :  "location.latitude", "completness":"60%"}
    ```    
4. **longitude :** Generates a random `longitude` value such as `-45.15259533671917, 115.70563293321999, 81.9426325226724...` etc. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    
    *syntax*:
    ```json
    {"field_name":  "long", "type" :  "location.longitude", "completeness":"30%"}
    ```
5. **phone_number :** Generates a random `phone` number, based on the format value specified. phone numbers generated can be atmost 15 digit
    long. you can specify the format value using `#` (hashs) few format options are listed below for your reference.You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
    + *format* : takes a string of `#` as a value each `#` will be replaced by positive integer to generate a phone number.
    
    example format strings:
    - `###-###-####`
    - `(###)-###-####`
    - `### ### ####`
    - `+# ### ### ####`
    - `+# (###) ###-####`
    - `#-(###)-###-####`
    - `##########`
    
    + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    *syntax*:
    ```json
    {"field_name" :  "mobile", "type" :  "location.phone_number", "format" :  "###-###-####", "completeness":"40%"}
    ```
    
6. **state :** Generates a random state or province name such as `Stockholm, Quebec, New York...` etc. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.

    *syntax*:
    ```json
    {"field_name" :  "state", "type" :  "location.state", "completeness":"50%"}
    ```
7. **country_code :** Generates a random country code, by `default` it will generate `2-DIGIT-ISO-CODES` such as `AF, AQ, IN...` etc.
    But you can generate `3-DIGIT-ISO-CODES` such as `AFG, ATA, IND..` etc or numeric country codes such as `93, 672, 91...` etc.
    by set the value to the attribute `category`. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    + *category* : takes one of the three values `numeric` or `2-digit-iso-code` or `3-digit-iso-code`
    
    *syntax*:
    ```json
    {"field_name" :  "code", "type" :  "location.country_code", "category" :  "numeric", "completeness":"50%"}
    ```
    
8. **postal_code :** Generates a random postal code. such as `56273, 40741...` etc. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    *syntax*:
    ```json
    {"field_name" :  "p_code", "type" :  "location.postal_code", "completeness":"40%"}
    ```
    
9. **address :** Generates a random address such as `78 Saint Paul Road, 836 Gale Road...` etc. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.

    *syntax*:
    ```json
    {"field_name" :  "address", "type" :  "location.address", "completeness":"40%"}
    ```
10. **timezone :** Generates a timezone value
    
    *syntax*:
    ```json
    {"field_name" :  "tz", "type" :  "location.timezone"}
    ```
11. **airport :** Generates a random airport name. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.

    *syntax*:
    ```json
    {"field_name" :  "airport", "type" :  "location.airport", "completeness":"90%"}
    ```
12. **municipality :** Generates  a random municipality name. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.

    *syntax*:
    ```json
    {"field_name" :  "municipality", "type" :  "location.municipality", "completeness":"40%"}
    ```
    
   
   **Localisation** :
   Localised data can be generated from `location` provider by specifying the `locale` attribute in corresponding `generator`
   function.

   >**Note :** Before using `locale` attribute check if the localised data is available.

   *example*: 
   
   ```json
   {"field_name":  "city", "type" :  "location.city", "locale" : "en_US"}
   ```

- ### Company

1. **company_name :** Generates a random company name. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    *syntax*:
    ```json
    {"field_name" :  "cname", "type" :  "company.company_name", "completeness":"60%"}
    ```
    
2. **department :** Generates a department type such as `Human Resource, Accounting, Engineering, Grocery, Books ...` etc
    department names can be either of `retail` category or `coporate` category. You can specify the category type by add a value
    to `category` attribute. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    + *`category`* : used to specify the category type, can take two values `retail` and `corporate`, by `default` the category
    has `all` value which will generate a randomly any name out of the two categories.
    
    *syntax*:
    ```json
    {"field_name" :  "dept", "type" :  "company.department", "category" :  "corporate", "completeness":"80%"}
    ```  
 3. **duns_number :** Generates random 9 digit Data Universal Numbering System (DUNS) number such as `31-300-8468, 34-230-3150...` etc. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
 
    *syntax*:
    ```json
    {"field_name":  "duns_id", "type" :  "company.duns_number", "completeness":"40%"}
    ```
  **```The `company` provider currently supports `en_GB` locale. ```**

- ### Commerce

1. **credit_card :** Generates a random credit card number. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    *syntax*:
    ```json
    {"field_name" :  "card", "type" :  "commerce.credit_card","completeness":"80%"}
    ```
   
2. **credit_card_type :** Generates credit card type such as `AmericanExpress, MasterCard...` etc. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.

    *syntax*:
    ```json
    {"field_name" :  "ctype", "type" :  "commerce.credit_card_type", "completeness":"40%"}
    ``` 
3. **currency :** Generates a random currency name such as `Dollar, Rupee, Euro ...` etc. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.

    *syntax*:
    ```json
    {"field_name" :  "money", "type" :  "commerce.currency", "completeness":"20%"}
    ```
4. **currency_code :** Generates a random currency code such as `USD, EUR, INR ...` etc. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.

    *syntax*:
    ```json
    {"field_name" :  "ccode", "type" :  "commerce.currency_code", "completeness":"60%"}
    ```

- ### IT

1. **ip_address :** Generates an IP address. such as `192.168.0.1, 251.150.202.132... `etc for `v4` category, 
    `43de:c4ea:7529:ebbc:754b:81a:be18:d2a1, 10d0:c44:63d:401a:440b:538f:8afc:fb0f...` etc for `v6` category
    You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    + *category* : takes value either `v4` or `v6`
    
    *syntax*:
    ```json
    {"field_name" :  "ip", "type" :  "it.ip_address", "category" :  "v6", "completeness":"40%"}
    ```

2. **mac_address :** Generates a random `MAC address` such as `69:9b:fd:f0:c8:38, f4:d0:0c:d6:b8:b4 ...` etc. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.

    *syntax*:
    ```json
    {"field_name" :  "mac", "type" :  "it.mac_address", "completeness":"70%"}
    ```

3. **sha1 :** Generates a random `SHA1` hex code string such as `f4fead60f28167de02e53c68d5fc3689a8d648ea`. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.

    *syntax*:
    ```json
    {"field_name" :  "sha1", "type" :  "it.sha1", "completeness":"60%"}
    ```

4. **sha256 :** Generates a random `SHA256` hex code string such as `ca7adf64d8112bddcb0c55ff6e92a5b553c0fc92117e494230b27afddb048ebe`. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.

    *syntax*:
    ```json
    {"field_name" :  "sha256", "type" :  "it.sha256", "completeness":"40%"}
    ```
5. **domain_name :** Generates a random domain name such as `apache.org, google.com ...` etc. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.

    *syntax*:
    ```json
    {"field_name" :  "domain", "type" :  "it.domain_name", "completeness":"70%"}
    ```
- ### Dates

1. **date :** Generates a random `date` , based on the format value specified. The default value for format is `dd/mm/YYYY`. 
    Few format options are listed below for your reference. 

    + *format* : takes a format string as a value
    + *start* : used to specify the starting value for date.
    + *end* :used to specify the starting value for date.
    
     >**Note :** The separator in `format` and `start`, `end` must be same.
        
    example format strings:
    - `mm/dd/yy`
    - `mm/dd/YYYY`
    - `YYYY/mm/dd`
    - `mm-dd-YYYY`
    - `mm.dd.YYYY`
    
    You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    *syntax*:
    ```json
    {"field_name" :  "date", "type" :  "dates.date","format":"mm-dd-YYYY","start":"12-07-2020","end":"12-08-2023", "completeness":"50%"}
    ```
  
2. **day :** Generates a list of weekdays. Such as `Fri, Sat, Thu... `etc. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
   
    *syntax*:
    ```json
    {"field_name" :  "day", "type" :  "dates.day", "completeness":"40%"}
    ```
3.  **month :** Generates a list of months. Such as `September, November, February... `etc. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
   
    *syntax*:
    ```json
    {"field_name" :  "month", "type" :  "dates.month", "completeness":"50%"}
    ```
   
4. **time :** Generates a list of time. Such as `19:30:24, 13:44:13, 20:56:28... `etc. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
   
    *syntax*:
    ```json
    {"field_name" :  "time", "type" :  "dates.time", "completeness":"80%"}
    ```
   
 5. **timestamp :** Generates a list of timestamps based on format value specified. Such as `17/08/2017 02:11`,`2007-09-30 06:15:22, 2011-04-26 11:23:21... `etc.
                    The default value for format is `dd/mm/YYYY HH:MM`
                   
    + *format* : takes a format string as a value
    + *start* : used to specify the starting value for timestamp.
    + *end* :used to specify the starting value for timestamp.
    
    >**Note :** The separator in `format` and `start`, `end` must be same.
        
    example format strings:         
    - `mm/dd/yy HH:MM:SS`         
    - `mm/dd/yy HH:MM`            
    - `mm/dd/YYYY HH:MM:SS`       
    - `mm/dd/YYYY HH:MM`          
    - `YYYY/mm/dd HH:MM:SS`      
    - `YYYY/mm/dd HH:MM`         
    - `mm-dd-YYYY HH:MM:SS`            
    - `mm-dd-YYYY HH:MM`         
    - `mm.dd.YYYY HH:MM:SS`       
    - `mm.dd.YYYY HH:MM`
    - `dd/mm/YYYY HH:MM:SS`
    - `dd/mm/YYYY HH:MM`
    - `dd/mm/yy HH:MM:SS`
    - `dd/mm/yy HH:MM`
    
    You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
   
    *syntax*:
    ```json
    {"field_name" :  "timestamp", "type" :  "dates.timestamp", "format":"mm/dd/YYYY HH:MM","start":"12/07/2020","end":"12/08/2023", "completeness":"60%"}
    ```


- ### Advanced

1. **custom_list :** Generates a random value from a user specified list. With `custom_list` you can simulate generation of
    any finite set as per your needs. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
         
    + *set_val* : here `set_val` takes a comma separated string, which will be used as a domain set for data generation
     
    *syntax*:
    ```json
    {"field_name" :  "teams", "type" :  "advanced.custom_list", "set_val" :  "HR, Accounts, Development, Field, Transport", "completeness":"40%"}
    ```
   
    Based on the value provided in the `set_val` attribute function can generate any specific finite data e.q
    the schema notation above will generate data such as `HR, Field, Transport, Development, HR, Accounts ...` etc

2. **concatenate :** Concatenates values from multiple columns into one. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    + *template* : take a template string as a value, A template string has `field_names` to be concatenated enclosed in `{}` braces.
    Besides `field_names` you can also use static strings and symbols like `$,#@..` etc
    
    *syntax*:
    ```json
    {"field_name" :  "mixed", "type" :  "advanced.concatenate", "template" :  "{synthetic.id}-{synthetic.teams}", "completeness":"50%"}
    ```
   
   *example* :
   ```python
   {"field_name" :  "row", "type" :  "basics.auto_increment", "start" :  5000}
   {"field_name" :  "id", "type" :  "basics.random_number", "start" :  2000, "end" :  3000}
   {"field_name" :  "teams", "type" :  "advanced.custom_list", "set_val" :  "HR, Accounts, Development, Field, Transport"}
   {"field_name" :  "mixed", "type" :  "advanced.concatenate", "fields" :  "{synthetic.id}-{synthetic.teams}#{synthetic.row}"}
   ```
   The Above `schema` will generate data something like this
   
   |row    |id   |teams       |mixed                 |
   |-------|-----|------------|----------------------|
   |5000   |2000 |HR          |2000-HR#5000          |
   |5001   |2222 |Account     |2222-Account#5001     |
   |5002   |2431 |Development |2431-Development#5002 | 

3. **custom_file :** Generates data using user data set. If you want to generate a data for a column using your data set you can use
    `custom_file` function.
    
    + *name* : name of the `csv` file `(the file must be in user-data folder)`. only `csv` is supported currently.
    
    + *column* : used to specify which column to use from your data set for data generation. This attribute takes `value` 
    based on the value of `ignore_headers` attribute. If `ignore_headers` is set to `yes` then it takes integer value which  
    refers to the index of the column, and if `ignore_headers` is set to `no` it takes a string which refers to a column name in
    the data set. 
    
    + *ignore_headers* : it can be `yes` or `no`, by default it is set to `yes`. Based on this value `column` attribute will change its definition.
    
    *syntax*:
    ```json
    {"field_name" :  "custom_column", "type" :  "advanced.custom_file", "name" :  "my_data_set", "column" :  "4", "ignore_headers" :  "yes"}
    ```
   
   **Data Masking / Data Obfuscation  :**
   
   With `custom_file` function, you can use data masking options to mask your custom data. Following are the available options
   for generating masked data from your data set.
   
   + *encrypt* : With this option you can apply encryption on the data column, this option takes a dictionary as a value 
                 which contains the `encryption_key` and `type` of encryption to be used for the process. In case no key 
                 is provided, encryption process will not be applied.
     
     - *type* : This attribute is used to specify the type of encryption to be used in the process. Currently `cloutdms`
                has support for following encryption techniques:
                `fernet`, `caesar`, `monoaplha`, `onetimepad`, `aes`. The `type` attribute can take any one of the value from
                these techniques. For more information check `data_masking` document.
     
     - *key* : This attribute is used to specify the encryption key. Key value need to be string or integer depending on the
               the technique used to encrypt. e.q in `caesar` cipher key must always be integer else exception will be raised
                
     *syntax*:
                 
      ```json
        {
        "field_name" :  "custom_column", 
        "type" :  "advanced.custom_file", 
        "name" :  "my_data_set", 
        "column" :  "4", 
        "ignore_headers" :  "yes", 
        "encrypt": {"type": "caesar","key" : 9797 }
        }
      ```
     
   + *mask_out* : With this option you can apply character substitution to values. You can replace a value character 
                  with a symbol such as `*` or `x` etc. to mask the actual data. This option takes a dictionary value 
                  comprising three keys.
                  
     - *with* : This attribute takes a single character as value such as `*` or `x` which will be used as a substitute value
                for masking the actual characters.
     - *character* : This take an integer value specifying the number of characters to mask out.
     
     - *from* : This option takes three values `start`, `end`, `mid` each refers to the starting point for carrying the masking
                operation
                
     In the example below the first 5 characters for all values in the 4th column from data file `my_data_set` will be masked with the character `*`                 
                 
     *syntax*:
                 
        ```json
        {
        "field_name" :  "custom_column", 
        "type" :  "advanced.custom_file", 
        "name" :  "my_data_set", 
        "column" :  "4", 
        "ignore_headers" :  "yes", 
        "mask_out" : {"with" : "*", "characters" : 5, "from" : "start"}
        }
        ```
   + *shuffle* : This option takes a boolean  value, specifying whether the data in the column should be shuffled or not.
     
     *syntax*:
                 
        ```
        {
        "field_name" :  "custom_column", 
        "type" :  "advanced.custom_file", 
        "name" :  "my_data_set", 
        "column" :  "4", 
        "ignore_headers" :  "yes", 
        "shuffle": True
        }
        ```
   + *set_null* : If you want to make the column values null, you can set this value to `True`, It will make the whole column
                  as null.
                 
     *syntax*:
                 
        ```
        {
        "field_name" :  "custom_column", 
        "type" :  "advanced.custom_file", 
        "name" :  "my_data_set", 
        "column" :  "4", 
        "ignore_headers" :  "yes", 
        "set_null": True
        }
        ```             
   
   
    

- ### Statistics
    
1. **normal :** Generates random numbers from a `normal distribution`. Such as `0.51984538, -0.01018767, -2.07595922', -0.35596830...`etc. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
           
    + *center* : used to specify the `mean` of the distribution.
    
    + *std_dev* : used to specify the `standard deviation` (spread or "width") of the distribution. Must be non-negative.

    + *decimals* : specify the decimal places in each number.
    
   *syntax*:
    ```json
    {"field_name" :  "normal", "type" :  "statistics.normal", "center" : 5, "std_dev" : 1, "decimals" : 2, "completeness":"50%"}
    ```
            
2. **poisson :** Generates random numbers from a `poisson distribution` with a specific mean value. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
                
    + *mean* : is expectation of interval, must be >= 0. A sequence of expectation intervals must be broadcastable over
               the requested size.
    
    *syntax*:
    ```json
    {"field_name" :  "poisson", "type" :  "statistics.poisson", "mean" : 5,"completeness":"80%"}
    ```
             
3. **binomial :** Generates random numbers from a binomial distribution with a specific probability of success. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    + *success_rate* : is parameter of the distribution, >= 0 and <=1.
 
    *syntax*:
    ```json
    {"field_name" :  "binomial", "type" :  "statistics.binomial", "success_rate" : 0.5, "completeness":"90%"}
    ```
            
4. **exponential :** Generates random numbers based on an exponential distribution with a specific `λ` rate. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.       
    
    + *scale* : must be non-negative.
    
    *syntax*:
    ```json
    {"field_name" :  "exponential", "type" :  "statistics.exponential", "scale" : 4, "completeness":"80%"}
    ```
            
 5. **geometric :** Generates numbers based from a `geometric distribution` with a specific probability of success. You can also specify how much of the data should be present in this column by `completeness` attribute. 
    
     + *`completeness`* : takes the percentage value, which signifies the completeness of the data in the column. If this attribute is not mentioned it will take the global `completeness` value.
    
    + *success_rate* : is the probability of success of an individual trial, >= 0 and <=1.
    
    *syntax*:
    ```json
    {"field_name" :  "geometric", "type" :  "statistics.geometric", "success_rate" : 0.4, "completeness":"70%"}
    ```
   
