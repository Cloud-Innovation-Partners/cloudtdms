STREAM = {
    "number": 1000,
    "title": 'test_synthetic_data_advanced_provider',
    "schema": [
    	# Date
    	{"field_name" :  "date", "type" :  "dates.date","format":"mm-dd-YYYY","start":"12-07-2020","end":"12-08-2023"},
    	{"field_name" :  "day", "type" :  "dates.day"},
    	{"field_name" :  "month", "type" :  "dates.month"},
    	{"field_name" :  "time", "type" :  "dates.time"},
    	{"field_name" :  "timestamp", "type" :  "dates.timestamp"},
    	# Advanced
    	{"field_name" :  "teams", "type" :  "advanced.custom_list", "set_val" :  "HR, Accounts, Development, Field, Transport"},
    	{"field_name" :  "mixed", "type" :  "advanced.concatenate", "template" :  "{date}-{teams}"},
    	{"field_name" :  "custom_column", "type" :  "advanced.custom_file", "name" :  "Churn-Modeling", "column" :  "4", "ignore_headers" :  "yes"}
    ],
    "format": "csv",
    "frequency": "once"
}
