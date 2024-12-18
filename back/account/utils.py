import boto3
from botocore.exceptions import NoCredentialsError
from datetime import timedelta
from django.conf import settings

def generate_presigned_url(key):
    print("turning", key)
    try:
        s3_client = boto3.client('s3')
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME  
        object_key = str(key)  
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=300  
        )
        print("generated", url)
        return url
    except NoCredentialsError:
        print("no client s3")
        return None  