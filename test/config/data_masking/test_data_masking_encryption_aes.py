STREAM = {
    "number": 1000,
    "title": 'test_data_masking_encryption_aes',
    "source": 'Churn-Modeling',
    "encrypt": {
        "columns": ["EstimatedSalary", "Balance"],
        "type" : "aes",
        "encryption_key": "Jd28hja8HG9wkjw89yd"
    },
    "format": "csv",
    "frequency": "once"
}
