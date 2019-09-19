""""""r"""
https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/


"""
from app import db

db.create_all()


from app import User

admin = User(username='admin', email='admin@example.com')
guest = User(username='guest', email='guest@example.com')

db.session.add(admin)
db.session.add(guest)
db.session.commit()

User.query.all()
User.query.filter_by(username='admin').first()
