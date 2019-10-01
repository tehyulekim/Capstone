""r"""

"""
from flask import Flask, request, render_template, json, jsonify
from flask_sqlalchemy import SQLAlchemy

import logging

logging.basicConfig(level=logging.DEBUG)  # comment out to turn off info messages

app = Flask(__name__)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://yijwjkfpucdepl:76e1c9f816bb03c73393508f6dac75f411a56105e74c2b14ebd9a8fc87025788@ec2-54-221-214-3.compute-1.amazonaws.com:5432/del3ceijjamsso'

db = SQLAlchemy(app)

db.drop_all()


class Product(db.Model):
    name = db.Column(db.String(255), primary_key=True)
    software_releases = db.relationship("SoftwareRelease", back_populates="product",
                                        cascade="all, delete, delete-orphan")


class SoftwareRelease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), db.ForeignKey('product.name'))
    version_number = db.Column(db.String(255))
    status = db.Column(db.String(255), default='In Development')
    __table_args__ = (db.UniqueConstraint('product_name', 'version_number'),)
    product = db.relationship("Product", back_populates="software_releases")
    components = db.relationship("Association", back_populates="software_release", cascade="all, delete, delete-orphan")


class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    version = db.Column(db.String(255))
    __table_args__ = (db.UniqueConstraint('name', 'version'),)
    software_releases = db.relationship("Association", back_populates="component", cascade="all, delete, delete-orphan")


# Association object for SoftwareRelease and Component. Includes extra column: Destination path
class Association(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    software_release_id = db.Column(db.Integer, db.ForeignKey('software_release.id'))
    component_id = db.Column(db.Integer, db.ForeignKey('component.id'))
    destination = db.Column(db.String(65535), default='.', nullable=False)  # if nullable, bypasses unique constraint
    __table_args__ = (db.UniqueConstraint('software_release_id', 'component_id', 'destination'),)
    component = db.relationship("Component", back_populates="software_releases")
    software_release = db.relationship("SoftwareRelease", back_populates="components")


db.create_all()

r"""
from app import db, Product, SoftwareRelease,Component, Association

Product.query.all()
SoftwareRelease.query.all()
Component.query.all()
Association.query.all()


for x in Component.query.all():
    print(x.name, x.version)


p1 = Product(name="p1")
db.session.add(p1)
p2 = Product(name="p2")
db.session.add(p2)

s1 = SoftwareRelease(product_name="p1", version_number="1")
db.session.add(s1)
s2 = SoftwareRelease(product_name="p2", version_number="1")
db.session.add(s2)

c1 = Component(name="c1", version="1")
db.session.add(c1)
c2 = Component(name="c2", version="1")
db.session.add(c2)

db.session.commit()



a1 = Association.query.filter_by(id=1).first()
a2 = Association.query.filter_by(id=2).first()
a3 = Association.query.filter_by(id=3).first()
a4 = Association.query.filter_by(id=4).first()
a12 = Association.query.filter_by(id=12).first()



a1 = Association()
a1.component = c1
s1.components.append(a1)

a2 = Association()
a2.component = c2
s2.components.append(a2)

a3 = Association()
a3.component = c1
s2.components.append(a3)

db.session.commit()


a12 = Association(id=12, component=c1)
s1.components.append(a12)


a2.component = c2
s2.components.append(a4)


a2 = Association.query.filter_by(software_release_id=2, component_id=2).first()
db.session.delete(a2)
db.session.commit()





https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html

# create parent, append a child via association
p = Parent()
a = Association(extra_data="some data")
a.child = Child()
p.children.append(a)

# iterate through child objects via association, including association
# attributes
for assoc in p.children:
    print(assoc.extra_data)
    print(assoc.child)






c1 = Component.query.filter_by(id=1).first()

s1 = SoftwareRelease.query.filter_by(id=1).first()
s2 = SoftwareRelease.query.filter_by(id=2).first()


s1.name= "s1"
s1.version = 1




db.session.rollback()
db.drop_all()

db.engine.table_names()



"""


# add component
# http://127.0.0.1:5000/add
@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        # component = json.loads(request.data)  # {'name': name, 'version': version} # <class 'dict'>

        component = request.get_json()  # <class 'dict'>
        name = component['name']
        version = component['version']
        logging.debug("name = " + str(name))
        logging.debug("version = " + str(version))

        # test with POSTMAN {"name": "c1", "version": "1"}
        # query component
        query_component = db.session.query(Component).filter_by(name=name, version=version).first()

        # check if exist
        if query_component is not None:
            return "409 Conflict. Component already exists"

        # add component
        component_new = Component(name=name, version=version)
        db.session.add(component_new)
        db.session.commit()

        # j1 = jsonify(username="user1", email="email2")
        # logging.debug("j1 = " + str(j1))
        # logging.debug("type(j1) = " + str(type(j1)))  # <class 'flask.wrappers.Response'>

        return "201 Created. Component is added"

    return '/add page text message'


# check component's existence
# http://127.0.0.1:5000/check
@app.route('/check', methods=['POST', 'GET'])
def check():
    component = request.get_json()  # <class 'dict'>
    name = component['name']
    version = component['version']

    query_component = db.session.query(Component).filter_by(name=name, version=version).first()

    # check if exist
    if query_component is not None:
        return "409 Conflict. Component already exists"

    return "404 Not Found. Component does not exist"


# bring recipe
# http://127.0.0.1:5000/b
@app.route('/b', methods=['POST', 'GET'])
def bring():
    c1 = {'name': 'x', 'version': '1'}
    c2 = {'name': 'y', 'version': '2'}
    c3 = {'name': 'z', 'version': '3'}
    product1 = {'Name': 'product1'}

    # recipe == software release
    r1 = {
        'Product': product1,
        'Version Number': '1.2.3.4',
        'Status': 'In Development',
        'component_list': [
            c1,
            c2,
            c3
        ]
    }

    if request.method == 'POST':
        return json.dumps(r1)

    return json.dumps(r1)


# save component > SQL, and create new recipe
# http://127.0.0.1:5000/c
@app.route('/c', methods=['POST', 'GET'])
def create():
    d1 = {'11': 111, '22': 222}

    j1 = json.dumps(d1)

    if request.method == 'POST':
        pass

    return j1


# http://127.0.0.1:5000/r
@app.route('/r', methods=['POST', 'GET'])
def recipe():
    if request.method == 'POST':
        return request.data

    return 'r page text message'


# view all
# http://127.0.0.1:5000/v
@app.route('/v', methods=['POST', 'GET'])
def view():
    if request.method == 'POST':
        return request.data

    pquery = Product.query.all()
    squery = SoftwareRelease.query.all()
    cquery = Component.query.all()
    aquery = Association.query.all()

    plist = []
    for p in pquery:
        plist.append(p.name)

    slist = []
    for s in squery:
        slist.append(s.product_name + "--v" + s.version_number)

    clist = []
    for c in cquery:
        clist.append(c.name + "--v" + c.version)

    # Component Names
    cset = set()
    for c in cquery:
        cset.add(c.name)
    cname = sorted(list(cset))

    # also make components list with highest version number

    alist = []
    for a in aquery:
        alist.append(a.software_release.product_name + "_" + a.component.name)

    viewall = {
        "Product": str(plist),
        "SoftwareRelease": str(slist),
        "Component": str(clist),
        "Component_Names": str(cname),
        "Association": str(alist)
    }

    return json.dumps(viewall)


# Get a list of all component names
# http://127.0.0.1:5000/cname
@app.route('/cname', methods=['POST', 'GET'])
def cname():
    if request.method == 'POST':
        return request.data

    cquery = Component.query.all()

    clist = []
    for c in cquery:
        clist.append(c.name + "--v" + c.version)

    # Component Names
    cset = set()
    for c in cquery:
        cset.add(c.name)
    cname_list = sorted(list(cset))

    # also make components list with highest version number

    cname_dict = {
        "component_names": str(cname_list),
    }

    return json.dumps(cname_dict)


# Get a list of versions for a specific component
# http://127.0.0.1:5000/cversion
@app.route('/cversion', methods=['POST', 'GET'])
def cversion():
    if request.method == 'POST':

        component = request.get_json()  # <class 'dict'>
        name = component['name']

        cquery = Component.query.filter_by(name=name).all()

        clist = []
        for c in cquery:
            clist.append(c.version)

        cversion_sorted = sorted(clist)

        cversion_dict = {"component_versions": str(cversion_sorted)}

        return json.dumps(cversion_dict)

    return 'cversion is POST. request body example: {"name": "component_name"}'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/1')
def f1():
    return render_template('page1.html')


@app.route('/5')
def f5():
    pass
    # return alchemy.f1()


@app.route('/dbca')
def dbca():
    db.create_all()
    return 'db.create_all()'


if __name__ == '__main__':
    app.run()
