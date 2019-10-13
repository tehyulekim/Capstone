""r"""
sample script 

To pass a list to a function, use a python script. 
CLI will not accept list, because cannot use unpack list method f(*list)

must unpack list at input

f( *list, 3,4 ) => 1,2,3,4 
= parse glob => full names

f2(compress) 







"""
from pathlib import Path

import cli


# file list of wildcards, => parse to file list
def f1(*files):
    file_list = []
    for file in files:
        for file_plain in list(Path().glob(file)):
            file_list.append(file_plain.as_posix())
    return file_list


list3 = f1(*['_Note/*.txt', '_Note/*.js'], '_Note/*.py', '_Note/*.vue')

# cli.compress('z.zip', *list3)


component1 = [
    'product/1/2',
    'product/1/*.txt',
]

cli.cu('c1', '1.1.1.1', *component1)