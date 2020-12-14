#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

from pathlib import Path
from typing import Union
import pandas as pd
import numpy as np
import jinja2
import warnings
from system.dags import get_templates_home


class ProfileReport(object):
    """
    Generate a profile report from a Dataset stored as a pandas `DataFrame`.
    output its content as an HTML report.
    """
    def __init__(self, df=None, title=None, **kwargs):

        self.df = df
        self._title = None
        self._html = None
        self._report = None

    @property
    def title(self):
        if self._title is None:
            self._title = 'CloudTDMS Profiling Report'

        return self._title

    def df_info(self, df: pd.DataFrame):
        """
        Generates Overview stats for the profiling report
        :param df:
        :return:
        """
        number_of_records, number_of_variables = df.shape
        missing_observations = sum(df.isnull().sum())
        number_of_observations = number_of_records * number_of_variables
        memory_usage = df.memory_usage(index=True).sum() / (1024 * 1024)

        return {
                'number_of_variables': f"{number_of_variables:,}",
                'number_of_records': f"{number_of_records:,}",
                'missing_observations': f"{missing_observations:,}",
                'total_missing': f"{round((missing_observations / number_of_observations)*100, 1):,}%",
                'number_of_observations': f"{number_of_observations:,}",
                'memory_usage': f"{round(memory_usage, 2):,} MB"
            }

    def df_dtypes(self, df: pd.DataFrame):
        """
        Generates Variable Types stats for profiling report
        :param df:
        :return:
        """
        dtype_counts = {}

        for df_type in df.convert_dtypes().dtypes:
            if df_type in dtype_counts:
                dtype_counts[df_type] += 1
            else:
                dtype_counts[df_type] = 1

        return dtype_counts

    def df_variables_stats(self, df: pd.DataFrame):
        """
        Generates related stats for each variable in data frame
        :param df:
        :return:
        """
        variable_stats = {}
        total_number_of_records, _ = df.shape
        for column in df.columns:
            variable_stats[column] = {k: f"{round(v,2)}" if type(v) != str else v for k, v in
                                      df[column].describe().items() if k not in ('top', 'freq', '25%', '50%', '75%')}

            variable_stats[column].update({
                'missing_(n)': df[column].isnull().sum(),
                'missing_(%)': f"{round((df[column].isnull().sum() / total_number_of_records)*100,1)}%",
                'max_length': np.vectorize(len)(df[column].values.astype(str)).max(axis=0),
                'min_length': np.vectorize(len)(df[column].values.astype(str)).min(axis=0),
                'd_type': df[column].convert_dtypes().dtype
            })

        return variable_stats

    def df_variable_top_value_counts(self, df: pd.DataFrame):
        """
        Get Top 5 common values of a variable
        :param df:
        :return:
        """
        variable_top_value_counts = {}
        for column in df.columns:
            variable_top_value_counts[column] = {k: f"{v:,}" if type(v) != str else v for k, v in df[column].value_counts().head(5).items()}

        return variable_top_value_counts

    def df_describe(self, df: pd.DataFrame):
        """
        Custom describe function used to generate report stats
        :param df:
        :return:
        """
        df_info = self.df_info(df)
        df_dtypes = self.df_dtypes(df)
        df_variables_stats = self.df_variables_stats(df)
        df_variable_top_value_counts = self.df_variable_top_value_counts(df)
        df_head = df.head(10)
        df_head.reset_index(drop=True, inplace=True)
        df_tail = df.tail(10)
        df_tail.reset_index(drop=True, inplace=True)

        return {
            'info': df_info,
            'types': df_dtypes,
            'variables': df_variables_stats,
            'variable_value_counts': df_variable_top_value_counts,
            'head': df_head,
            'tail': df_tail
        }

    @property
    def html(self):
        if self._html is None:
            self._html = self._render_html()
        return self._html

    @property
    def report(self):
        if self._report is None:
            self._report = self.df_describe(self.df)
        return self._report

    def _render_html(self):
        """
        Render report template with generated stats into HTML
        :return:
        """
        # Load template environment

        loader = jinja2.FileSystemLoader(
            searchpath=get_templates_home())
        env = jinja2.Environment(loader=loader)

        report_template = "report.py.j2"
        template = env.get_template(report_template)

        report = self.report

        html = template.render(
            title=self.title,
            overview=report['info'],
            variable_types=report['types'],
            variables=report['variables'],
            value_counts=report['variable_value_counts'],
            head=report['head'],
            tail=report['tail'],
        )

        return html

    def to_html(self) -> str:
        """Generate and return complete template as lengthy string.

        Returns:
            Profiling report html .

        """
        return self.html

    def to_file(self, output_file: Union[str, Path]):
        """
        Write html report to a file.
        :param output_file:  The name or the path of the file to generate including the extension (.html).
        :return:
        """
        if not isinstance(output_file, Path):
            output_file = Path(str(output_file))

        data = self.to_html()

        if output_file.suffix != ".html":
            suffix = output_file.suffix
            output_file = output_file.with_suffix(".html")
            warnings.warn(
                f"Extension {suffix} not supported. For now we assume .html was intended. "
                f"To remove this warning, please use .html"
            )

        output_file.write_text(data, encoding="utf-8")
