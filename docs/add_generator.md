# Adding New Generator Function To Provider

`cloudtdms` uses concept of `generator` function to generate synthetic data. Each `generator` function is capable of generating
random sequence of data. A `generator` function has following signature 

```python
def boolean(data_frame, number, args=None):
    """
    Generator function for boolean values
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
   
```

`CloudTDMS` has many in-built providers that can be used for generating synthetic data for specific purpose.

**`Providers`** in `CloudTDMS` refers to a collection of `generator` functions that generate realistic synthetic data for a
specific category. 

for example, **`personal`** is a provider and it is comprised of following `generator` functions `first_name`,
`last_name`, `gender` etc. **`personal`** provider can be used to generate personal data. Similarly, **`location`** provider 
can generate `location` data such as `country`, `city` etc.

`generator` functions are defined inside the `__init__.py` of the `provider` package. Each provider has `__init__.py` file defined that contains definition for various
synthetic `generator` functions.

In order to add a new generator function simply create a function with specified signature as described above and then provide the definition of the function. In function
definition you need to generate the data and add it as a column to the `dataframe` passed as argument to your function.

### Function Arguments
A signature of `generator` function has three arguments `dataframe`, `number` and `agrs`. 
- The `dataframe` is the pandas dataframe that is going to hold all the synthetic data to be generated for the `STREAM`.
- The `number` will define the number of records to generate
- `args` is an important argument that will contain the attribute values associated to generator function, passed by user to your generator function in configuration file

## Example
Let's take an example of `boolean` generator function inside the `basics` provider. Following Steps will be done to integrate `boolean` function to `basics` provider

1. Add a function signature to `__init__.py` file of `basics` provider.

    ```python
    def boolean(data_frame, number, args=None):
        """
        Generator function for boolean values
        :param number: Number of records to generate
        :type int
        :param args: schema attribute values
        :type dict
        :return: list
        """

        #TODO - Function definition
        pass

    ```
2. Provide the definition of the function. Now the boolean function is supposed to generate random  `boolean` values as ouput. First thing to note is how user
   will use this function in his configuration file. Let the following configuration entry define the call to synthetic boolean function

    ```python
    {"field_name": "Activated", "type": "basics.boolean", "set_val": "Y,N"}
    ```
    A `boolean` function can have additional attributes associated to it such as, `set_val` which defines what values to use as boolean value. In current case user wants
    `Y` to represent True and `N` to represent `False`.The `args` argument to the function definition will hold such attributes that are passed by user. 
    
    Now, it's worth mentioning here that a stream can contain multiple invocation of `boolean` function. but all the invocations will be sent to function definition
    in one call. So we need to make sure for each invocation we generate a separate set of data and add that as a column to the passed dataframe.
    
    Keep this thing in mind our function definition will change to something this!
    
    ```python
    def boolean(data_frame, number, args=None):
    """
    Generator function for boolean values
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    dcols = [f for f in data_frame.columns if f.startswith("boolean")]
    for column_name, data_frame_col_name in zip(args, dcols):
      #TODO Generate separate data for each boolean invocation
      pass
    ```
    
    First we filter all the columns that are tagged to contain `boolean` values. Then we iterate over all the boolean columns of the dataframe and 
    populate each column with the generated data.
    
3. Last step, is to generate the data as a list and add the generated data to dataframe as a column.

    ```python
    def boolean(data_frame, number, args=None):
    """
    Generator function for boolean values
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    dcols = [f for f in data_frame.columns if f.startswith("boolean")]
    for column_name, data_frame_col_name in zip(args, dcols):
        if args is not None:
            value = args.get(column_name).get('set_val', '1,0')
            value = value if isinstance(value, str) else '1,0'
            boolean_values = value.split(',')[:2]
        else:
            boolean_values = ['1', '0']

        boolean_weights = [0.5, 0.5]
        boolean_list = random.choices(population=boolean_values, weights=boolean_weights, k=number)
        data_frame[data_frame_col_name] = boolean_list
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)
    ```
    
    The third last line in above snippet defines a variable `boolean_list` of type list with size equal to `number` argument which holds the generated data.
    The second last line assignes the same generated list as a column to the dataframe passed as argument to the function.






















