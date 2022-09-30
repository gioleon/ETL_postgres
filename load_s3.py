import boto3
from decouple import config


def load_data() -> None:
    """
    Takes the given DataFrame and loads it to S3 bucket

    @input: pandas.DataFrame
    """
    client = boto3.client(
        's3', aws_access_key_id=config('ACCESS_KEY_ID'),
        aws_secret_access_key=config('SECRET_ACCESS_KEY'),
        region_name=config('REGION')
    )

    client.upload_file(
        r'data/staging/cleaned_talks_info.csv',
        config('BUCKET_NAME'),
        r'staging/cleaned_talks_info.csv'
    )
