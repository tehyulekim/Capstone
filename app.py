""r"""

"""
from itertools import groupby

from flask import Flask, request, jsonify, redirect
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
    software_releases = db.relationship("SoftwareRelease", back_populates="product", cascade="all, delete-orphan")


class SoftwareRelease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), db.ForeignKey('product.name', onupdate="CASCADE"), nullable=False)
    version_number = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), default='In Development')
    __table_args__ = (db.UniqueConstraint('product_name', 'version_number'),)
    product = db.relationship("Product", back_populates="software_releases")
    components = db.relationship("Association", back_populates="software_release", cascade="all, delete-orphan")


class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(255), nullable=False)
    __table_args__ = (db.UniqueConstraint('name', 'version'),)
    software_releases = db.relationship("Association", back_populates="component", cascade="all, delete-orphan")


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


s1 =  SoftwareRelease.query.filter_by(product_name="p1", version_number="1").first()


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


a1.software_release.product_name






a12 = Association(id=12, component=c1)
s1.components.append(a12)


a2.component = c2
s2.components.append(a4)


a2 = Association.query.filter_by(software_release_id=2, component_id=2).first()
db.session.delete(a2)
db.session.commit()


a_new = Association(component=c1)








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


a = Association(component=c3, destination="./dest3")


aquery = Association.query.all()
for a in aquery:
    print(a.software_release.product_name + a.software_release.version_number + a.component.name + a.component.version)
    





c1 = Component.query.filter_by(id=1).first()

s1 = SoftwareRelease.query.filter_by(id=1).first()
s2 = SoftwareRelease.query.filter_by(id=2).first()

s1.name= "s1"
s1.version = 1



db.session.rollback()
db.drop_all()
db.engine.table_names()


"""


@app.route('/')
def index():
    # Not using template engine
    # return render_template('index.html')
    # Must force hard reload in browser CTRL+F5 to use updated static files
    return redirect("/static/index.html")


# add component
# http://127.0.0.1:5000/cli_add
@app.route('/cli_add', methods=['POST'])
def cli_add():
    # component = json.loads(request.data)  # {'name': name, 'version': version} # <class 'dict'>

    component = request.get_json()  # <class 'dict'>
    name = component['name']
    version = component['version']
    logging.debug("name = " + str(name))
    logging.debug("version = " + str(version))

    # test with Postman {"name": "c1", "version": "1"}
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


# check component's existence in database
# http://127.0.0.1:5000/cli_exist
@app.route('/cli_exist', methods=['POST', 'GET'])
def cli_exist():
    component = request.get_json()  # <class 'dict'>
    name = component['name']
    version = component['version']

    query_component = db.session.query(Component).filter_by(name=name, version=version).first()

    # check if exist
    if query_component is not None:
        return "409 Conflict. Component already exists"

    return "404 Not Found. Component does not exist"


# bring sample recipe
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
        return jsonify(r1)

    return jsonify(r1)


# http://127.0.0.1:5000/r
@app.route('/r', methods=['POST', 'GET'])
def requestreturn():
    if request.method == 'POST':
        return jsonify(request.data)

    return 'r page text message'


# view all for debugging
# http://127.0.0.1:5000/v
@app.route('/v', methods=['POST', 'GET'])
def view():
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

    alist = []
    for a in aquery:
        alist.append(
            a.software_release.product_name + "v" + a.software_release.version_number + "_" + a.component.name + "v" + a.component.version)

    viewall = {
        "Product": str(plist),
        "SoftwareRelease": str(slist),
        "Component": str(clist),
        "Component_Names": str(cname),
        "Association": str(alist)
    }

    return jsonify(viewall)


# returns list of all components
# http://127.0.0.1:5000/c
@app.route('/c', methods=['GET'])
def c():
    cquery = Component.query.all()

    clist = []
    for c in cquery:
        clist.append({'name': c.name,
                      'version': c.version})

    return jsonify(clist)


# unique component list, each its max (highest) version number
# http://127.0.0.1:5000/cmax
@app.route('/cmax', methods=['GET'])
def cmax():
    cquery = Component.query.all()

    clist = []
    for c in cquery:
        clist.append({'name': c.name,
                      'version': c.version})

    # sort by name, which groups them together
    clist_sorted = sorted(clist, key=lambda x: x['name'])

    # sort name group by version, then append one with max version
    clist_version_max = []
    for k, g in groupby(clist_sorted, lambda x: x['name']):
        clist_version_max.append(max(g, key=lambda x: x['version']))

    return jsonify(clist_version_max)


# Get a list of all component names, unique name
# http://127.0.0.1:5000/cname
@app.route('/cname', methods=['GET'])
def cname():
    cquery = Component.query.all()

    cset = set()
    for c in cquery:
        cset.add(c.name)
    cname_list = sorted(list(cset))

    return jsonify(cname_list)


# Get a list of versions for a specific component
# http://127.0.0.1:5000/cversion
@app.route('/cversion', methods=['POST'])
def cversion():
    """
    cversion is POST. request body example: {"name": "component_name"}
    :return:
    """
    req_data = request.get_json()  # <class 'dict'>
    logging.debug("req_data = " + str(req_data))
    name = req_data['name']

    cquery = Component.query.filter_by(name=name).all()

    clist = []
    for c in cquery:
        clist.append({'name': c.name,
                      'version': c.version})

    cversion_sorted = sorted(clist, key=lambda x: x['name'])

    return jsonify(cversion_sorted)


# rename to c_sr
# Get a list of software releases associated with a component
# http://127.0.0.1:5000/csearchsr
@app.route('/csearchsr', methods=['POST'])
def csearchsr():
    """
    csearchsr is POST. request body example: {"name": "component_name", "version": "v"}
    :return:
    """
    req_data = request.get_json()  # <class 'dict'>
    logging.debug("req_data = " + str(req_data))

    name = req_data['name']
    version = req_data['version']

    component = Component.query.filter_by(name=name, version=version).first()
    c_sr_association = component.software_releases

    srlist = []
    for a in c_sr_association:
        srlist.append({'product_name': a.software_release.product_name,
                       'version_number': a.software_release.version_number})

    return jsonify(srlist)


# http://127.0.0.1:5000/p
@app.route('/p', methods=['GET'])
def p():
    pquery = Product.query.all()

    plist = []
    for p in pquery:
        plist.append({"name": p.name})

    return jsonify(plist)


# http://127.0.0.1:5000/pnew
@app.route('/pnew', methods=['POST'])
def pnew():
    req_data = request.get_json()
    logging.debug("req_data = " + str(req_data))

    name = req_data['name']

    return_code = {"name": "Error"}

    try:
        p_new = Product(name=name)
        db.session.add(p_new)
        db.session.commit()
        return_code['name'] = "Success"
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
        return jsonify(return_code)


# http://127.0.0.1:5000/pdelete
@app.route('/pdelete', methods=['POST'])
def pdelete():
    req_data = request.get_json()
    logging.debug("req_data = " + str(req_data))

    name = req_data['name']

    return_code = {"name": "Error"}

    try:
        p_delete = Product.query.filter_by(name=name).first()
        db.session.delete(p_delete)
        db.session.commit()
        return_code['name'] = "Success"
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
        return jsonify(return_code)


# http://127.0.0.1:5000/pedit
@app.route('/pedit', methods=['POST'])
def pedit():
    req_data = request.get_json()
    logging.debug("req_data = " + str(req_data))

    name = req_data['name']
    field = req_data['field']
    value = req_data['value']

    return_code = {"name": "Error"}

    try:
        # p_delete = Product.query.filter_by(name=name).first()
        # db.session.delete(p_delete)
        p_edit = Product.query.filter_by(name=name).first()
        exec("p_edit." + field + " = '" + value + "'")  # p_edit.field = 'value'
        db.session.commit()
        return_code['name'] = "Success"
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
        return jsonify(return_code)


# software release all
# http://127.0.0.1:5000/sr
@app.route('/sr', methods=['GET'])
def sr():
    srquery = SoftwareRelease.query.all()

    srlist = []
    for sr in srquery:
        srlist.append(
            {'product_name': sr.product_name,
             'version_number': sr.version_number,
             'status': sr.status})

    return jsonify(srlist)


# http://127.0.0.1:5000/srnew
@app.route('/srnew', methods=['POST'])
def srnew():
    req_data = request.get_json()
    logging.debug("req_data = " + str(req_data))

    product_name = req_data['product_name']
    version_number = req_data['version_number']

    return_code = {"name": "Error"}

    try:
        sr_new = SoftwareRelease(product_name=product_name, version_number=version_number)
        db.session.add(sr_new)
        db.session.commit()
        return_code['name'] = "Success"
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
        return jsonify(return_code)


# http://127.0.0.1:5000/srdelete
@app.route('/srdelete', methods=['POST'])
def srdelete():
    req_data = request.get_json()
    logging.debug("req_data = " + str(req_data))

    product_name = req_data['product_name']
    version_number = req_data['version_number']

    return_code = {"name": "Error"}

    try:
        sr_delete = SoftwareRelease.query.filter_by(product_name=product_name, version_number=version_number).first()
        db.session.delete(sr_delete)
        db.session.commit()
        return_code['name'] = "Success"
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
        return jsonify(return_code)


# http://127.0.0.1:5000/sredit
@app.route('/sredit', methods=['POST'])
def sredit():
    req_data = request.get_json()
    logging.debug("req_data = " + str(req_data))

    product_name = req_data['product_name']
    version_number = req_data['version_number']
    field = req_data['field']
    value = req_data['value']

    return_code = {"name": "Error"}

    try:
        # p_delete = Product.query.filter_by(name=name).first()
        # db.session.delete(p_delete)
        sr_edit = SoftwareRelease.query.filter_by(product_name=product_name, version_number=version_number).first()
        exec("sr_edit." + field + " = '" + value + "'")  # sr_edit.field = 'value'
        db.session.commit()
        return_code['name'] = "Success"
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
        return jsonify(return_code)


# makes sr deep copy with different version. Copy and paste description from requirements
# sr name ver, sr ver => in dev
# http://127.0.0.1:5000/sr_copy
@app.route('/sr_copy', methods=['POST'])
def sr_copy():
    r"""

    Postman test

{
    "product_name": "p3",
    "version_number": "1",
    "version_number_new": "2",
}

    :return:
    """
    req_data = request.get_json()
    logging.debug("req_data = " + str(req_data))

    product_name = req_data['product_name']
    version_number = req_data['version_number']
    version_number_new = req_data['version_number_new']

    return_code = {"name": "Error"}

    try:
        # create new association
        sr = SoftwareRelease.query.filter_by(product_name=product_name, version_number=version_number).first()

        sr_new = SoftwareRelease(product_name=product_name, version_number=version_number_new)
        db.session.add(sr_new)

        # extract components to list, and add components based on list
        for a in sr.components:
            a_new = Association(destination=a.destination)
            a_new.component = a.component
            sr_new.components.append(a_new)

        db.session.commit()
        return_code['name'] = "Success"
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
        return jsonify(return_code)


# {"product_name": "p1", "version_number": "1"}
# sr c list
# http://127.0.0.1:5000/sr_c
@app.route('/sr_c', methods=['POST'])
def sr_c():
    req_data = request.get_json()
    logging.debug("req_data = " + str(req_data))

    product_name = req_data['product_name']
    version_number = req_data['version_number']

    sr = SoftwareRelease.query.filter_by(product_name=product_name, version_number=version_number).first()

    sr_clist = []

    if sr is not None:  # must check if sr is not NoneType
        for a in sr.components:
            sr_clist.append({'name': a.component.name,
                             'version': a.component.version,
                             'destination': a.destination})

    return jsonify(sr_clist)


# sr's c with current version highlight
# http://127.0.0.1:5000/sr_c_highlight
@app.route('/sr_c_highlight', methods=['POST'])
def sr_c_highlight():
    req_data = request.get_json()
    logging.debug("req_data = " + str(req_data))

    product_name = req_data['product_name']
    version_number = req_data['version_number']

    sr = SoftwareRelease.query.filter_by(product_name=product_name, version_number=version_number).first()

    sr_clist = []

    if sr is not None:  # must check if sr is not NoneType
        for a in sr.components:
            sr_clist.append({'name': a.component.name,
                             'version': a.component.version,
                             'destination': a.destination})
    else:
        return jsonify([])

    # from /cmax
    cquery = Component.query.all()

    clist = []
    for c in cquery:
        clist.append({'name': c.name,
                      'version': c.version})

    # sort by name, which groups them together
    clist_sorted = sorted(clist, key=lambda x: x['name'])

    # sort name group by version, then append one with max version
    clist_version_max = []
    for k, g in groupby(clist_sorted, lambda x: x['name']):
        clist_version_max.append(max(g, key=lambda x: x['version']))

    # { "c1" : "c1.highest_version", "c2" : "c2.highest_version", ... }
    clist_highlight = {}
    for c in clist_version_max:
        clist_highlight[str(c['name'])] = str(c['version'])

    for c in sr_clist:
        newest_version = clist_highlight[c['name']]
        if c['version'] < newest_version:
            c['newest_version'] = newest_version
        elif c['version'] == newest_version:
            c['newest_version'] = "This"
        else:
            c['newest_version'] = "Unknown"

    return jsonify(sr_clist)


# http://127.0.0.1:5000/sr_add_c
@app.route('/sr_add_c', methods=['POST'])
def sr_add_c():
    r"""

    Postman test

{
    "product_name": "p3",
    "version_number": "1",
    "name": "c2",
    "version": "1",
    "destination": "./dest2"
}

    :return:
    """
    req_data = request.get_json()
    logging.debug("req_data = " + str(req_data))

    product_name = req_data['product_name']
    version_number = req_data['version_number']
    name = req_data['name']
    version = req_data['version']
    destination = req_data['destination']

    return_code = {"name": "Error"}

    try:
        # create new association
        c = Component.query.filter_by(name=name, version=version).first()
        sr = SoftwareRelease.query.filter_by(product_name=product_name, version_number=version_number).first()

        a = Association(destination=destination)
        a.component = c
        sr.components.append(a)

        db.session.commit()
        return_code['name'] = "Success"
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
        return jsonify(return_code)


# sr name ver, c name ver URL ( selected from clist)
# http://127.0.0.1:5000/sr_remove_c
@app.route('/sr_remove_c', methods=['POST'])
def sr_remove_c():
    r"""

    Postman test

{
    "product_name": "p3",
    "version_number": "1",
    "name": "c2",
    "version": "1",
    "destination": "./dest2"
}

    :return:
    """
    req_data = request.get_json()
    logging.debug("req_data = " + str(req_data))

    product_name = req_data['product_name']
    version_number = req_data['version_number']
    name = req_data['name']
    version = req_data['version']
    destination = req_data['destination']

    return_code = {"name": "Error"}

    try:
        # create new association
        c_id = Component.query.filter_by(name=name, version=version).first().id
        sr_id = SoftwareRelease.query.filter_by(product_name=product_name, version_number=version_number).first().id
        a = Association.query.filter_by(software_release_id=sr_id, component_id=c_id, destination=destination).first()

        db.session.delete(a)

        db.session.commit()
        return_code['name'] = "Success"
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
        return jsonify(return_code)


# complete recipe list for cli
# take sr name ver, return full json recipe
# http://127.0.0.1:5000/recipe
@app.route('/recipe', methods=['POST'])
def recipe():
    """
    {
    "product_name": "p2",
    "version_number": "3"
    }

    :return: recipe json
    """
    req_data = request.get_json()
    logging.debug("req_data = " + str(req_data))

    product_name = req_data['product_name']
    version_number = req_data['version_number']

    sr = SoftwareRelease.query.filter_by(product_name=product_name, version_number=version_number).first()

    clist = []
    for a in sr.components:
        clist.append({'name': a.component.name,
                      'version': a.component.version,
                      'destination': a.destination})

    recipe = {'product_name': sr.product_name,
              'version_number': sr.version_number,
              'status': sr.status,
              'components': clist}

    return jsonify(recipe)


@app.route('/5', methods=['POST', 'GET'])
def f5():
    if request.method == 'POST':
        logging.debug("request.data = " + str(request.data))
        logging.debug("request.get_json() = " + str(request.get_json()))
        return jsonify(request.get_json())
    return "f5"


if __name__ == '__main__':
    app.run()
