from flask import request
import boto3, botocore
import os

s3 = boto3.client(
    "s3",
    aws_access_key_id = os.environ.get('S3_KEY'),
    aws_secret_access_key = os.environ.get('S3_SECRET_ACCESS_KEY')
)

def upload(folder_path):
    file = request.files.get('user_file')
    s3.upload_fileobj(
        file,
        "nextagram-qwerty-flask",
        f'{folder_path}/' + file.filename,
        ExtraArgs={
            "ACL": 'public-read',
            "ContentType" : file.content_type
        }
    )