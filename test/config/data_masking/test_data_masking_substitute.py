STREAM = {
    "number": 1000,
    "title": 'test_data_masking_substitute',
    "source": 'Churn-Modeling',
    "substitute": {
        "Surname": {"type" : "personal.last_name"},
        "Gender": {"type": "personal.gender"},
        "Geography": {"type" : "location.country"}
    },
    "format": "csv",
    "frequency": "once"
}
