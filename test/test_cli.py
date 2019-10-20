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
    logging.debug("cli.f1() = " + str(cli.f1()))
    assert cli.f1('text') == 'text'

