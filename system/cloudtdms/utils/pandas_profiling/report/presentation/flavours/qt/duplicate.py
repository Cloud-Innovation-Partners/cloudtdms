from PyQt5.QtWidgets import QPushButton

from system.cloudtdms.utils.pandas_profiling.report.presentation.core import Duplicate


class QtDuplicate(Duplicate):
    def render(self):
        return QPushButton(self.content["name"])
