# Data Masking / Data Obfuscation

Data masking or data obfuscation is the process of hiding original data with modified content, the main reason for applying 
masking to a data field is to protect data that is classified as personally identifiable information, sensitive personal data, 
or commercially sensitive data. [*courtesy* : [wikipedia](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjftM33iLbrAhWC8HMBHQlDBEMQmhMwJXoECAMQAg&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FData_masking&usg=AOvVaw2RlM7u4zsoU6I2zbbJGBot)]

In an organisation data may be needed at various fronts such as `Analysis`, `Training`, `DevOps`, `3rd Party` or `Development`. Using
production data is always going to cost you with regards to compliance and security. `CloudTDMS` provides you an option to 
anonymize personally identifiable information and hide sensitive data by masking it using various data masking techniques.

## Scope 
With `CloudTDMS` you can perform various data masking operations besides generating synthetic data. You can:

+ Anonymize sensitive data with synthetic data
+ Encrypt data with available encryption techniques
+ Perform masking using pseudo characters
+ Shuffle data
+ Perform nullying and deletion operations

## Basic Usage
We shall take an example to describe the basic usage of the data masking feature. Suppose we have a sample bank data named 
**`Churn-Modeling.csv`** with following contents. We shall apply various data masking technique on this data.

 >**Note** : Each of the data masking attribute requires `source` attribute to be present.

```csv
RowNumber,CustomerId,Surname,CreditScore,Geography,Gender,Age,Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary,Exited
1,15634602,Hargrave,619,France,Female,42,2,0,1,1,1,101348.88,1
2,15647311,Hill,608,Spain,Female,41,1,83807.86,1,0,1,112542.58,0
3,15619304,Onio,502,France,Female,42,8,159660.8,3,1,0,113931.57,1
4,15701354,Boni,699,France,Female,39,1,0,2,0,0,93826.63,0
5,15737888,Mitchell,850,Spain,Female,43,2,125510.82,1,1,1,79084.1,0
```
### Steps


1. Create a `connection` entry named `modeling` inside `config_default.yaml` for the source CSV file like:

   ```yaml
    csv:
       modeling:          # Connection Name
          source: ""        # source is usually a path to CSV data file
          target: ""        # target is usually a path to local folder where data must be saved
   ```
   
2. Create a configuration inside **`config`** folder with name say `example.py`. Now we shall create a **`STREAM`** variable 
   which represents a python dictionary for specifying our configuration. `cloudtdms` will load your configuration and start the 
   data generation process. You can find your generated data inside **`data`** folder of `cloudtdms`.
   
   Following is an example configuration.
   
    ```
    STREAM = {
        "number": 1000,
        "title": 'Stream6',
        "frequency": "once"
       
        "encryption": {
         "type": "caesar",
         "key": "Jd28hja8HG9wkjw89yd"
         },
         
         "mask": {
         "with": "x",
         "characters": 4,
         "from": "mid"
         },
        
        "source": {
           "csv": [
                  {"connection": "modeling", "delimiter": ","},
             ]
        },
        
        "substitute" : {
                 "csv.modeling.Surname" : {"type" : "personal.last_name"},
                 "csv.modeling.Gender" : {"type": "personal.gender"},
                 "csv.modeling.Geography" : {"type" : "location.country"}
       },
       
        "encrypt": {
          "csv.modeling.EstimatedSalary",
          "csv.modeling.Balance"
        },
        
        "mask_out": {
            "csv.modeling.CustomerId"
        },
        
        "shuffle": {
            "csv.modeling.NumOfProducts",
            "csv.modeling.IsActiveMember"
        },
        
        "nullying" : {
                  "csv.modeling.RowNumber"
        },
          
           
        "synthetic": [
            {"field_name": "email", "type": "personal.email_address"},
            {"field_name": "univ", "type": "personal.university"},
        ],
        
        "output_schema": {
        "csv.modeling.Surname" ,
        "csv.modeling.Gender" ,
        "csv.modeling.Geography",
        "csv.modeling.EstimatedSalary",
        "csv.modeling.Balance",
        "csv.modeling.CustomerId",
        "csv.modeling.NumOfProducts",
        "csv.modeling.IsActiveMember",
        "csv.modeling.RowNumber",
        "synthetic.email","synthetic.univ",
     }
       
    }
    ``` 

## Data Masking

1. **Anonymization / Substitution :**
   Anonymization or substitution, substitutes realistic but false data for the original to ensure privacy. It is used to 
   allow for testing, training, application development, or support personnel to work with the data set without sharing 
   sensitive data.
   
   In order to use anonymization technique on Personal Identifiable Information (PII), you can choose a compatible realistic data
   provider from the list of providers in the `cloudtdms`. Once you have found a compatible provider, you can use that to
   generate substitute value for your real data. For example, in case of bank data example mentioned above. The PII are 
   `Surname`, `Gender`, `Country`. In order to anonymize PII's in the data file we use **`substitute`** attribute in our 
   configuration. The substitute attribute takes a dictionary as value, where `key` represents the column in the data
   file and `value` represents a `cloudtdms` provider to be used as substitute value. 
   
   In the below code snippet we took `last_name` provider from the `personal` category of the `cloudtdms` to be used as a 
   substitution value for the `Surname` data. The `last_name` provider is going to generate synthetic data for the column `Surname`.
   Similarly, we have used `gender` provider from the `personal` category to replace `Gender` and `country` provider from 
   `location` category to replace `Geography` values in the real data. 
   ```
    STREAM = {
    "number": 1000,
    "title": 'substitute_example',
    "frequency": "once",
    
    "source": {
           "csv": [
                  {"connection": "modeling", "delimiter": ","},
             ]
        },
    
      "substitute" : {
                 "csv.modeling.Surname" : {"type" : "personal.last_name"},
                 "csv.modeling.Gender" : {"type": "personal.gender"},
                 "csv.modeling.Geography" : {"type" : "location.country"}
       },
    
    }
   ```
    
2. **Encryption :**
   Encryption is very secure, but you lose the ability to work with or analyze the data while it’s encrypted. It is a good 
   obfuscation method if you need to store or transfer data securely.
   
   In order to use encryption on an sensitive data, you can choose type of encryption to be used from the various encryption's
   supported by `cloudtdms`. *encryption's are resource intensive's, they consume lot of processing power and are usually
   time consuming*.   
   
   In case of bank data example mentioned above. We are using encryption for two columns `EstimatedSalary`, `Balance`,
   To encrypt the values for these columns we need to use attribute `encryption` inside our `STREAM` dictionary. `encryption` 
   take a dictionary as a value which contains information about the `type` of encryption and `key`. `encrypt` attribute is a `set` which contains the names 
   of the columns to be used for encryption. Lets discuss each attribute of `encryption` attribute.
   
    - *type* : This attribute is used to specify the type of encryption to be used in the process. Currently `cloutdms`
                has support for following encryption techniques:
                `fernet`, `caesar`, `monoaplha`, `onetimepad`, `aes`. The `type` attribute can take any one of the value from
                these techniques.
     
    - *key* : This attribute is used to specify the encryption key. Key value need to be string or integer depending on the
               the technique used to encrypt. e.q in `caesar` cipher key must always be integer else exception will be raised
    
    `encryption` attribute is an optional attribute. By default this attribute gets its values from `config_default.yaml` file. 
     In order to override the default behaviour we can define the `encryption` attribute within the scope of STREAM and set the values for `type` and 
    `key` attributes specific to current STREAM. 
  
   ```
    STREAM = {
    "number": 1000,
    "title": 'encrypt_example',
    "frequency": "once",
    
    "source": {
           "csv": [
                  {"connection": "modeling", "delimiter": ","},
             ]
        },

    "encryption": {
         "type": "caesar",
         "key": "Jd28hja8HG9wkjw89yd"    "source": 'Churn-Modeling',
         },
         
    "encrypt": {
          "csv.modeling.EstimatedSalary",
          "csv.modeling.Balance"
        },
    }
   ```
   
    **Different Types of Encryption Techniques Available in CloudTDMS**
    
    Following are the encryption/cipher techniques provided by `CloudTDMS` for data masking and obfuscation purpose. In order
    to use any of the supported ciphers techniques you can use the associated value name in the below table in the `type` 
    attribute of `encrypt` attribute of your `STREAM` variable.
    
    | Name                               | value       |
    |------------------------------------|-------------|
    | Fernet (Symmetric Encryption)      |`fernet`     |
    | Caesar Cipher                      |`caesar`     |
    | One Time Pad                       | `onetimepad`|
    | Mono-Alphabetic Cipher             |`monoalpha`  |
    | Advanced Encryption Standard (AES) |`aes`     |
    
    Let's discuss each cipher techniques briefly:
    
    + **Fernet (Symmetric Encryption):** `Fernet` is a name of Symmetric-key algorithm provided by the cryptography library
    that use the same cryptographic keys for both encryption of plaintext and decryption of ciphertext. The keys may be 
    identical or there may be a simple transformation to go between the two keys.`Fernet` guarantees that a message encrypted 
    using it cannot be manipulated or read without the key.
     
       *example:*
             
            key            :      helloworld123
      
            text           :    My name is Jhon
            
            fernet cipher :   b'gAAAAABfRgB14pvxcSm9CkS1whOVlWdxWmxzKxVW-BM70CBucTNi4YYPpX9jY0GjUEUTb7gPNDuXOyE69k-0Ku4XJDJ0PCOIkg=='
     
    + **Caeser Cipher:** `Caesar cipher` is one of the simplest and most widely known encryption techniques. It is a type of 
    substitution cipher in which each letter in the plaintext is replaced by a letter some fixed number of positions down the 
    alphabet. For example, with a left shift of 3, D would be replaced by A, E would become B, and so on.
                 
      *example:*
      
            key              :  15
      
            text            :   My name is Jhon
            
            caesar cipher  :   BnccpbtcxhcYwdc
      
      >**Note:**  *For `caesar` encryption technique, you must provide the key which contains only integers.*
     
    + **MonoAlphabetic Cipher:** A `Monoalphabetic cipher` uses a fixed substitution for encrypting the entire message. 
    It uses the mapping values which are used for encrypting a message. For example, the mapping values are`{h:J, l:T, o:G, e:P ...}`
    and the message is `hello`. From the mapping values `h` will be replaced with `J`, `e` with `P`, `l` with `T` and so on. 
    Finally the message `hello` will be encrypted as `JPTTG`.
       
     *example:*
      
            text              :   My name is Jhon
            
            monoaplha cipher :   Hw jmhc si Dakj
                   
     >**Note:**  *You don't have to specify a `key` for `monoalpha` encryption technique.* 
     
    + **OneTimePad:** The one-time pad (OTP) is an encryption technique that cannot be cracked, but requires the use of 
    a one-time pre-shared key the same size as, or longer than, the message being sent.      
                    
     *example:*
      
            key        :   helloworld123
            
            text      :    My name is Jhon
            
            onetimepad:   251c4c020e1a0a52051711785b070b 
          
    + **AES:** The Advanced Encryption Standard (AES) is a symmetric block cipher chosen by the U.S. government to protect
              classified information. AES is implemented in software and hardware throughout the world to encrypt sensitive 
              data. It is essential for government computer security, cybersecurity and electronic data protection. AES 
              includes three block ciphers: AES-128, AES-192 and AES-256. AES-128 uses a 128-bit key length to encrypt 
              and decrypt a block of messages, while AES-192 uses a 192-bit key length and AES-256 a 256-bit key length 
              to encrypt and decrypt messages. Each cipher encrypts and decrypts data in blocks of 128 bits using 
              cryptographic keys of 128, 192 and 256 bits, respectively.
              You have to just provide a key and it will convert it into the specified block cipher (AES-128, AES-192 and AES-256)
    
      *example:*
      
            key:    helloworld123
            
            text:  My name is Jhon
            
            aes:   b'\xd3\xf6;i\xad\x01\xfe\xc5\x8a\xdb\xd2\x80\xa3\xfa\xb6A' 
            
            
3. **Masking :**

    This technique is used to mask the column values. By masking we mean replacing the characters of field value of a record with some random
    characters e.g `x` or `#` etc. In case of bank data example mentioned above we are using masking for `CustomerId` column, To mask the values for columns we 
    need to use attribute `mask_out` inside our `STREAM` dictionary.
    `mask_out` attribute takes a set of column names as value. Each column listed inside the `mask_out` attribute will be 
    masked out using the character defined in `with` attribute of `mask` attribute.

    `mask` attribute is an optional attribute that can be used to define what type of masking values to use for `mask_out` in a STREAM.
    By default this attribute gets its values from `config_default.yaml` file. In order to override the default behaviour we can define the `mask`
    attribute within the scope of STREAM and set the values for `with`, `characters` and `from` attributes specific to current STREAM. 
    
    `with` defines what character to use for masking, `characters` defines number of characters to be masked in a field value and `from` defines the alignment
    from where to start the masking operation. `from` takes values as `start`, `mid` and `end`.


```
    STREAM = {
    "number": 1000,
    "title": 'encrypt_example',
    "frequency": "once",

    "source": {
        "csv": [
               {"connection": "modeling", "delimiter": ","},
          ]
     },

   "mask": {
            "with": "x",
            "characters": 4,
            "from": "mid"
         },
        
   "mask_out": {
      "csv.modeling.CustomerId"
   }
}
```

4. **Nullying :** 
 
   Nullying is a simple data masking technique, It replaces all the data in a column with null values. The column is there 
   but there will be no data available. This technique is mostly used when we neither anonymize / substitute the data nor 
   encrypt the data. In order to use `nullying` on an sensitive data, you have to specify which column/columns you want to be 
   nullified. 
   
   In case of bank data example mentioned above. We are using `nullying` for `RowNumber`,
   to nullify the values for these column we need to use attribute `nullying` inside our `STREAM` dictionary. `nullying` key
   take a `set` as a value which contains information about the column/columns which are supposed to be nullified.
   
   ```
    STREAM = {
    "number": 1000,
    "title": 'encrypt_example',
    "frequency": "once",

    "source": {
        "csv": [
               {"connection": "modeling", "delimiter": ","},
          ]
     },

    "nullying" : {
               "csv.modeling.RowNumber"
       },
    }
   ```

5. **Shuffle :** 
    In this technique the original data columns are shuffled in order to break the relativity of data. 
       
   In case of bank data example mentioned above. We are using `shuffle` for `NumOfProducts` and `IsActiveMember`, 
   to `shuffle` the values for these column we need to use attribute `shuffle` inside our `STREAM` dictionary. 
   `shuffle` key take a `set` as a value which contains information about the column/columns which are supposed to be shuffled.
   
   ```
    STREAM = {
    "number": 1000,
    "title": 'encrypt_example',
    "frequency": "once",

    "source": {
           "csv": [
                  {"connection": "modeling", "delimiter": ","},
             ]
        },

    "shuffle": {
            "csv.modeling.NumOfProducts",
            "csv.modeling.IsActiveMember"
        },
    }
    
   ```

                  
                  
                
                
     
        
        
        
