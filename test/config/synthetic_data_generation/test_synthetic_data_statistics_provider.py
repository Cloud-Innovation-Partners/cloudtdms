STREAM = {
    "number": 1000,
    "title": 'test_synthetic_data_statistics_provider',
    "schema": [
    	# Statistics
    	{"field_name" :  "normal", "type" :  "statistics.normal", "center" : 5, "std_dev" : 1, "decimals" : 2},
    	{"field_name" :  "poisson", "type" :  "statistics.poisson", "mean" : 5},
    	{"field_name" :  "binomial", "type" :  "statistics.binomial", "success_rate" : 0.5},
    	{"field_name" :  "exponential", "type" :  "statistics.exponential", "scale" : 4},
    	{"field_name" :  "geometric", "type" :  "statistics.geometric", "success_rate" : 0.4}
    	
    ],
    "format": "csv",
    "frequency": "once"
}
