STREAM = {
    "number": 1000,
    "title": 'test_synthetic_data_company_provider',
    "schema": [
    	# Company
    	{"field_name" :  "cname", "type" :  "company.company_name"},
    	{"field_name" :  "dept", "type" :  "company.department", "category" :  "corporate"},
    	{"field_name":  "duns_id", "type" :  "company.duns_number"},
    	
    	
    ],
    "format": "csv",
    "frequency": "once"
}
