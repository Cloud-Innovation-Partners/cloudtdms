STREAM = {
    "number": 1000,
    "title": 'test_synthetic_data_masking_provider',
    "schema": [
    	# Advanced-DataMasking
    	{"field_name" :  "Surname", "type" :  "advanced.custom_file", "name" :  "Churn-Modeling", "column" :  "Surname", "ignore_headers" :  "no", "encrypt": {"type": "caesar","key" : 9797 }},
    	{"field_name" :  "CustomerId", "type" :  "advanced.custom_file", "name" :  "Churn-Modeling", "column" :  "CustomerId", "ignore_headers" :  "no", "mask_out" : {"with" : "*", "characters" : 5, "from" : "start"}},
    	{"field_name" :  "RowNumber", "type" :  "advanced.custom_file", "name" :  "Churn-Modeling", "column" :  "RowNumber", "ignore_headers" :  "no", "shuffle": True},
    	{"field_name" :  "NumOfProducts", "type" :  "advanced.custom_file", "name" :  "Churn-Modeling", "column" :  "NumOfProducts", "ignore_headers" :  "no", "set_null": True}
    	
    ],
    "format": "csv",
    "frequency": "once"
}
