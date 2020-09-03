"""Main module of pandas-profiling.

.. include:: ../../README.md
"""

from system.cloudtdms.utils.pandas_profiling.config import Config, config
from system.cloudtdms.utils.pandas_profiling.controller import pandas_decorator
from system.cloudtdms.utils.pandas_profiling.profile_report import ProfileReport
from system.cloudtdms.utils.pandas_profiling.version import __version__

clear_config = ProfileReport.clear_config
