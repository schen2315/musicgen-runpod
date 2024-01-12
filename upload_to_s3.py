import boto3
from botocore.exceptions import ClientError
import os

ACCESS_KEY_ID = os.environ['ACCESS_KEY_ID']
SECRET_ACCESS_KEY_ID = os.environ['SECRET_ACCESS_KEY_ID']

def upload_file(filename, bucket, region, object_name):
    if object_name is None:
        object_name = os.path.basename(filename)

    s3_client = boto3.client('s3',
                             aws_access_key_id=ACCESS_KEY_ID,
                             aws_secret_access_key=SECRET_ACCESS_KEY_ID,
                             region_name=region)
    try:
        resp = s3_client.upload_file(filename, bucket, object_name)
    except ClientError as e:
        print(e)

# upload files
def upload_files(files, bucket, region):
    try:
        for file in files:
            upload_file(file, bucket, region, f"audio/{file}")
            print(f"uploaded to s3://{bucket}/audio/{file}")
    except ClientError as e:
        print(e)

if __name__ == "__main__":
    bucket = 'riff8-audio'
    filename = './outputs/heavy_metal-1.wav'
    object_name = 'test/heavy_metal-1.wav'
    upload_file(filename, bucket, object_name)
