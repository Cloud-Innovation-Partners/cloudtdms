from PyQt5.QtWidgets import QPushButton

from system.cloudtdms.utils.pandas_profiling.report.presentation.core import FrequencyTable


class QtFrequencyTable(FrequencyTable):
    def render(self):
        return QPushButton("Frequency Table")
