import boto3
from botocore.exceptions import ClientError
import os

ACCESS_KEY_ID = os.environ.get('ACCESS_KEY_ID', None)
SECRET_ACCESS_KEY_ID = os.environ.get('SECRET_ACCESS_KEY_ID', None)
REGION = 'us-east-1'
# todo : get rid of upload_file
# only use upload_files
def upload_file(filename,
                bucket,
                region=REGION,
                object_name,
                aws_access_key_id=ACCESS_KEY_ID,
                aws_secret_access_key=SECRET_ACCESS_KEY_ID):
    if object_name is None:
        object_name = os.path.basename(filename)

    s3_client = boto3.client('s3',
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key,
                             region_name=region)
    try:
        resp = s3_client.upload_file(filename, bucket, object_name)
    except ClientError as e:
        print(e)

# upload files
def upload_files(files,
                 bucket,
                 region=REGION,
                 aws_access_key_id=ACCESS_KEY_ID,
                 aws_secret_access_key=SECRET_ACCESS_KEY_ID):
    try:
        for file in files:
            filename = os.path.basename(file)
            upload_file(file, bucket, region, f"audio/{filename}", aws_access_key_id, aws_secret_access_key)
            print(f"uploaded to s3://{bucket}/audio/{filename}")
    except ClientError as e:
        print(e)

if __name__ == "__main__":
    bucket = 'riff8-audio'
    filename = './outputs/heavy_metal-1.wav'
    object_name = 'test/heavy_metal-1.wav'
    upload_file(filename, bucket, object_name)
