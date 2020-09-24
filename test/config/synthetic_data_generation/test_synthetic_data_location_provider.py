STREAM = {
    "number": 1000,
    "title": 'test_synthetic_data_location_provider',
    "schema": [
    	# Location
    	{"field_name":  "country", "type" :  "location.country"},
    	{"field_name":  "city", "type" :  "location.city"},
    	{"field_name":  "lat", "type" :  "location.latitude"},
    	{"field_name":  "long", "type" :  "location.longitude"},
    	{"field_name" :  "mobile", "type" :  "location.phone_number", "format" :  "###-###-####"},
    	{"field_name" :  "state", "type" :  "location.state"},
    	{"field_name" :  "code", "type" :  "location.country_code", "category" :  "numeric"},
    	{"field_name" :  "p_code", "type" :  "location.postal_code"},
    	{"field_name" :  "address", "type" :  "location.address"},
    	{"field_name" :  "tz", "type" :  "location.timezone"},
    	{"field_name" :  "airport", "type" :  "location.airport"},
    	{"field_name" :  "municipality", "type" :  "location.municipality"}
        
    ],
    "format": "csv",
    "frequency": "once"
}
