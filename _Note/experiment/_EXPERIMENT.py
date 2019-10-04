""r"""

use aws cli to login and configure access keys


https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html






# Retrieve the list of existing buckets
import boto3

s3 = boto3.client('s3')
response = s3.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')




"""

