#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import xml.etree.ElementTree as ET
import pandas as pd

# The below Parser class will be used in profiliing of XML files
class Parser():
    """
    This class is actually responsible for parsing the xml data with the help of generators
    in a minimal possible time,  and creates an object for each parsed data
    """

    def __init__(self, file_path):
        print(f"FILEPATH : {file_path}")
        self.file_path = file_path
        xml_data = open(self.file_path, 'r').read()  # Read file
        self.root = ET.XML(xml_data)  # Parse XML

    def get_column_labels(self):
        # get cols names only
        for i, child in enumerate(self.root):
            if i > 0:  # executes only one time, because we need only column names
                break
            cols = [subchild.tag for subchild in child]
        return cols

    def get_data(self):
        count = 0
        for i, child in enumerate(self.root):
            # if count == limit:
            #     break
            yield [subchild.text for subchild in child]
            # count += 1





