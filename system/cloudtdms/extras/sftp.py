import base64

import paramiko, socket
from datetime import datetime, timedelta
from system.dags import get_config_default_path, get_output_data_home, get_user_data_home
import yaml
from airflow.utils.log.logging_mixin import LoggingMixin
import os
import pandas as pd

FIVE_MB = 5244880  # 5 MB = 5244880 BYTES


def get_sftp_config_default():
    """
    This method fetches the configuration details of SFTP
    :return:
    """
    config = yaml.load(open(get_config_default_path()), Loader=yaml.FullLoader)
    if config is not None and config.get('sftp', None) is not None:
        return config.get('sftp')
    else:
        raise KeyError('config_default.yaml has no postgres entry')


def decode_(field):
    """
    This method decodes the encoded fields
    :param field:
    :return:
    """
    base64_bytes = field.encode("UTF-8")
    field_bytes = base64.b64decode(base64_bytes)
    decoded_field = field_bytes.decode("UTF-8")
    return decoded_field


def sftp_upload(**kwargs):
    """
    This method Uploads the file to the SFTP server
    :param kwargs:
    :return:
    """

    connection_name = kwargs.get('connection')
    prefix = kwargs.get('prefix')
    execution_date = kwargs.get('execution_date')
    sftp_file_path = kwargs.get('file_path')
    is_overwrite = kwargs.get('overwrite') if kwargs.get('overwrite') else False
    is_overwrite = True if str(is_overwrite).lower() == 'true' else False

    if is_overwrite:
        sftp_file_path = sftp_file_path  # set the same path
    else:
        directory = os.path.dirname(sftp_file_path)
        timestamp = str(execution_date)[:19].replace('-', '_').replace(':', '_')
        filename, extension = os.path.basename(sftp_file_path).split('.')
        updated_file_name = f"{filename}_{timestamp}.{extension}"  # append timestamp to the filename
        sftp_file_path = f"{directory}/{updated_file_name}"
        LoggingMixin().log.info(f"Updated file path {sftp_file_path}")

    file_name = f"{os.path.basename(prefix)}_{str(execution_date)[:19].replace('-', '_').replace(':', '_')}.csv"

    connection_in_yaml = get_sftp_config_default()
    # folder = connection_in_yaml.get(connection).get('folder')

    # read latest modified csv file
    latest_file_path = get_output_data_home() + '/' + kwargs['prefix'] + '/' + file_name
    LoggingMixin().log.info(f" LATEST FILE PATH : {latest_file_path}")
    csv_file = pd.read_csv(latest_file_path)

    is_available = True if connection_name in connection_in_yaml else False

    if is_available:
        user = decode_(connection_in_yaml.get(connection_name).get('username')).replace('\n', '')
        password = decode_(connection_in_yaml.get(connection_name).get('password')).replace('\n', '')
        host = connection_in_yaml.get(connection_name).get('host').replace(' ', '')
        port = int(connection_in_yaml.get(connection_name).get('port')) if connection_in_yaml.get(connection_name).get(
            'port') else 22
        ssh_public_key = connection_in_yaml.get(connection_name).get('ssh_public_key')
        # passphrase = connection_in_yaml.get(connection_name).get('passphrase') if connection_in_yaml.get(connection_name).get(
        #     'passphrase') else " "
        # passphrase = decode_(passphrase).replace('\n', '')

        passphrase = connection_in_yaml.get(connection_name).get('passphrase')
        passphrase = None if len(passphrase.strip()) == 0 or passphrase is None else decode_(passphrase)

        LoggingMixin().log.info(f'Inserting data in {file_name}, {sftp_file_path}')

        if len(password.strip()) != 0:  # means password is present
            storage = Storage(
                user=user,
                password=password,
                host=host,
                connection_name=connection_name,
                sftp_file_path=sftp_file_path,
                port=port,
                local_file_path=latest_file_path
            )

            storage.upload()
        else:
            # use SSH KEY
            storage = Storage(
                user=user,
                password=password,
                host=host,
                connection_name=connection_name,
                sftp_file_path=sftp_file_path,
                port=port,
                local_file_path=latest_file_path,
                ssh_key=ssh_public_key,
                passphrase=passphrase
            )

            storage.ssh_upload()

    else:
        raise AttributeError(f"{connection_name} not found in config_default.yaml")


def sftp_download(**kwargs):
    """
    This method Downloads the file from the SFTP server
    :param kwargs:
    :return:
    """
    connection_name = kwargs.get('connection')
    dwn_sftp_file = kwargs.get('file_path')
    execution_date = kwargs.get('execution_date')
    prefix = kwargs.get('prefix')

    connection_in_yaml = get_sftp_config_default()
    # folder = connection_in_yaml.get(connection).get('folder')

    file_name = f"sftp_{connection_name}_{os.path.dirname(prefix)}_{os.path.basename(prefix)}_{str(execution_date)[:19].replace('-', '_').replace(':', '_')}.csv"

    user = decode_(connection_in_yaml.get(connection_name).get('username')).replace('\n', '')
    password = decode_(connection_in_yaml.get(connection_name).get('password')).replace('\n', '')
    host = connection_in_yaml.get(connection_name).get('host') if connection_in_yaml.get(connection_name).get(
        'host') else None
    port = int(connection_in_yaml.get(connection_name).get('port')) if connection_in_yaml.get(connection_name).get(
        'port') else 22

    ssh_public_key = connection_in_yaml.get(connection_name).get('ssh_public_key')

    # passphrase = connection_in_yaml.get(connection_name).get('passphrase') if connection_in_yaml.get(connection_name).get(
    #     'passphrase') else " "
    # passphrase = decode_(passphrase)

    passphrase = connection_in_yaml.get(connection_name).get('passphrase')
    passphrase = None if len(passphrase.strip()) == 0 or passphrase is None else decode_(passphrase)

    if host is not None:
        if len(password.strip()) != 0:  # means password is present
            storage = Storage(
                user=user,
                password=password,
                host=host,
                connection_name=connection_name,
                sftp_file_path=dwn_sftp_file,
                port=port,
                local_file_path=f'{get_user_data_home()}/.__temp__/{file_name}',
            )

            storage.download()
        else:
            # use SSH KEY
            storage = Storage(
                user=user,
                password=password,
                host=host,
                connection_name=connection_name,
                sftp_file_path=dwn_sftp_file,
                port=port,
                local_file_path=f'{get_user_data_home()}/.__temp__/{file_name}',
                ssh_key=ssh_public_key,
                passphrase=passphrase
            )

            storage.ssh_download()


class Storage:
    """
     This class is responsible for uploading a file or downloading a file.
     Uploading: Simple Upload, with Username and Password
                SSH_Upload, with ssh public key

     Downloading: Simple Download, with Username and Password
                  SSH Download, with ssh public key
    """

    def __init__(self, user, password, host, connection_name,
                 sftp_file_path, port, local_file_path, ssh_key=None, passphrase=None):
        self.user = user
        self.password = password
        self.host = host
        self.connection_name = connection_name
        self.sftp_file_path = sftp_file_path
        self.port = port
        self.local_file_path = local_file_path
        self.ssh_key = ssh_key
        self.passphrase = passphrase

    def upload(self):
        """
        upload method uploads the file with username and password
        :return:
        """
        r_file_path = self.sftp_file_path
        r_file = os.path.basename(r_file_path)

        LoggingMixin().log.info(f"LOCAL FILE PATH: {self.local_file_path}")
        LoggingMixin().log.info(f"REMOTE FILE PATH: {r_file_path}")

        # Open a transport
        transport = paramiko.Transport((self.host, self.port))

        # Auth
        transport.connect(None, self.user, self.password)

        # Go!
        sftp = paramiko.SFTPClient.from_transport(transport)

        for dir in r_file_path.split('/')[:-1]:
            try:
                sftp.listdir(dir)
                sftp.chdir(dir)
            except IOError as e:
                sftp.mkdir(dir)
                sftp.chdir(dir)

        sftp.put(self.local_file_path, r_file)

        # Close
        if sftp:
            sftp.close()
        if transport:
            transport.close()

    def ssh_upload(self):
        """
        ssh_upload method file uploads the file using ssh public key
        :return:
        """
        r_file_path = self.sftp_file_path
        r_file = os.path.basename(r_file_path)

        LoggingMixin().log.info(f"SSH_UPLOAD-LOCAL FILE PATH: {self.local_file_path}")
        LoggingMixin().log.info(f"SSH_UPLOAD- REMOTE FILE PATH: {r_file_path}")

        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname=self.host,
                  port=self.port,
                  username=self.user,
                  password='',
                  key_filename=self.ssh_key,
                  passphrase=self.passphrase
                  )

        sftp = s.open_sftp()
        for dir in r_file_path.split('/')[:-1]:
            try:
                sftp.listdir(dir)
                sftp.chdir(dir)
            except IOError as e:
                sftp.mkdir(dir)
                sftp.chdir(dir)

        sftp.put(self.local_file_path, r_file)

        # Close
        if sftp:
            sftp.close()

    def download(self):
        """
        download method downloads the file using username and password
        :return:
        """
        r_file_path = self.sftp_file_path
        r_file = os.path.basename(r_file_path).split('.')[0]

        LoggingMixin().log.info(f"Downloaded FILE PATH: {self.local_file_path}")
        LoggingMixin().log.info(f"REMOTE FILE PATH: {r_file_path}")

        # Open a transport
        transport = paramiko.Transport((self.host, self.port))

        # Auth
        transport.connect(None, self.user, self.password)

        # Go!
        sftp = paramiko.SFTPClient.from_transport(transport)

        CheckSum.download(self.connection_name, self.local_file_path, r_file_path, r_file, sftp)

        # Close
        if sftp:
            sftp.close()
        if transport:
            transport.close()

    def ssh_download(self):
        """
        ssh_method downlods the file using ssh public key
        :return:
        """
        r_file_path = self.sftp_file_path
        r_file = os.path.basename(r_file_path).split('.')[0]

        LoggingMixin().log.info(f"SSH_DOWNLOAD-LOCAL FILE PATH: {self.local_file_path}")
        LoggingMixin().log.info(f"SSH_DOWNLOAD- REMOTE FILE PATH: {r_file_path}")

        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname=self.host,
                  port=self.port,
                  username=self.user,
                  password='',
                  key_filename=self.ssh_key,
                  passphrase=self.passphrase
                  )

        sftp = s.open_sftp()
        CheckSum.download(self.connection_name, self.local_file_path, r_file_path, r_file, sftp)
        # Close
        if sftp:
            sftp.close()


class CheckSum:
    """
    This class checks the conditions before downloading a file, i.e is file CSV or JSON,
    is file size less than 5MB e.t.c

    """

    @staticmethod
    def download(connection_name, local_file_path, r_file_path, r_file, sftp):
        """
        This method checks the conditions before downloading a file, i.e is file CSV or JSON,
        is file size less than 5MB e.t.c
        :param connection_name:
        :param local_file_path:
        :param r_file_path:
        :param r_file:
        :param sftp:
        :return:
        """

        # 1. read only csv and json files
        if str(r_file_path).endswith(".csv") or str(r_file_path).endswith(".json"):
            LoggingMixin().log.info("File extension CSV or JSON ")
            info = sftp.lstat(r_file_path)
            file_size = info.st_size  # return size in bytes

            # 2. validate file size, limit 5MB, More than 5 MB don't download - raise exception
            if file_size <= FIVE_MB:
                LoggingMixin().log.info(f"File size {file_size} bytes <= {FIVE_MB} bytes (5MB)")
                sftp.get(remotepath=r_file_path, localpath=local_file_path)
            else:
                raise SystemError(f'File {os.path.basename(r_file_path)} exceeds 5MB file size limit')

            # 3. load only 5000 records in df
            df = pd.read_csv(local_file_path, nrows=5000)
            # 4. add prefix -- sftp.prod.filename(without extension)
            df.columns = [f"sftp.{connection_name}.{r_file}.{f}" for f in df.columns]
            # 5. overwrite the file with updated 5000 records
            df.to_csv(f'{get_user_data_home()}/.__temp__/{os.path.basename(local_file_path)}', index=False)
        else:
            LoggingMixin().log.info(f"File {os.path.basename(r_file_path)} is not a CSV or JSON file.")
