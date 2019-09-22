""r"""

sr = software release
r = recipe


https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#simple-example
One to many relationship

"""

c1 = {
    'name': 'component1',
    'version': '1.1'
}

c2 = {
    'name': 'component2',
    'version': '1.2'
}

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
