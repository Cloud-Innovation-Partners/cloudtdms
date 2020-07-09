#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

STREAM = {
    "number": 1000,
    "title": 'Stream2',
    "schema": [
        {"field_name": "fname", "type": "person.first_name"},
        {"field_name": "lname", "type": "person.last_name"},
    ],
    "format": "csv",
    "frequency": "once"
}