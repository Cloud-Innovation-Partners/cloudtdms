STREAM = {
    "number": 1000,
    "title": 'test_synthetic_data_basics_provider',
    "schema": [
    	# Basics
        {"field_name" : "status", "type" : "basics.boolean", "set_val": "1,0"},
        {"field_name" :  "freq", "type" :  "basics.frequency"},
        {"field_name" : "colour", "type" : "basics.color", "format" :  "hex-code"},
        {"field_name" :  "captcha", "type" :  "basics.words", "atleast" :  "5", "atmost" :  "15"},
        {"field_name" :  "text", "type" :  "basics.sentence", "atleast" :  "5", "atmost" :  "10"},
        {"field_name" :  "empty", "type" :  "basics.blank"},
        {"field_name" :  "uuid", "type" :  "basics.guid"},
        {"field_name" :  "passcode", "type" :  "basics.password", "length" :  12},
        {"field_name" :  "id", "type" :  "basics.auto_increment", "prefix" :  "INC", "suffix" :  "NZD", "start":  2000, "increment" :  5},
        {"field_name" :  "random_id", "type" :  "basics.random_number", "start" :  20, "end" :  200},
        {"field_name" :  "range", "type" :  "basics.number_range", "start" :  20, "end" :  200}
    ],
    "format": "csv",
    "frequency": "once"
}
