STREAM = {
    "number": 1000,
    "title": 'test_synthetic_data_date_provider',
    "schema": [
    	# Date
    	{"field_name" :  "date", "type" :  "dates.date","format":"mm-dd-YYYY","start":"12-07-2020","end":"12-08-2023"},
    	{"field_name" :  "day", "type" :  "dates.day"},
    	{"field_name" :  "month", "type" :  "dates.month"},
    	{"field_name" :  "time", "type" :  "dates.time"},
    	{"field_name" :  "timestamp", "type" :  "dates.timestamp"}
    ],
    "format": "csv",
    "frequency": "once"
}
