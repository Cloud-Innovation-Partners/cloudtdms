STREAM = {
    "number": 1000,
    "title": 'test_data_masking_encryption_fernet',
    "source": 'Churn-Modeling',
    "mask_out": {
    "CustomerId": {
    "with": "x",
    "characters": 4,
    "from": "start"
    },
    "Surname" : {
    "with": "#",
    "characters": 4,
    "from": "mid"
    },
    "RowNumber" : {
    "with": "*",
    "characters": 4,
    "from": "end"
    }
    },
    "format": "csv",
    "frequency": "once"
}
