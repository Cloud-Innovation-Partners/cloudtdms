#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

from pandas_profiling.profile_report import ProfileReport
from pandas_profiling.report.presentation.core.renderable import Renderable
from pandas_profiling.config import Config
from pandas_profiling.version import __version__
import random
import json

from tqdm import tqdm
from typing import List, Optional
import warnings
from system.cloudtdms.discovery import discover
from datetime import datetime
from pandas_profiling.report.presentation.core.root import Root
from pandas_profiling.report.presentation.core import (
    HTML,
    Container,
    Table,
)
from pandas_profiling.report.presentation.flavours.html.html import HTMLHTML
config = Config()

import pandas as pd


def get_dataset_personal_identifiable_information(summary: dict, metadata: dict):
    pii = summary['pii']
    rows = []
    # {'person_name': [{'surname': 50.0}], 'person_detail': [{'age': 50.0}, {'gender': 50.0}, {'rownumber': 100.0}]}
    for key, value in pii.items():
        for item in value:
            (i, k) = next(enumerate(item))
            rows.append(
                {
                    "name": f'<a class="anchor" href="#pp_var_{hash(k)}"><code>{k}</code></a> <span style="font-weight:normal">is classified as <strong>{item["match"]}</strong> with score of <code>{item[k]}%</code> on <code>{item["basis"]}</code> basis </span> ',
                    "value": f'<span class ="label label-primary"> {key} </span>',
                    "fmt": "raw",
                }
            )
    pii_table = Table(
        rows,
        name="Sensitive Variables",
        anchor_id="metadata_reproduction",
    )

    return Container(
        [pii_table], name="Overview", anchor_id="pii", sequence_type="grid",
    )


def generate_script(filename, pii):
    pii=dict(pii) # pii is string, convert it into dict and make list of dict below
    results = []
    for key in pii:
        result = pii[key]
        results.extend(result)

    STREAM = {'number': 1000, "title": 'Stream6', "source": filename, "format": "csv", "frequency": "once"}

    enc_type = {'high': 'mask_out', 'mid': 'ceasar', 'low': 'substitute'}

    subtitute_mapping_values = {
        'FirstName': {'type': 'personal.first_name'},
        'LastName': {'type': 'personal.last_name'},
        'Name': {'type': 'personal.full_name'},
        'Gender': {'type': 'personal.gender'},
        'Email': {'type': 'personal.email_address'},
        'City': {'type': 'location.city'},
        'Latitude': {'type': 'location.latitude'},
        'Longitude': {'type': 'location.longtitude'},
        'Phone': {'type': 'location.phone'},
        'State': {'type': 'location.state'},
        'Municipality': {'type': 'location.municipality'},
        'Postal_code': {'type': 'location.postal_code'},
        'Country': {'type': 'location.country'},
        'Dob': {"type": "date.dates", "format": "mm-dd-YYYY", "start": "12-07-2020", "end": "12-08-2023"},
        'Age': {'type': "basics.random_number", "start": 18, "end": 80},
        'Guid': {"type": "basics.guid"},
    }

    with_ = ['*', '$', '@', '!', '^']
    from_ = ['start', 'mid', 'end']
    high_sensi_cols = []
    mid_sensi_cols = []
    low_sensi_cols = []
    substitute_dict = {}
    delete_subs_cols = []
    updated_result = []
    sensiH=sensiM=''

    # substitute
    for result in results:
        match = result['match']
        match = match.title()
        if match in subtitute_mapping_values:
            substitute_dict[match] = subtitute_mapping_values[match]
            delete_subs_cols.append(match.lower())
        else:
            updated_result.append(result)

    STREAM['substitute'] = substitute_dict

    for result in updated_result:
        if result['sensitvity'] == 'high':
            high_sensi_cols.append(result['match'])
            typeH = enc_type['high']
            sensiH = result['sensitvity']
        if result['sensitvity'] == 'mid':
            mid_sensi_cols.append(result['match'])
            typeM = enc_type['mid']
            sensiM = result['sensitvity']
        if result['sensitvity'] == 'low':
            low_sensi_cols.append(result['match'])
            typeL = enc_type['low']
            sensiL = result['sensitvity']

    if sensiH == 'high':
        STREAM['mask_out'] = {k: {"with": with_[random.randint(0, len(with_) - 1)], "characters": 6,
                                  "from": from_[random.randint(0, len(from_) - 1)]} for k in high_sensi_cols}

    if sensiM == 'mid':
        STREAM['encrypt'] = {
            "columns": mid_sensi_cols,
            "type": typeM,
            "encryption_key": random.randint(10, 99)
        }

    return STREAM


def get_dataset_proposed_masking_script(summary: dict, metadata: dict):
    pii=summary['pii']
    filename=summary['file_name']
    STREAM=generate_script(filename,pii)
    STREAM = json.dumps(STREAM, indent=3)
    script = HTMLHTML(name="Synthetic Data Configuration", content=f"""
    
    <div style="margin:10px">
    <pre>
    <code>
    STREAM = {
                STREAM
             }
                </code>
                </pre>
                </div>
    """)

    return Container(
        [script], name="Configuration", anchor_id="script", sequence_type="sections",
    )


def get_dataset_items(summary: dict, warnings: list) -> list:
    """Returns the dataset overview (at the top of the report)

    Args:
        summary: the calculated summary
        warnings: the warnings

    Returns:
        A list with components for the dataset overview (overview, reproduction, warnings)
    """
    metadata = {
        key: config["dataset"][key].get(str) for key in config["dataset"].keys()
    }

    items = [
        get_dataset_personal_identifiable_information(summary, metadata),
    ]

    return items


def render_configuration(summary: dict, warnings: list) -> list:
    metadata = {
        key: config["dataset"][key].get(str) for key in config["dataset"].keys()
    }

    items = [
        get_dataset_proposed_masking_script(summary, metadata),
    ]

    return items


def get_report_structure(summary: dict) -> Renderable:
    """Generate a HTML report from summary statistics and a given sample.

    Args:
      sample: A dict containing the samples to print.
      summary: Statistics to use for the overview, variables, correlations and missing values.

    Returns:
      The profile report in HTML format
    """
    disable_progress_bar = not config["progress_bar"].get(bool)
    with tqdm(
            total=1, desc="Generate report structure", disable=disable_progress_bar
    ) as pbar:

        section_items: List[Renderable] = [
            Container(
                get_dataset_items(summary, warnings=[]),
                sequence_type="list",
                name="Personally Identifiable Information (PII)",
                anchor_id="personal_identifiable_information",
            ),
            Container(
                render_configuration(summary, warnings=[]),
                sequence_type="list",
                name="",
                anchor_id="configuration",
            )
        ]

        sections = Container(section_items, name="Root", sequence_type="sections")
        pbar.update()

    footer = HTML(
        content='Report generated with <a href="https://github.com/Cloud-Innovation-Partners/cloudtdms">cloudtdms</a>.'
    )

    return Root("Root", sections, footer)


def describe_df(title: str, df: pd.DataFrame, sample: Optional[dict] = None) -> dict:
    """Calculate the statistics for each series in this DataFrame.

    Args:
        title: report title
        df: DataFrame.
        sample: optional, dict with custom sample

    Returns:
        This function returns a dictionary containing:
            - table: overall statistics.
            - variables: descriptions per series.
            - correlations: correlation matrices.
            - missing: missing value diagrams.
            - messages: direct special attention to these patterns in your data.
            - package: package details.
    """

    if df is None:
        raise ValueError("Can not describe a `lazy` ProfileReport without a DataFrame.")

    if not isinstance(df, pd.DataFrame):
        warnings.warn("df is not of type pandas.DataFrame")

    if df.empty:
        raise ValueError("df can not be empty")

    date_start = datetime.utcnow()

    with tqdm(
            total=1, desc="Identifying PII's", disable=False
    ) as pbar:
        pii = discover(df)
        pbar.update()

    date_end = datetime.utcnow()

    package = {
        "pandas_profiling_version": __version__,
        "pandas_profiling_config": config.dump(),
    }

    analysis = {
        "title": title,
        "date_start": date_start,
        "date_end": date_end,
        "duration": date_end - date_start,
    }

    # Start PII discovery

    return {
        #Analysis
        "analysis" : analysis,
        #Package
        "package": package,
        # PII
        "pii" : pii
    }


class PIIReport(ProfileReport):
    def __init__(self, df,filename=None, **kwargs):
        super().__init__(df)
        self._file_name=filename

    @property
    def report(self):
        if self._report is None:
            self._report = get_report_structure(self.description_set)
        return self._report

    @property
    def description_set(self):
        if self._description_set is None:
            self._description_set = describe_df(self.title, self.df, self._sample)
            self._description_set['file_name']=self._file_name
        return self._description_set