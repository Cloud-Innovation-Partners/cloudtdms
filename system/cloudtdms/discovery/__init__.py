#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import system.cloudtdms.discovery.person_name
import system.cloudtdms.discovery.person_detail
import system.cloudtdms.discovery.location
from system.cloudtdms.discovery import networking, phone_number


def pii_scale(match_score_on_column_basis, match_score_on_data_basis):
    """
    Formula For PII_Scale
    :param match_score_on_column_basis:
    :param match_score_on_data_basis:
    :return: (MATCH SCORE ON COLUMN BASIS) + (MATCH SCORE ON DATA BASIS) / 2
    """
    return match_score_on_column_basis + match_score_on_data_basis/2


def discover(data_frame):
    t_data_frame = data_frame.copy()
    return {
        "person_name": person_name.search(t_data_frame, pii_scale),
        "person_detail": person_detail.search(t_data_frame, pii_scale),
        "location_detail": location.search(t_data_frame, pii_scale),
        "network_details": networking.search(t_data_frame, pii_scale),
        "phone_number_details": phone_number.search(t_data_frame, pii_scale)
    }
