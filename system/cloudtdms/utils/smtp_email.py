#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import os
import yaml
import smtplib, ssl, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from system.dags import get_config_default_path


class SMTPEmail():
    def __init__(self):
        self.body = None
        self.message = MIMEMultipart()
        self.reports_path = None
        self.report_files = None

    @property
    def username(self):
        return SMTPEmail.get_email_config_default().get('username')

    @property
    def password(self):
        return SMTPEmail.get_email_config_default().get('password')

    @property
    def subject(self):
        return SMTPEmail.get_email_config_default().get('subject')

    @property
    def to(self):
        return SMTPEmail.get_email_config_default().get('to')

    @property
    def from_email(self):
        return SMTPEmail.get_email_config_default().get('from')

    @property
    def body(self):
        if self._body is not None:
            return self._body
        else:
            template =Template(open(f"{os.path.dirname(__file__)}/email.html").read())
            return template.render(
                data=self.report_files
            )


    @property
    def message(self):
        return self._message

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def reports_path(self):
        return self._reports_path

    @property
    def report_files(self):
        return self._report_files

    @report_files.setter
    def report_files(self, value):
        self._report_files = value

    @reports_path.setter
    def reports_path(self, value):
        self._reports_path = value

    @message.setter
    def message(self, value):
        self._message = value

    @staticmethod
    def get_email_config_default():
        config = yaml.load(open(get_config_default_path()), Loader=yaml.FullLoader)
        if config is not None and config.get('email', None) is not None:
            return config.get('email')
        else:
            raise KeyError('config_default.yaml has no email entry')

    @staticmethod
    def availability():
        try:
            email = SMTPEmail.get_email_config_default()
            if email.get('to') == "" or email.get('username') == "" or email.get('password') == "":
                return False
        except KeyError:
            return False
        return True

    def add_attachments(self, directory_path: str, file_format='.html'):
        # Create a multipart message and set headers
        message = self.message
        message["From"] = self.from_email
        message["To"] = self.to
        message["Subject"] = self.subject

        # Add body to email
        self.reports_path = directory_path
        self.report_files = [f for f in os.listdir(directory_path) if str(f).startswith('pii_') or
                     str(f).startswith('profiling_') or str(f).startswith('script_')]

        message.attach(MIMEText(self.body, "html"))

        for file in [f for f in os.listdir(directory_path) if str(f).startswith('pii_') or
                     str(f).startswith('profiling_') or str(f).startswith('script_')]:
            with open(f"{directory_path}/{file}", "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {file}",
            )

            # Add attachment to message and convert message to string
            message.attach(part)

    def send_email(self):
        text = self.message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTPEmail.get_email_config_default().get('smtp_host'),
                              SMTPEmail.get_email_config_default().get('smtp_port'), context=context) as server:
            server.login(self.username, self.password)
            server.sendmail(self.username, self.to, text)
