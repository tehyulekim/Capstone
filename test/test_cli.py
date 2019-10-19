""r"""
https://docs.pytest.org/en/latest/

pytest show print() only when test fails

test each function
# test zipping self, and unzipping self created file

    test_zip(name_zip)
    extract(name_zip, target_dir)



TODO test upload
upload_file('test.txt', 'capstones3bucket')


DOWNLOAD_PATH = Path(r"./download")
print("DOWNLOAD_PATH.exists() = " + str(DOWNLOAD_PATH.exists()))


https://docs.python.org/3/library/pathlib.html#pathlib.Path.exists
Path('.').exists()

Path('setup.py').exists()

Path('/etc').exists()

Path('nonexistentfile').exists()

"""
from cstore import cli
import logging


def test_f1():
    print("cli.f1() = ", cli.f1())
    logging.info("stnd")
    assert cli.f1() == 1


def test_t2():
    print("test2")
    logging.info("test2")


def test_t3():
    print("test3")
    logging.info("t3")


def test_download():
    cli.download(cli.BUCKET, 'product1/f1/f2/z.zip_v1.2.3.4.zip')


def test_download_filename():
    cli.download(cli.BUCKET, 'product1/f1/f2/z.zip_v1.2.3.4.zip', 'download/product1/f1/f2/z.zip_v1.2.3.4.zip')

def test_de():
    # def de(name, version, target_dir=DOWNLOAD_PATH)
    cli.de('product1/x', 1)

def test_de2():
    # def de(name, version, target_dir=DOWNLOAD_PATH)
    cli.de('y', 2)
