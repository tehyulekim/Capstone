""r"""

"""
from zipfile import ZipFile


def extract(src, curdir):
    with ZipFile(src, 'r') as zf:
        zf.extractall(curdir)

extract('test.zip', '.')