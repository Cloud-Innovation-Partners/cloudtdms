STREAM = {
    "number": 1000,
    "title": 'test_synthetic_data_personal_provider',
    "schema": [
    	# Personal
        {"field_name":  "fname", "type" :  "personal.first_name", "category" :  "male"},
        {"field_name":  "lname", "type" :  "personal.last_name"},
        {"field_name":  "name", "type" :  "personal.full_name", "category" :  "female"},
        {"field_name":  "gender", "type" :  "personal.gender", "set_val" :  "M,F"},
        {"field_name" :  "username", "type" :  "personal.username"},
        {"field_name" :  "email", "type" :  "personal.email_address"},
        {"field_name":  "lang", "type" :  "personal.language"},
        {"field_name":  "university_name", "type" :  "personal.university"},
        {"field_name":  "title", "type" :  "personal.title"},
        
    ],
    "format": "csv",
    "frequency": "once"
}
