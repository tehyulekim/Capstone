""r"""

using print() to debug because logging makes too many TypeError: not all arguments converted during string formatting

"""
from flask import Flask, request, render_template, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://yijwjkfpucdepl:76e1c9f816bb03c73393508f6dac75f411a56105e74c2b14ebd9a8fc87025788@ec2-54-221-214-3.compute-1.amazonaws.com:5432/del3ceijjamsso'

db = SQLAlchemy(app)

# from app import db, Association,Parent,Child
class Association(db.Model):
    __tablename__ = 'association'
    left_id = db.Column(db.Integer, db.ForeignKey('left.id'), primary_key=True)
    right_id = db.Column(db.Integer, db.ForeignKey('right.id'), primary_key=True)
    extra_data = db.Column(db.String(50))
    child = db.relationship("Child")


class Parent(db.Model):
    __tablename__ = 'left'
    id = db.Column(db.Integer, primary_key=True)
    children = db.relationship("Association")


class Child(db.Model):
    __tablename__ = 'right'
    id = db.Column(db.Integer, primary_key=True)


db.create_all()

r"""
from app import db, Softwarerelease,Component,Recipe


"""


# add component
# http://127.0.0.1:5000/a
@app.route('/a', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        component = json.loads(request.data)  # {'name': name, 'version': version} # <class 'dict'>

        return request.data

    return '/a page text message'


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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/1')
def f1():
    return render_template('page1.html')


@app.route('/2')
def f2():
    return render_template('page2.html')


@app.route('/3')
def f3():
    return render_template('page3.html')


@app.route('/4')
def f4():
    return render_template('page4.html')


@app.route('/5')
def f5():
    return alchemy.f1()


@app.route('/dbca')
def dbca():
    db.create_all()
    return 'db.create_all()'


if __name__ == '__main__':
    app.run()
