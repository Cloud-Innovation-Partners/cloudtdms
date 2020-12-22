
import os
import base64
import yaml
import boto3
from urllib.parse import urlparse
import pandas as pd
from airflow.utils.log.logging_mixin import LoggingMixin
from system.dags import get_config_default_path, get_output_data_home, get_user_data_home
from airflow.hooks.S3_hook import S3Hook
from botocore.exceptions import ClientError


class CTDMS2AmazonS3:
    def __init__(self, access_key, secret_key, region, prefix, execution_date, uri, format=None, connection=None):
        self.amazon_s3_access_key_id = access_key
        self.amazon_s3_secret_key_id = secret_key
        self._parsed = urlparse(uri, allow_fragments=False)
        self.name = str(self.bucket).upper()
        self.region = region
        self.file_prefix = prefix
        self.data = None
        self.execution_date = execution_date
        self.format = format
        self.connection_name = connection
        self.file_name = f"{os.path.basename(prefix)}_{str(execution_date)[:19].replace('-', '_').replace(':', '_')}.csv" if format is None else f"{os.path.basename(prefix)}_{str(execution_date)[:19].replace('-', '_').replace(':', '_')}.{format}"

    @property
    def bucket(self):
        return self._parsed.netloc

    @property
    def path(self):
        p = self._parsed.path.lstrip('/')
        if p.endswith('.csv') or p.endswith('.json'):
            return os.path.dirname(p)
        else:
            return p

    @property
    def key(self):
        if self._parsed.query:
            return self._parsed.path.lstrip('/') + '?' + self._parsed.query
        else:
            return self._parsed.path.lstrip('/')

    @property
    def url(self):
        return self._parsed.geturl()

    def upload(self):
        """
        This is a convenience function used to upload the data into bucket
        :return:
        """
        synthetic_data_path = f"{get_output_data_home()}/{self.file_prefix}/{self.file_name}"
        if os.path.exists(synthetic_data_path):

            access_key = base64.b64decode(str(self.amazon_s3_access_key_id).encode()).decode('utf-8')
            secret_key = base64.b64decode(str(self.amazon_s3_secret_key_id).encode()).decode('utf-8')
            region = self.region
            bucket = self.bucket

            try:
                s3_hook = S3HookWrapper(
                    aws_secret_key_id=secret_key,
                    aws_access_key_id=access_key
                )

                if s3_hook._check_aws_credentails():
                    if not s3_hook.check_for_bucket(bucket_name=bucket):
                        s3_hook.create_bucket(bucket_name=bucket, region_name=region)

                else:
                    LoggingMixin().log.warning("Authentication Error : invalid s3 credentials")
                s3_hook.load_file(filename=synthetic_data_path, key=f"{self.file_prefix}/{self.file_name}" if self.path == '' else f"{self.path}/{self.file_prefix}/{self.file_name}", bucket_name=bucket, replace=True)

            except (Exception, ClientError) as e:
                if isinstance(e, ClientError) and e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                    return True

                raise

        else:
            LoggingMixin().log.error(f"No Synthetic Data Found @ {synthetic_data_path}!")
            raise FileNotFoundError

    def download(self):
        """
        This is a convenience function used to download the data
        :return:
        """
        access_key = base64.b64decode(str(self.amazon_s3_access_key_id).encode()).decode('utf-8')
        secret_key = base64.b64decode(str(self.amazon_s3_secret_key_id).encode()).decode('utf-8')
        region = self.region
        bucket = self.bucket

        s3_hook = S3HookWrapper(
            aws_secret_key_id=secret_key,
            aws_access_key_id=access_key
        )

        if s3_hook._check_aws_credentails():
            if not s3_hook.check_for_bucket(bucket_name=bucket):
                LoggingMixin().log.error("BucketDoesNotExists")
                exit()
        else:
            LoggingMixin().log.warning("Authentication Error : invalid s3 credentials")

        # TODO Add Dynamic Key and Bucket

        body = s3_hook.read_key(
            key=self.key,
            bucket_name=self.bucket)

        file_name = f"amazons3_{self.connection_name}_{os.path.dirname(self.file_prefix)}_{os.path.basename(self.file_prefix)}_{str(self.execution_date)[:19].replace('-', '_').replace(':', '_')}.csv"
        r_file_name, _ = os.path.splitext(os.path.basename(self._parsed.path))
        with open(f'{get_user_data_home()}/.__temp__/{file_name}', 'w+') as f:
            f.write(body)
            f.seek(0)
            df = pd.read_csv(f)
            df.columns = [f"amazons3.{self.connection_name}.{self.bucket}.{r_file_name}.{f}" for f in df.columns]

        try:
            df.to_csv(f'{get_user_data_home()}/.__temp__/{file_name}', index=False)
        except FileNotFoundError:
            os.makedirs(f'{get_user_data_home()}/.__temp__/')
            df.to_csv(f'{get_user_data_home()}/.__temp__/{file_name}', index=False)

    @staticmethod
    def get_amazon_s3_config_default():
        config = yaml.load(open(get_config_default_path()), Loader=yaml.FullLoader)
        if config is not None and config.get('amazons3', None) is not None:
            return config.get('amazons3')
        else:
            raise KeyError('config_default.yaml has no amazons3 entry')


class S3HookWrapper(S3Hook):

    """
    This class is a Wrapper Class for S3Hook of airflow.hooks.S3_hook
    It is used to pass the acess_key and secret_key directly to the hook
    without registering them into the airflow connection's database table
    """

    def __init__(self,
                 aws_access_key_id=None,
                 aws_secret_key_id=None,
                 aws_session_token=None,
                 endpoint_url = None,
                 *args,**kwargs):

        super().__init__(*args,**kwargs)

        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_key_id = aws_secret_key_id
        self.aws_session_token = aws_session_token
        self.endpoint_url = endpoint_url

    def _get_credentials(self, region_name):
        """
        This method is overriding _get_credentials() method of Aws_hook
        which is the base class for S3Hook
        :param region_name: specify the region name
        :return: returns a boto3.session object with the specified aws_key,aws_secret and token
        """

        return boto3.session.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_key_id,
            aws_session_token=self.aws_session_token,
            region_name=region_name), self.endpoint_url

    def _check_aws_credentails(self):
        client = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_key_id,
        )

        try:
            response = client.list_buckets()

            if 'Buckets' in response:
                return True
            else:
                return False

        except ClientError as e:
            return False


def amazons3_upload(**kwargs):
    execution_date = kwargs.get('execution_date', None)  # dag execution date
    uri = kwargs.get('uri')  # AmazonS3 bucket
    prefix = kwargs.get('prefix')  # title of the synthetic data config file
    connection = kwargs.get('connection')
    format = kwargs.get('format')
    # Load AmazonS3 Details From config_default.yaml
    amazons3_config = CTDMS2AmazonS3.get_amazon_s3_config_default()

    access_key, secret_id, region = None, None, None
    try:
        access_key = amazons3_config.get(connection).get('access_key', None)
        secret_key = amazons3_config.get(connection).get('secret_key', None)
        region = amazons3_config.get(connection).get('region', None)
    except AttributeError:
        LoggingMixin().log.error(f'AmazonS3 credentials not available for {connection} in config_default.yaml',
                                 exc_info=True)
        raise

    if access_key is not None and secret_key is not None and region is not None:
        amazon_s3 = CTDMS2AmazonS3(
            access_key=access_key,
            secret_key=secret_key,
            uri=uri,
            region=region,
            prefix=prefix,
            execution_date=execution_date,
            format=format,
            connection=connection
        )
        amazon_s3.upload()
    else:
        LoggingMixin().log.error(f'Amazon S3 credentials not available for {connection} in config_default.yaml')


def amazons3_download(**kwargs):
    execution_date = kwargs.get('execution_date', None)  # dag execution date
    uri = kwargs.get('uri', None)  # AmazonS3 object URI
    prefix = kwargs.get('prefix')  # title of the synthetic data config file
    connection = kwargs.get('connection')
    format = kwargs.get('format')
    # Load AmazonS3 Details From config_default.yaml
    amazons3_config = CTDMS2AmazonS3.get_amazon_s3_config_default()

    access_key, secret_id, region = None, None, None
    try:
        access_key = amazons3_config.get(connection).get('access_key', None)
        secret_key = amazons3_config.get(connection).get('secret_key', None)
        region = amazons3_config.get(connection).get('region', None)
        uri = uri if uri != '' or uri is not None else None
    except AttributeError:
        LoggingMixin().log.error(f'AmazonS3 credentials not available for {connection} in config_default.yaml',
                                 exc_info=True)
        raise

    if access_key is not None and secret_key is not None and region is not None:
        amazon_s3 = CTDMS2AmazonS3(
            access_key=access_key,
            secret_key=secret_key,
            uri=uri,
            region=region,
            prefix=prefix,
            execution_date=execution_date,
            format=format,
            connection=connection
        )
        amazon_s3.download()
    else:
        LoggingMixin().log.error(f'Amazon S3 credentials not available for {connection} in config_default.yaml')

