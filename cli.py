""r"""

must configure constants:
BUCKET

"""

import os
import logging
from zipfile import ZipFile

import boto3
import fire
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)  # comment out to turn off info messages

BUCKET = 'capstones3bucket'


# compress and upload
def cu(name, version, *files):
    """
    $ python cli.py cu <name> <version> <*files>

    Example: will create z_1.zip containing folder1 and README.md
    $ python cli.py cu z v1 folder1 README.md


    :param name:
    :param version:
    :param files:
    :return: True when success, False when failure
    """
    logging.info("function cu()")

    name_zip = name + "_v" + str(version) + ".zip"

    try:
        # Compress
        compress(name_zip, *files)
        # list_zip(name_zip) # prints list of files inside zip. Comment to turn off

        # ? delete zipped file
    except Exception as e:
        logging.error(e)
        return False

    try:
        # Upload
        upload(name_zip, BUCKET)
    except Exception as e:
        logging.error(e)
        return False

    print(name_zip, "is compressed and uploaded to:", BUCKET)
    return True


# download and extract
def de(name, version, target_dir='./download'):
    """
    $ python cli.py de <name> <version> <target_dir>

    EXAMPLE:  will extract z_1.zip to ./download/folder1
    $ python cli.py de z 1 ./download/folder1


    :param name:
    :param version:
    :param target_dir:
    :return: True if success, False if failure
    """
    logging.info("function de()")

    name_zip = name + "_v" + str(version) + ".zip"

    try:
        # Download
        download(BUCKET, name_zip)

    except Exception as e:
        logging.error(e)
        return False

    try:
        # Extract
        test_zip(name_zip)  # test if downloaded file is valid zip file
        extract(name_zip, target_dir)
    except Exception as e:
        logging.error(e)
        return False

    print(name_zip, "is downloaded from:", BUCKET, "and extracted to:", target_dir)
    return True


# commandline zipfile source code modified from zipfile.py in https://docs.python.org/3/library/zipfile.html
# to write: compress(), extract(), test_zip, list_zip

# Create zipfile from source files.
def compress(zip_name, *files):
    def add_to_zip(zf, path, zippath):
        if os.path.isfile(path):
            zf.write(path, zippath, 8)  # ZIP_DEFLATED = 8
        elif os.path.isdir(path):
            if zippath:
                zf.write(path, zippath)
            for nm in sorted(os.listdir(path)):
                add_to_zip(zf, os.path.join(path, nm), os.path.join(zippath, nm))
        # else: ignore

    with ZipFile(zip_name, 'w') as zf:
        for path in files:
            zippath = os.path.basename(path)
            if not zippath:
                zippath = os.path.basename(os.path.dirname(path))
            if zippath in ('', os.curdir, os.pardir):
                zippath = ''
            add_to_zip(zf, path, zippath)


# Extract zipfile into target directory.
def extract(src, target_dir):
    with ZipFile(src, 'r') as zf:
        zf.extractall(target_dir)


# Test whether the zipfile is valid or not.
def test_zip(src):
    with ZipFile(src, 'r') as zf:
        bad_file = zf.testzip()
    if bad_file:
        print("The following enclosed file is corrupted: {!r}".format(bad_file))
    print(src, "Done testing: zipfile is valid")


# List files in a zipfile.
def list_zip(src):
    with ZipFile(src, 'r') as zf:
        zf.printdir()


# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
def upload(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    EXAMPLE
    upload('test.zip', 'capstones3bucket')

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


# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-download-file.html
# modified to match upload() style
def download(bucket, object_name, file_name=None):
    """Download file from S3 bucket

    EXAMPLE
    download('test.txt', 'capstones3bucket', './download/test.txt')

    :param bucket:
    :param object_name:
    :param file_name:
    :return: True if downloaded, False if failed
    """
    # If S3 file_name was not specified, use object_name
    if file_name is None:
        file_name = object_name

    # Download file
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket, object_name, file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def f1():
    logging.info("function f1")
    return 1


if __name__ == '__main__':
    fire.Fire()
