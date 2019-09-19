from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://yijwjkfpucdepl:76e1c9f816bb03c73393508f6dac75f411a56105e74c2b14ebd9a8fc87025788@ec2-54-221-214-3.compute-1.amazonaws.com:5432/del3ceijjamsso'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username







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


if __name__ == '__main__':
    app.run()
