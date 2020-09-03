from system.cloudtdms.utils.pandas_profiling.report.presentation.core import Image
from system.cloudtdms.utils.pandas_profiling.report.presentation.flavours.html import templates


class HTMLImage(Image):
    def render(self):
        return templates.template("diagram.html").render(**self.content)
