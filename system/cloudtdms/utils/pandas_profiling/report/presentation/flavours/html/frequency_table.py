from system.cloudtdms.utils.pandas_profiling.report.presentation.core import FrequencyTable
from system.cloudtdms.utils.pandas_profiling.report.presentation.flavours.html import templates


class HTMLFrequencyTable(FrequencyTable):
    def render(self):
        return templates.template("frequency_table.html").render(**self.content)
