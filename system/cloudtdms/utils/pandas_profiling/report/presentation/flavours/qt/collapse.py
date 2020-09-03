from PyQt5.QtWidgets import QPushButton

from system.cloudtdms.utils.pandas_profiling.report.presentation.core import Collapse


class QtCollapse(Collapse):
    def render(self):
        return QPushButton("PyQt5 button")
