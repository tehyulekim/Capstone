""r"""
Must configure constants:

BUCKET
SERVER_URL
DOWNLOAD_PATH

"""

import os
import logging
import requests
import fire
import boto3
from botocore.exceptions import ClientError
from zipfile import ZipFile
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)  # comment out to turn off info messages

# BUCKET = 'capstones3bucket'
BUCKET = 'capstones3bucket'

# SERVER_URL = 'https://capstoneherokuapp.herokuapp.com/'
SERVER_URL = 'http://127.0.0.1:5000'

# DOWNLOAD_PATH = Path(r"./download")
DOWNLOAD_PATH = Path(r"./download")


# component compress and upload
def cu(name, version, *files):
    """
    $ python cli.py cu <name> <version> <*files>

    Example:
        $ python cli.py cu z 1 folder1 README.md
    will create z--v1.zip containing folder1 and README.md


    $ python cli.py cu product/c0 1 product/0.txt
    creates ./c0--v1.zip locally
    uploads to  product/c0--v1.zip in s3bucket
    deletes ./c0--v1.zip local file


    :param name:
    :param version:
    :param files:
    :return: True when success, False when failure
    """

    name_path = Path(name)  # converts name string to Path.  1/2/3/name  =>  1\2\3\name
    name_parent = name_path.parent  # parent directory    1\2\3
    name_name = name_path.name  # file name without parent.  name

    name_zip = name_name + "--v" + str(version) + ".zip"  # name--v1.2.3.4.zip
    logging.debug("name_zip = " + str(name_zip))

    name_path_zip = name_parent.joinpath(name_zip).as_posix()  # 1/2/3/name--v1.2.3.4.zip

    # check component's existence in database
    if component_exist(name, version):
        print("409 Component already exists")
        return False

    try:

        # must create folder path for zip file to go

        # Compress
        compress(name_zip, *files)
        # list_zip(name_zip) # prints list of files inside zip. Comment to turn off
        # To do: take file list or wild cards, must extract file list, and wild card list, then pass to compress()

        # Upload
        upload(name_zip, BUCKET, name_path_zip)
        logging.info(str(name_path_zip) + " is compressed and uploaded to: " + BUCKET)

        # post metadata
        add_component(name, version)

    except Exception as e:
        logging.error(e)
        return False

    finally:
        # delete zip file
        if Path(name_zip).exists():
            Path(name_zip).unlink()
        pass

    return True


# recipe download and extract
def rde(product_name, version_number=""):
    """
    $ python cli.py rde <product> <version>

    Example: finds recipe with product named product1 and version 1.2.3.4
    And downloads the components in the recipe list and extracts in folder specified by de() function
    $ python cli.py rde product1 1.2.3.4

    :param output_folder:
    :param product_name:
    :param version_number:
    :return:
    """
    recipe = get_recipe(str(product_name), str(version_number))
    logging.debug("recipe = " + str(recipe))

    # check if output folder exist and is empty


    if recipe['code'] == '200':
        logging.info("received recipe, assembling")
        for component in recipe['components']:
            print(component)
            de(component['name'], component['version'], component['destination'])
        return 'Success'
    else:
        return "Failure Error code: " + recipe['code']


# component download and extract to target directory
def de(name, version, destination='.'):
    """
    def de(name, version, target_dir='./download/product'):


    $ python cli.py de <name> <version> <target_dir>

    EXAMPLE: extract z_v1.zip to ./download/folder1
    $ python cli.py de z 1 ./download/folder1


    $ python cli.py de product/c0 1 dest1
    downloads product/c0--v1.zip to ./c0--v1.zip
    extracts to DOWNLOAD_PATH/product/
    deletes c0--v1.zip local file


    :param name:
    :param version:
    :param destination:
    :return: True if success, False if failure
    """

    name_path = Path(name)  # converts name string to Path.  1/2/3/name  =>  1\2\3\name
    name_parent = name_path.parent  # parent directory    1\2\3
    name_name = name_path.name  # file name without parent.  name

    name_zip = name_name + "--v" + str(version) + ".zip"  # name--v1.2.3.4.zip
    logging.debug("name_zip = " + str(name_zip))

    name_path_zip = name_parent.joinpath(name_zip).as_posix()  # 1/2/3/name--v1.2.3.4.zip

    # download_folder/name_path.parent/destination
    extract_path = DOWNLOAD_PATH.joinpath(name_parent).joinpath(destination)

    try:
        # Download
        download(BUCKET, name_path_zip, name_zip)

        # Extract
        ziptest(name_zip)  # test if downloaded file is valid zip file
        extract(name_zip, extract_path)

    except Exception as e:
        logging.error(e)
        return False

    finally:
        # delete zip file
        if Path(name_zip).exists():
            Path(name_zip).unlink()

    logging.info(name_zip + " is downloaded from: " + BUCKET + " and extracted to: " + str(destination))

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


# Extract zipfile into target directory. Automatically creates target directory if not exist.
def extract(src, target_dir):
    """
    :param src:
    :param target_dir:
    :return:
    """
    with ZipFile(src, 'r') as zf:
        zf.extractall(target_dir)


# Test whether the zipfile is valid or not.
def ziptest(src):
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

    object name field needed to have folder structure
    $ python cli.py upload requirements.txt capstones3bucket 1/2.txt

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
def download(bucket, object_name, file_name=None):
    """Download file from S3 bucket

    :param bucket: bucket name
    :param object_name: s3 object path
    :param file_name: local path
    :return: True if downloaded, False if failed
    """

    # If S3 file_name was not specified, use DOWNLOAD_PATH/object_name
    if file_name is None:
        file_name = DOWNLOAD_PATH.joinpath(object_name).as_posix()

    # must create file_name's full parent path
    destination_path = Path(file_name).parent
    if not destination_path.exists():
        destination_path.mkdir(parents=True, exist_ok=True)

    # Download file
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket, object_name, file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def f1():
    text = 'stndfaei'
    logging.info("function f1()" + text)
    logging.debug("text = " + str(text))
    return 1


# Get a list of versions for a specific component
def component_version(name):
    component = {'name': str(name)}

    url = SERVER_URL + '/cversion'
    response = requests.post(url, json=component)
    logging.debug("response.text = " + str(response.text))

    return response.text


# check if component exist in database
def component_exist(name, version):
    component = {'name': str(name),
                 'version': str(version)}

    url = SERVER_URL + '/cli_exist'
    response = requests.post(url, json=component)
    logging.debug("response.text = " + str(response.text))

    if "404" in response.text:
        return False
    elif "409" in response.text:
        return True


# post component metadata
def add_component(name, version: str):
    component = {'name': str(name),
                 'version': str(version)}

    url = SERVER_URL + '/cli_add'
    response = requests.post(url, json=component)

    if "409" in response.text:
        logging.error(response.text)
        return False
    elif "201" in response.text:
        logging.debug("response.text = " + str(response.text))
        return True


def get_recipe(product_name, version_number=""):
    url = SERVER_URL + '/cli_recipe'
    req_data = {'product_name': str(product_name),
                'version_number': str(version_number)}

    r = requests.post(url, json=req_data)
    recipe = r.json()  # converted from json str to <class 'dict'>

    return recipe


if __name__ == '__main__':
    fire.Fire()
