""r"""

"""
import os
import logging
from itertools import groupby
from pathlib import Path

from flask import Flask, request, jsonify, redirect, flash, url_for, render_template, abort, g
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, ALL, configure_uploads
from sqlalchemy import func

logging.basicConfig(level=logging.DEBUG)  # com ment out to turn off info messages

UPLOADED_ALL_DEST = 'static/uploads/'

app = Flask(__name__)
app.secret_key = b'secret_key'

app.config['UPLOADED_ALL_DEST'] = UPLOADED_ALL_DEST
files = UploadSet('files', extensions=ALL, default_dest=lambda x: UPLOADED_ALL_DEST)
configure_uploads(app, (files,))

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


@app.route('/')
def index():
    # Must force hard reload in browser CTRL+F5 update static files
    return redirect("static/index.html")


# view all with JSONView on Chrome for debugging
# http://127.0.0.1:5000/v
@app.route('/v', methods=['GET'])
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
        clist.append({'id': c.id,
                      'name': c.name,
                      'version': c.version})

    return jsonify(clist)


# unique component list, each its max (highest) version number. Not used
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


# Get a list of software releases associated with a component
# http://127.0.0.1:5000/csearchsr
@app.route('/c_sr', methods=['POST'])
def c_sr():
    """
    :return:
    """
    req_data = request.get_json()  # <class 'dict'>
    logging.debug("req_data = " + str(req_data))

    id = req_data['id']

    component = Component.query.filter_by(id=id).first()
    c_sr_association = component.software_releases

    srlist = []
    for a in c_sr_association:
        srlist.append({
            'id': a.software_release.id,
            'product_name': a.software_release.product_name,
            'version_number': a.software_release.version_number,
            'status': a.software_release.status})

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
            {
                'id': sr.id,
                'product_name': sr.product_name,
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


# http://127.0.0.1:5000/sr_c
@app.route('/sr_c', methods=['POST'])
def sr_c():
    """

    :return:
    """
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


# SR's components with newest version parameter. to be optimized
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

    for c in sr_clist:
        newest_version = db.session.query(func.max(Component.version)).filter_by(name=c['name']).first()[0]
        if c['version'] < newest_version:
            c['newest_version'] = newest_version
        else:
            c['newest_version'] = "This"

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

    if destination == "":
        destination = "."

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



# http://127.0.0.1:5000/sr_compare
@app.route('/sr_compare', methods=['POST'])
def sr_compare():

    req_data = request.get_json()
    logging.debug("req_data = " + str(req_data))

    product_name = req_data['product_name']
    version_number = req_data['version_number']
    product_name2 = req_data['product_name2']
    version_number2 = req_data['version_number2']

    sr = SoftwareRelease.query.filter_by(product_name=product_name, version_number=version_number).first()
    sr2 = SoftwareRelease.query.filter_by(product_name=product_name2, version_number=version_number2).first()


    sr_clist = []
    if sr is not None:  # must check if sr is not NoneType
        for a in sr.components:
            sr_clist.append({'name': a.component.name,
                             'version': a.component.version,
                             'destination': a.destination})
    
    sr2_clist = []
    if sr2 is not None:  # must check if sr2 is not NoneType
        for a in sr2.components:
            sr2_clist.append({'name': a.component.name,
                             'version': a.component.version,
                             'destination': a.destination})

    def compare(c1, c2):
        c2only = c2.copy()
        c1only = []
        cboth = []

        for c in c1:
            found = False
            for d in c2only:
                if c == d:
                    cboth.append(c)
                    c2only.remove(d)
                    found = True
                    break
            if not found:
                c1only.append(c)

        return (c1only, c2only, cboth)

    sr1only, sr2only, srboth = compare(sr_clist, sr2_clist)

    compare_data = {
        'sr1only': sr1only,
        'sr2only': sr2only,
        'srboth': srboth
    }

    return jsonify(compare_data)



# cli.py API

# add component
# http://127.0.0.1:5000/cli_add
@app.route('/cli_add', methods=['POST'])
def cli_add():
    component = request.get_json()  # <class 'dict'>
    name = component['name']
    version = component['version']

    # test with Postman {"name": "c1", "version": "1"}
    # query component
    query_component = db.session.query(Component).filter_by(name=name, version=version).first()

    # check if exist
    if query_component is not None:
        return "409 Conflict. Component already exists"

    # add component

    try:
        component_new = Component(name=name, version=version)
        db.session.add(component_new)
        db.session.commit()
        return "201 Created. Component is added"
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
        return "500 Unknown error"


# delete component in database, also deletes associated SR contents.
# http://127.0.0.1:5000/cli_delete_c
@app.route('/cli_delete_c', methods=['POST'])
def cli_delete_c():
    req_data = request.get_json()  # <class 'dict'>
    name = req_data['name']
    version = req_data['version']



    name_path = Path(name)  # converts name string to Path.  1/2/3/name  =>  1\2\3\name
    name_parent = name_path.parent  # parent directory    1\2\3
    name_name = name_path.name  # file name without parent directory.  name
    name_zip = name_name + "--v" + str(version) + ".zip"  # name--v1.2.3.4.zip
    name_path_zip = name_parent.joinpath(name_zip).as_posix()  # 1/2/3/name--v1.2.3.4.zip

    object_path = Path(UPLOADED_ALL_DEST + name_path_zip)

    component = Component.query.filter_by(name=name, version=version).first()

    return_code = {"name": "Error"}

    if component is not None:
        try:
            db.session.delete(component)
            db.session.commit()

            # also need to delete in Storage
            if object_path.exists():
                object_path.unlink()

            return_code['name'] = "Success"

        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()

    return jsonify(return_code)


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


# complete recipe list for cli
# take sr name ver, return full json recipe
# http://127.0.0.1:5000/cli_recipe
@app.route('/cli_recipe', methods=['POST'])
def cli_recipe():
    """
    {
    "product_name": "p2",
    "version_number": "3"
    }

    :return: recipe
    """
    req_data = request.get_json()
    logging.debug("req_data = " + str(req_data))

    product_name = req_data['product_name']
    version_number = req_data['version_number']

    if version_number is "":
        # get highest version number for recipe
        version_number = \
            db.session.query(func.max(SoftwareRelease.version_number)).filter_by(product_name=product_name).first()[0]

    sr = SoftwareRelease.query.filter_by(product_name=product_name, version_number=version_number).first()

    recipe = {'code': '404'}

    if sr is not None:  # must check if sr is not NoneType
        clist = []
        for a in sr.components:
            clist.append({'name': a.component.name,
                          'version': a.component.version,
                          'destination': a.destination})

        recipe = {
            'code': '200',
            'product_name': sr.product_name,
            'version_number': sr.version_number,
            'status': sr.status,
            'components': clist}

        return jsonify(recipe)

    else:
        return jsonify(recipe)


# http://127.0.0.1:5000/upload
@app.route('/upload', methods=['POST'])
def upload():
    logging.debug("request.form['file_name'] = " + str(request.form['file_name']))

    filename = files.save(request.files['file'], name=request.form['file_name'])
    return "uploaded to " + UPLOADED_ALL_DEST + filename


# http://127.0.0.1:5000/download
@app.route('/download', methods=['GET', 'POST'])
def download():
    req_data = request.get_data()
    logging.debug("request.form['file_name'] = " + str(request.form['file_name']))

    filename = files.save(request.files['file'], name=request.form['file_name'])
    return UPLOADED_ALL_DEST + filename


# return request json data. For testing
@app.route('/5', methods=['POST', 'GET'])
def f5():
    if request.method == 'POST':
        logging.debug("request.get_data() = " + str(request.get_data()))
        logging.debug("request.get_json() = " + str(request.get_json()))
        return jsonify(request.get_json())
    return "f5"


@app.route('/6', methods=['POST', 'GET'])
def f6():
    if request.method == 'POST':
        logging.debug("request.get_data() = " + str(request.get_data()))
        logging.debug("request.form['stnw'] = " + str(request.form['stnw']))
        return request.get_data()
    return "f6"


if __name__ == '__main__':
    app.run()
