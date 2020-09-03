from system.cloudtdms.utils.pandas_profiling.report.presentation.core.table import Table
from system.cloudtdms.utils.pandas_profiling.report.presentation.flavours.html import templates


class HTMLTable(Table):
    def render(self):
        return templates.template("table.html").render(**self.content)
