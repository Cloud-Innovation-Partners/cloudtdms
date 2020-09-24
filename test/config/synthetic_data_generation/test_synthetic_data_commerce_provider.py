STREAM = {
    "number": 1000,
    "title": 'test_synthetic_data_commerce_provider',
    "schema": [
    	# Commerce
    	{"field_name" :  "card", "type" :  "commerce.credit_card"},
    	{"field_name" :  "ctype", "type" :  "commerce.credit_card_type"},
    	{"field_name" :  "money", "type" :  "commerce.currency"},
    	{"field_name" :  "ccode", "type" :  "commerce.currency_code"}    	
    	
    ],
    "format": "csv",
    "frequency": "once"
}
