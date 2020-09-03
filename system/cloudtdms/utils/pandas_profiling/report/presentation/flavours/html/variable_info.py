from system.cloudtdms.utils.pandas_profiling.report.presentation.core import VariableInfo
from system.cloudtdms.utils.pandas_profiling.report.presentation.flavours.html import templates


class HTMLVariableInfo(VariableInfo):
    def render(self):
        return templates.template("variable_info.html").render(**self.content)
