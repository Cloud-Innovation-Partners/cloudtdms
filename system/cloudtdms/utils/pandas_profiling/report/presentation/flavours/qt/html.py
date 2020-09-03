from PyQt5.QtWidgets import QPushButton

from system.cloudtdms.utils.pandas_profiling.report.presentation.core import HTML


class QtHTML(HTML):
    def render(self):
        return QPushButton(self.content["html"])
