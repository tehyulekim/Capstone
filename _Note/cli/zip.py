""r"""
https://www.datacamp.com/community/tutorials/zip-file#CZF

https://github.com/python/cpython/blob/3.7/Lib/zipfile.py
Source code: Lib/zipfile.py


zipfile source code to get command line for compressing folder

 elif args.create is not None:
        zip_name = args.create.pop(0)
        files = args.create

        def addToZip(zf, path, zippath):
            if os.path.isfile(path):
                zf.write(path, zippath, ZIP_DEFLATED)
            elif os.path.isdir(path):
                if zippath:
                    zf.write(path, zippath)
                for nm in sorted(os.listdir(path)):
                    addToZip(zf,
                             os.path.join(path, nm), os.path.join(zippath, nm))
            # else: ignore

        with ZipFile(zip_name, 'w') as zf:
            for path in files:
                zippath = os.path.basename(path)
                if not zippath:
                    zippath = os.path.basename(os.path.dirname(path))
                if zippath in ('', os.curdir, os.pardir):
                    zippath = ''
                addToZip(zf, path, zippath)



# source code modified. recursive function
def f4(zip_name, *files):
    def addToZip(zf, path, zippath):
        if os.path.isfile(path):
            zf.write(path, zippath, 8)  # ZIP_DEFLATED = 8
        elif os.path.isdir(path):
            if zippath:
                zf.write(path, zippath)
            for nm in sorted(os.listdir(path)):
                addToZip(zf, os.path.join(path, nm), os.path.join(zippath, nm))
        # else: ignore

    with ZipFile(zip_name, 'w') as zf:
        for path in files:
            zippath = os.path.basename(path)
            if not zippath:
                zippath = os.path.basename(os.path.dirname(path))
            if zippath in ('', os.curdir, os.pardir):
                zippath = ''
            addToZip(zf, path, zippath)


"""
import os
from zipfile import ZipFile

import fire

file_name = 'test.zip'


def f1():
    with ZipFile(file_name, 'w') as file:
        file.write('test.jpg')
        print('File overrides the existing files')

    with ZipFile(file_name) as file:
        print(file.namelist())


def f2():
    with ZipFile(file_name, 'a') as file:
        file.write('test.txt')

    with ZipFile(file_name) as file:
        print(file.namelist())


def f3():
    with ZipFile(file_name) as zf:
        zf.printdir()


# source code modified. recursive function
def f4(zip_name, *files):
    def addToZip(zf, path, zippath):
        if os.path.isfile(path):
            zf.write(path, zippath, 8)  # ZIP_DEFLATED = 8
        elif os.path.isdir(path):
            if zippath:
                zf.write(path, zippath)
            for nm in sorted(os.listdir(path)):
                addToZip(zf, os.path.join(path, nm), os.path.join(zippath, nm))
        # else: ignore

    with ZipFile(zip_name, 'w') as zf:
        for path in files:
            zippath = os.path.basename(path)
            if not zippath:
                zippath = os.path.basename(os.path.dirname(path))
            if zippath in ('', os.curdir, os.pardir):
                zippath = ''
            addToZip(zf, path, zippath)


# https://docs.python.org/3/library/zipfile.html#zipfile.ZipFile.write
# writes zip file with dir name, folder structure
def f5():
    with ZipFile(file_name, 'w') as file:
        file.write('test.txt', arcname='a/11/test.txt')
        print('File overrides the existing files')

    with ZipFile(file_name) as file:
        print(file.namelist())


if __name__ == '__main__':
    fire.Fire()
    f5()
