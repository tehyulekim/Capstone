import boto3

BUCKET_NAME = "capstones3bucket"
OBJECT_NAME = "capstones3bucket.txt"
FILE_NAME = "capstones3bucket.txt"

# OBJECT_NAME, FILE_NAME = "f1"

s3 = boto3.client('s3')
s3.download_file(BUCKET_NAME, OBJECT_NAME, FILE_NAME)
