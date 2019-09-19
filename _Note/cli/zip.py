from zipfile import ZipFile

# https://www.datacamp.com/community/tutorials/zip-file#CZF


file_name = 'test.zip'

with ZipFile(file_name, 'w') as file:
    file.write('test.jpg')
    print('File overrides the existing files')

with ZipFile(file_name) as file:
    print(file.namelist())

with ZipFile(file_name, 'a') as file:
    file.write('test.txt')

with ZipFile(file_name) as file:
    print(file.namelist())
