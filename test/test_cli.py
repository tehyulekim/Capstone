""r"""
https://docs.pytest.org/en/latest/

pytest show print() only when test fails

test each function
# test zipping self, and unzipping self created file

    test_zip(name_zip)
    extract(name_zip, target_dir)



TODO test upload
upload_file('test.txt', 'capstones3bucket')


"""
import cli


def test_f1():
    print("cli.f1() = ", cli.f1())
    assert cli.f1() == 1

