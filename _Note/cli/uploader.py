""r"""

https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html


https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
Presigned URLs
A user who does not have AWS credentials or permission to access an S3 object can be granted temporary access by using a presigned URL.

"""

import logging
import boto3
from botocore.exceptions import ClientError


# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


# upload_file('test.txt', 'capstones3bucket')
# upload_file('test.txt', 'tehyulekimbucket1')