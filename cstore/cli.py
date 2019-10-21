""r"""

Must configure constants:

SERVER_URL
OUTPUT_FOLDER


"""

import os
import logging
import requests
import fire
# import boto3
# from botocore.exceptions import ClientError
from zipfile import ZipFile
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)  # .DEBUG .INFO .ERROR

# BUCKET = 'capstonebuckets3'

# SERVER_URL = 'https://capstoneherokuapp.herokuapp.com/'
SERVER_URL = 'http://127.0.0.1:5000'

OUTPUT_FOLDER = Path(r"./downloads")


def store(name, version, *args):
    """
    Store a component
    previously named cu() Compress and Upload Component

    $ python cli.py store <name> <version> <*files>

    Example:
        $ python cli.py store z 1 folder1 README.md
    will create z--v1.zip containing folder1 and README.md

    $ python cli.py cu product/c0 1 product/0.txt
    creates ./c0--v1.zip locally
    uploads to  product/c0--v1.zip in s3bucket
    deletes ./c0--v1.zip local file


    $ python cli.py cu c1 1.2 [filelist.txt,filelist2.txt]


    IMPORTANT!     must not have space or . in list input. Because Python Fire limitation.
    To input filelist.txt and filelist2.txt:
    [filelist,filelist2]



    :param name:
    :param version:
    :param args: string
    :return: True when success, False when failure
    """
    logging.debug("args = " + str(args))

    # check component's existence in database
    if component_exist(name, version):
        print("409 Component already exists")
        return False

    name_path = Path(name)  # converts name string to Path.  1/2/3/name  =>  1\2\3\name
    name_parent = name_path.parent  # parent directory    1\2\3
    name_name = name_path.name  # file name without parent directory.  name
    name_zip = name_name + "--v" + str(version) + ".zip"  # name--v1.2.3.4.zip
    logging.debug("name_zip = " + str(name_zip))
    name_path_zip = name_parent.joinpath(name_zip).as_posix()  # 1/2/3/name--v1.2.3.4.zip

    # turn all input into list containing plain strings
    list_string = []
    for a in args:
        if type(a) == list:  # list type is parsed as file.txt; [ filelist.txt, filelist2.txt]
            for filelist in a:
                with open(filelist + '.txt', 'r') as file_list:
                    lines = file_list.read().split('\n')  # each line is file path
                for line in lines:
                    if line != '':  # remove empty lines being registered as ''
                        list_string.append(str(line))
        else:  # type string
            if a != '':  # removes empty string
                list_string.append(str(a))

    logging.debug("list_string = " + str(list_string))

    # convert glob pattern (wildcard) names to plain names
    final_list = []
    for file in list_string:
        for file_plain in list(Path().glob(file)):
            final_list.append(file_plain.as_posix())

    logging.debug("final_list = " + str(final_list))

    try:
        # Compress
        compress(name_zip, *final_list)
        # list_zip(name_zip) # prints list of files inside zip. Comment to turn off
        # To do: take file list or wild cards, must extract file list, and wild card list, then pass to compress()

        # Upload
        # upload_s3(name_zip, BUCKET, name_path_zip)
        upload(name_zip, name_path_zip)

        logging.info(str(name_path_zip) + " is compressed and uploaded")

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


def retrieve(name, version, destination='.', output_folder=OUTPUT_FOLDER):
    """
    Retrieve a Component
    Download and Extract Component
    # Retrieve a Component. component download and extract to target directory, previously named de()


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
    extract_path = output_folder.joinpath(name_parent).joinpath(destination)

    try:
        # Download
        # download_s3(BUCKET, name_path_zip, name_zip)
        download(name_path_zip)

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

    logging.info(name_zip + " is downloaded and extracted to: " + str(output_folder))

    return True


def assemble(product_name, version_number="", output_folder = r"./downloads"):
    """
    Assemble Software Release recipe
    Recipe Download and Extract
    previously named rde()

    $ python cli.py assemble <product> <version>

    Example: finds recipe with product named product1 and version 1.2.3.4
    And downloads the components in the recipe list and extracts in folder specified by de() function
    $ python cli.py rde product1 1.2.3.4

    :param product_name:
    :param version_number:
    :return:
    """
    recipe = get_recipe(str(product_name), str(version_number))
    logging.debug("recipe = " + str(recipe))

    output_folder = Path(str(output_folder))

    if output_folder.exists() and len(list(output_folder.iterdir())) > 0:
        return "Output folder is not empty"

    if recipe['code'] == '200':
        logging.info("received recipe, assembling")
        for component in recipe['components']:
            print(component)
            retrieve(component['name'], component['version'], component['destination'], output_folder)
        return 'Success'
    else:
        return "Failure Error code: " + recipe['code']


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
            zippath = Path(path)  # modified; keep all folder structure 1/2/3/4.txt
            # zippath = os.path.basename(path)
            # if not zippath:
            #     zippath = os.path.basename(os.path.dirname(path))
            # if zippath in ('', os.curdir, os.pardir):
            #     zippath = ''
            add_to_zip(zf, path, zippath)


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


def upload(file_name, object_name=None):
    """

    :param file_name:
    :param object_name:
    :return:
    """
    if object_name is None:
        object_name = file_name

    file_name = str(file_name)
    object_name = str(object_name)

    url = SERVER_URL + '/upload'
    req_data = {'file_name': object_name}

    try:
        files = {'file': open(file_name, 'rb')}
        r = requests.post(url, data=req_data, files=files)
        print(r.text)
    except:
        return False
    return True


def download(object_name, file_name=None):
    object_name = str(object_name)

    if file_name is None:
        file_name = Path(object_name).name  # no parent directory

    url = SERVER_URL + "/static/uploads/" + object_name

    try:
        r = requests.get(url)
        open(file_name, 'wb').write(r.content)
    except:
        return False
    return True


# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-unploading-files.html
# def upload_s3(file_name, bucket, object_name=None):
#     """Upload a file to an S3 bucket
#
#     EXAMPLE
#     upload_s3('test.zip', 'capstones3bucket')
#
#     object name field needed to have folder structure
#     $ python cli.py upload requirements.txt capstones3bucket 1/2.txt
#
#     :param file_name: File to upload
#     :param bucket: Bucket to upload to
#     :param object_name: S3 object name. If not specified then file_name is used
#     :return: True if file was uploaded, else False
#     """
#
#     # If S3 object_name was not specified, use file_name
#     if object_name is None:
#         object_name = file_name
#
#     # Upload the file
#     s3_client = boto3.client('s3')
#     try:
#         response = s3_client.upload_file(file_name, bucket, object_name)
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True


# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-download-file.html
# def download_s3(bucket, object_name, file_name=None):
#     """Download file from S3 bucket
#
#     :param bucket: bucket name
#     :param object_name: s3 object path
#     :param file_name: local path
#     :return: True if downloaded, False if failed
#     """
#     if file_name is None:
#         file_name = Path(object_name).name  # no folder
#
#     # Download file
#     s3 = boto3.client('s3')
#     try:
#         s3.download_file(bucket, object_name, file_name)
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True


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

    url = SERVER_URL + '/cli_delete_c'
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
    Get Recipe in JSON
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


# testing functions
def f1(*args):
    print("args = " + str(args))
    for a in args:
        if type(a) == str:
            print('str: ' + a)
            return a
        if type(a) == list:
            print('list: ' + str(a))


def f6(file_name):
    url = SERVER_URL + '/6'
    req_data = {'stnw': 'faei'}
    # req_data = {'file_name': str(file_name)}
    files = {'file': open(file_name, 'rb')}
    r = requests.post(url, data=req_data, files=files)
    return r.text


def main():
    fire.Fire()


if __name__ == '__main__':
    main()
