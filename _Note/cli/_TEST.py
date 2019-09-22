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