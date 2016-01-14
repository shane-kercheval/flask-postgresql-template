# run 'python -m unittest test_app.py'
# 'python -m unittest -v test_app.py' to produce more verbose output
# pep8 --first app.py
import pep8
import unittest
import logging
from models import User
from app import db

class AppTest(unittest.TestCase):

    def setUp(self):
        db.session.close()
        db.drop_all()
        db.create_all()
        assert len(User.query.all()) == 0

    def tearDown(self):
        db.session.close()
        db.drop_all()
        db.create_all()
        assert len(User.query.all()) == 0

    def test_pep8(self):
        """Test that we conform to PEP8."""
        pep8style = pep8.StyleGuide()
        result = pep8style.check_files(['app.py'])
        self.assertEqual(result.total_errors, 0, "Found code style errors (and warnings).")

    def test_create_user(self):
        email = 'test_email'
        password = 'test_password'
        user = User(email=email, password=password)
        add_to_database(user)

        logging.info(user)
        #make sure user exists
        assert user in db.session

        users = User.get_user_by_email(email)
        assert len(users) == 1
        assert users[0].email == email
        assert users[0].password == password


def add_to_database(object):
    db.session.add(object)
    db.session.commit()

if __name__ == '__main__':
    unittest.main()