""r"""

https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-download-file.html


https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.download_file

download_file(Bucket, Key, Filename, ExtraArgs=None, Callback=None, Config=None)
Download an S3 object to a file.


import boto3
s3 = boto3.resource('s3')
s3.meta.client.download_file('mybucket', 'hello.txt', '/tmp/hello.txt')


"""

import boto3

BUCKET_NAME = "capstones3bucket"
OBJECT_NAME = "product1/x_v1.zip"  # at S3
FILE_NAME = "product1/x_v1.zip"  # at local file. Must create folder

# OBJECT_NAME, FILE_NAME = "f1"

s3 = boto3.client('s3')
s3.download_file(BUCKET_NAME, OBJECT_NAME, FILE_NAME)
