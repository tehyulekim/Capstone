""r"""
need to append file for multiple file zipping
"""

import os
import logging
from zipfile import ZipFile

import fire

logging.basicConfig(level=logging.DEBUG)  # comment this to turn off debug and info messages


# compress and upload
def cu(name, version, *files):
    """
    $ python cli.py cu <name> <version> <*files>

    Example: will create z_1.zip containing folder1 and README.md
    $ python cli.py cu z 1 folder1 README.md


    :param name:
    :param version:
    :param files:
    :return:
    """
    logging.info("function cu")

    name_zip = name + "_" + str(version) + ".zip"

    compress(name_zip, *files)
    list_zip(name_zip)


# download and extract
def de(name, version, target_dir='.'):
    """
    $ python cli.py de <name> <version> <target_dir>

    EXAMPLE:  will extract z_1.zip to folder1
    $ python cli.py de z 1 folder1


    $ python cli.py de z 1 ~/Desktop/folder2


    :param name:
    :param version:
    :param target_dir:
    :return:
    """
    logging.info("function de")

    name_zip = name + "_" + str(version) + ".zip"

    test_zip(name_zip)
    extract(name_zip, target_dir)


# Create zipfile from source files.
# commandline zipfile -c in https://docs.python.org/3/library/zipfile.html
# source code modified from zipfile.py. recursive function.
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
    print("Done testing")


# List files in a zipfile.
def list_zip(src):
    with ZipFile(src, 'r') as zf:
        zf.printdir()


def upload():
    logging.info("function up")
    pass


def download():
    logging.info("function down")
    pass


def f1():
    logging.info("function f1")
    return 1


if __name__ == '__main__':
    fire.Fire()
