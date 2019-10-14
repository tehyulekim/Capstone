""r"""
Must configure constants:

BUCKET
SERVER_URL
OUTPUT_FOLDER


Must install:

pip install requests
pip install fire
pip install boto3
pip install awscli


Must configure: 

$ aws configure

enter your AWS account, and S3 Bucket
otherwise use this user account temporarily to access BUCKET 'capstonebuckets3'

AKIARSKDD7KW6CZDHZ4G
IAM0/AH/NqhJgtXFaJGIhTzEEbH1jU3bpMDGgVFF
ap-southeast-2
json


"""

import os
import logging
import requests
import fire
import boto3
from botocore.exceptions import ClientError
from zipfile import ZipFile
from pathlib import Path

logging.basicConfig(level=logging.INFO)  # .DEBUG .INFO .ERROR

BUCKET = 'capstonebuckets3'

# SERVER_URL = 'https://capstoneherokuapp.herokuapp.com/'
SERVER_URL = 'http://127.0.0.1:5000'

OUTPUT_FOLDER = Path(r"./download")


def cu(name, version, *files):
    """
    Compress and Upload Component

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

    # check component's existence in database
    if component_exist(name, version):
        print("409 Component already exists")
        return False

    name_path = Path(name)  # converts name string to Path.  1/2/3/name  =>  1\2\3\name
    name_parent = name_path.parent  # parent directory    1\2\3
    name_name = name_path.name  # file name without parent.  name
    name_zip = name_name + "--v" + str(version) + ".zip"  # name--v1.2.3.4.zip
    logging.debug("name_zip = " + str(name_zip))
    name_path_zip = name_parent.joinpath(name_zip).as_posix()  # 1/2/3/name--v1.2.3.4.zip

    # wildcard (glob) to plain names
    file_list = []
    for file in files:
        for file_plain in list(Path().glob(file)):
            file_list.append(file_plain.as_posix())

    try:
        # Compress
        compress(name_zip, *file_list)
        # list_zip(name_zip) # prints list of files inside zip. Comment to turn off
        # To do: take file list or wild cards, must extract file list, and wild card list, then pass to compress()

        # Upload
        upload(name_zip, BUCKET, name_path_zip)
        logging.info(str(name_path_zip) + " is compressed and uploaded to: " + BUCKET)

        # post metadata
        add_c(name, version)

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
    Recipe Download and Extract

    $ python cli.py rde <product> <version>

    Example: finds recipe with product named product1 and version 1.2.3.4
    And downloads the components in the recipe list and extracts in folder specified by de() function
    $ python cli.py rde product1 1.2.3.4

    :param product_name:
    :param version_number:
    :return:
    """
    recipe = get_recipe(str(product_name), str(version_number))
    logging.debug("recipe = " + str(recipe))

    if OUTPUT_FOLDER.exists() and len(list(OUTPUT_FOLDER.iterdir())) > 0:
        return "Output folder is not empty"

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
    Download and Extract Component

    def de(name, version, target_dir='./download/product'):


    $ python cli.py de <name> <version> <target_dir>

    EXAMPLE: extract z_v1.zip to ./download/folder1
    $ python cli.py de z 1 ./download/folder1


    $ python cli.py de product/c0 1 dest1
    downloads product/c0--v1.zip to ./c0--v1.zip
    extracts to OUTPUT_FOLDER/product/
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
    extract_path = OUTPUT_FOLDER.joinpath(name_parent).joinpath(destination)

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
def compress(zip_name, *files):
    """Create zipfile from source files."""
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


#
def extract(src, target_dir):
    """
    Extract zipfile into target directory. Automatically creates target directory if not exist.
    :param src:
    :param target_dir:
    :return:
    """
    with ZipFile(src, 'r') as zf:
        zf.extractall(target_dir)



def ziptest(src):
    """Test whether the zipfile is valid or not."""
    with ZipFile(src, 'r') as zf:
        bad_file = zf.testzip()
    if bad_file:
        print("The following enclosed file is corrupted: {!r}".format(bad_file))
    print(src, "Done testing: zipfile is valid")


def list_zip(src):
    """List files in a zipfile"""
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
    if file_name is None:
        file_name = Path(object_name).name

    # Download file
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket, object_name, file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def component_version(name):
    """
    Get a list of versions for a specific component
    :param name:
    :return:
    """
    req_data = {'name': str(name)}

    url = SERVER_URL + '/cversion'
    response = requests.post(url, json=req_data)
    logging.debug("response.text = " + str(response.text))

    return response.text


# check if component exist in database
def component_exist(name, version):
    """
    Check if component exists
    :param name:
    :param version:
    :return:
    """
    req_data = {'name': str(name),
                'version': str(version)}

    url = SERVER_URL + '/cli_exist'
    response = requests.post(url, json=req_data)
    logging.debug("response.text = " + str(response.text))

    if "404" in response.text:
        return False
    elif "409" in response.text:
        return True


def add_c(name, version):
    """
    Add Component metadata
    :param name:
    :param version:
    :return:
    """
    req_data = {'name': str(name),
                'version': str(version)}

    url = SERVER_URL + '/cli_add'
    response = requests.post(url, json=req_data)

    # "409 Conflict. Component already exists"
    # "201 Created. Component is added"
    if "409" in response.text:
        logging.error(response.text)
        return False
    elif "201" in response.text:
        logging.debug("response.text = " + str(response.text))
        return True


# # delete component in SQL and S3, also deletes associated SR contents
def delete_c(name, version):
    """
    Delete Component
    :param name:
    :param version:
    :return:
    """
    req_data = {'name': str(name),
                'version': str(version)}

    url = SERVER_URL + '/cli_delete'
    response = requests.post(url, json=req_data)
    return response.text


def delete_p(name):
    """
    Delete Product
    :param name:
    :return:
    """
    req_data = {'name': str(name)}

    url = SERVER_URL + '/pdelete'
    response = requests.post(url, json=req_data)
    return response.text


def delete_sr(product_name, version_number):
    """
    Delete Software Release
    :param product_name:
    :param version_number:
    :return:
    """
    req_data = {'product_name': str(product_name),
                'version_number': str(version_number)}

    url = SERVER_URL + '/srdelete'
    response = requests.post(url, json=req_data)
    return response.text


def get_recipe(product_name, version_number=""):
    """
    Get Recipe
    :param product_name:
    :param version_number:
    :return:
    """
    url = SERVER_URL + '/cli_recipe'
    req_data = {'product_name': str(product_name),
                'version_number': str(version_number)}

    r = requests.post(url, json=req_data)
    recipe = r.json()  # converted from json str to <class 'dict'>

    return recipe


def f1(*args):
    print("args = " + str(args))
    for a in args:
        print(a)


if __name__ == '__main__':
    fire.Fire()
