""""""r"""
import sys

print("sys.argv = ", sys.argv)
print("sys.argv[0] = ", sys.argv[0])
print("sys.argv[1] = ", sys.argv[1])


if sys.argv == 1:
    print(111)
if sys.argv == 2:
    print(222)




s1= '123'
s2= '.zip'
s3= s1 +s2
print("s3 = ", s3)
print("stnd", "stnd")

print("stnd"+str(3))



def f1(x,*y):
    print(list(y))

f1(1,2,3,4,5)




# compress and upload
def cu(name, version, input_files):

    logging.info("function cu")

    name_zip = name + "_" + str(version) + ".zip"

    with ZipFile(name_zip, 'w') as file:
        file.write(input_files)
        print('zipfile write complete')

    with ZipFile(name_zip) as file:
        print(file.namelist())
        
        
# download and extract
def de(name, version, target_dir='.'):
    logging.info("function de")

    name_zip = name + "_" + str(version) + ".zip"
    
    extract(name_zip, target_dir)

    with ZipFile(name_zip) as file:
        print(file.namelist())
        file.printdir()
        file.extractall()
        print('zipfile extract complete')












c1 = {'name': 'z', 'version': '1'}
c2 = {'name': 'x', 'version': '2'}
product1 = {'Name': 'product1'}

# recipe == software release
r1 = {
    'Product': product1,
    'Version Number': '1.2.3.4',
    'Status': 'In Development',
    'component_list': [
        c1,
        c2
    ]
}

for x in r1['component_list']:
    print(x)
    print(x['name'])
    
    
    
    
"""
