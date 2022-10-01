import os
import boto3
from decouple import config


def get_file() -> None:
    """
    Downloads the csv file from S3 bucket.
    """

    if not os.path.exists("data"):
        os.makedirs('data/preprocess')

    # Connect to S3 bucket
    client = boto3.client(
        's3', aws_access_key_id=config('ACCESS_KEY_ID'),
        aws_secret_access_key=config('SECRET_ACCESS_KEY'),
        region_name=config('REGION')
    )

    if not os.path.exists("./data/preprocess/talks_info.csv"):
        # Download file
        client.download_file(
            config('BUCKET_NAME'),
            r'preprocess/talks_info.csv',
            r'./data/preprocess/talks_info.csv')