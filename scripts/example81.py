#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

STREAM = {
    "number": 1000,
    "title": 'Stream2',
    "schema": [
        {"field_name": "cardnumber", "type": "commerce.card_number"},
        {"field_name": "cvv", "type": "commerce.cvv"},
        {"field_name": "network", "type": "commerce.network"},
        {"field_name": "expiry_date", "type": "commerce.expiry_date"},
        {"field_name": "currency", "type": "commerce.currency"},
        {"field_name": "currency_code", "type": "commerce.currency_code"},
        {"field_name": "currency_code2", "type": "commerce.currency_code"},
        # {"field_name": "fname", "type": "person.first_name"},
        # {"field_name": "lname", "type": "person.last_name"},
        # {"field_name": "gender", "type": "person.sex"},
        # {"field_name": "country", "type": "geo.country"},
        # {"field_name": "city", "type": "geo.city"},

        # {"field_name": "auto_increment", "type": "basics.auto_increment",'prefix':'INC','suffix':'PR'},
        # {"field_name": "number_range", "type": "basics.number_range",'start':300,'end':400},
        # {"field_name": "uuid", "type": "credentials.UUID"},
        # {"field_name": "password", "type": "credentials.password"},

        # {"field_name": "boolean", "type": "basics.boolean",'set_val':'yes,no'},
        # {"field_name": "frequency", "type": "basics.frequency"},
        # {"field_name": "color", "type": "basics.color",'format':'hex-code'},
        # {"field_name": "country", "type": "location.country"},
        # {"field_name": "city", "type": "location.city"},
        # {"field_name": "latitude", "type": "location.latitude"},
        # {"field_name": "longitude", "type": "location.longitude"},
        # {"field_name": "phone", "type": "location.phone_number",'format':'#-(###)-###-####'},
        # {"field_name": "muncipality", "type": "location.muncipality"},
        # {"field_name": "airport", "type": "location.airport"}

    ],
    "format": "csv",
    "frequency": "once"
}