STREAM = {
    "number": 1000,
    "title": 'test_synthetic_data_it_provider',
    "schema": [
    	# IT
    	{"field_name" :  "ip", "type" :  "it.ip_address", "category" :  "v6"},
    	{"field_name" :  "mac", "type" :  "it.mac_address"},
    	{"field_name" :  "sha1", "type" :  "it.sha1"},
    	{"field_name" :  "sha256", "type" :  "it.sha256"},
    	{"field_name" :  "domain", "type" :  "it.domain_name"}
    ],
    "format": "csv",
    "frequency": "once"
}
