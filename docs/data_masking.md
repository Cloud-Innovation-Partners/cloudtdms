

**Encryption techniques**

The various techniques the the curernt version of `cloudtdms` supports are:
+ *fernet*
+ *ceasar*
+ *monoaplha*
+ *onetimepad*
+ *aes*
 
 **Fernet(symmetric encryption):** `Fernet` guarantees that a message encrypted using it cannot be manipulated or read without the key. `Fernet` 
                                    is an implementation of symmetric (also known as “secret key”) authenticated cryptography.
 
 The syntax for using `fernet` in `cloudtdms` is given below:
 
 *syntax*:
   
    ```json
        {
        "field_name" :  "custom_column", 
        "type" :  "advanced.custom_file", 
        "name" :  "my_data_set", 
        "column" :  "4", 
        "ignore_headers" :  "yes", 
        "encrypt": {"type": "fernet","key" : "your key here"}
        }
      ```
                                     
 
 **Caeser:** `Caesar cipher` is one of the simplest and most widely known encryption techniques. It is a type of
             substitution cipher in which each letter in the plaintext is replaced by a letter some fixed number of 
             positions down the alphabet. For example, with a left shift of 3, D would be replaced by A, E would become
             B, and so on.
             
  *Example:*
  
        Plain:    ABCDEFGHIJKLMNOPQRSTUVWXYZ
        
        Cipher:   XYZABCDEFGHIJKLMNOPQRSTUVW
        
 The syntax for using `caeser` in `cloudtdms` is given below:
 
 *syntax*:
   
    ```json
        {
        "field_name" :  "custom_column", 
        "type" :  "advanced.custom_file", 
        "name" :  "my_data_set", 
        "column" :  "4", 
        "ignore_headers" :  "yes", 
        "encrypt": {"type": "caeser","key" : "your key here"}
        }
      ```
 **Note:**  *For `caesar` encryption technique, you must provide the key which contains only integers.*
 
 
 **monoalpha:** A `Monoalphabetic cipher` uses a fixed substitution for encrypting the entire message. It uses the mapping
                values which are used for encrypting a message. For example, the mapping values are`{h:J, l:T, o:G, e:P ...}`
                and the message is `hello`. From the mapping values `h` will be replaced with `J`, `e` with `P`, `l` with `T`
                and so on. Finally the message `hello` will be encrypted as `JPTTG`.
   
  The syntax for using `monoalpha` in `cloudtdms` is given below:
 
 *syntax*:
   
    ```json
        {
        "field_name" :  "custom_column", 
        "type" :  "advanced.custom_file", 
        "name" :  "my_data_set", 
        "column" :  "4", 
        "ignore_headers" :  "yes", 
        "encrypt": {"type": "monoalpha"}
        }
      ```       
 **Note:**  *You don't have to specify a `key` for `monoalpha` encryption technique.* 
 
 **onetimepad:** The one-time pad (OTP) is an encryption technique that cannot be cracked, but requires the use of 
                a one-time pre-shared key the same size as, or longer than, the message being sent.      
                
  The syntax for using `onetimepad` in `cloudtdms` is given below:
 
 *syntax*:
   
    ```json
        {
        "field_name" :  "custom_column", 
        "type" :  "advanced.custom_file", 
        "name" :  "my_data_set", 
        "column" :  "4", 
        "ignore_headers" :  "yes", 
        "encrypt": {"type": "onetimepad","key":"your key here"}
        }
      ```      
      
 **AES:** The Advanced Encryption Standard (AES) is a symmetric block cipher chosen by the U.S. government to protect
          classified information. AES is implemented in software and hardware throughout the world to encrypt sensitive 
          data. It is essential for government computer security, cybersecurity and electronic data protection. AES 
          includes three block ciphers: AES-128, AES-192 and AES-256. AES-128 uses a 128-bit key length to encrypt 
          and decrypt a block of messages, while AES-192 uses a 192-bit key length and AES-256 a 256-bit key length 
          to encrypt and decrypt messages. Each cipher encrypts and decrypts data in blocks of 128 bits using 
          cryptographic keys of 128, 192 and 256 bits, respectively.
          You have to just provide a key and it will convert it into the specified block cipher (AES-128, AES-192 and AES-256)

 The syntax for using `AES` in `cloudtdms` is given below:
 
 *syntax*:
   
    ```json
        {
        "field_name" :  "custom_column", 
        "type" :  "advanced.custom_file", 
        "name" :  "my_data_set", 
        "column" :  "4", 
        "ignore_headers" :  "yes", 
        "encrypt": {"type": "aes","key":"your key here"}
        }
      ```              
                
                
     
        
        
        
