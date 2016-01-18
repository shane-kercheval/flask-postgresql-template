from models import User
from app_factory import db


def add_to_database(object):
    db.session.add(object)
    db.session.commit()

db.session.close()
db.drop_all()
db.create_all()

add_to_database(User(email='test_email', password='test_password'))
add_to_database(User(email='test@gmail.com', password='shane_password'))

