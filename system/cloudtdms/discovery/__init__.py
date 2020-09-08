#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import system.cloudtdms.discovery.person_name
import system.cloudtdms.discovery.person_detail
import system.cloudtdms.discovery.location
from system.cloudtdms.discovery import networking, phone_number


def discover(data_frame):
    t_data_frame = data_frame.copy()
    return {
        # "person_name": person_name.search(t_data_frame),
        # "person_detail": person_detail.search(t_data_frame),
        # "location_detail": location.search(t_data_frame),
        "network_details":networking.search(t_data_frame),
        "phone_number_details":phone_number.search(t_data_frame)
    }
