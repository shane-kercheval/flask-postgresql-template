# run 'python -m unittest test_app.py'
# 'python -m unittest -v test_app.py' to produce more verbose output
# pep8 --first app.py
import pep8
import unittest
import logging
from sqlalchemy.exc import IntegrityError
from models import User
from app_factory import db, bcrypt


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

        assert user in db.session

        assert len(User.query.filter_by(email=email).all()) == 1
        user_from_db = User.get_user_by_email(email)
        assert user_from_db.email == email
        assert user_from_db.check_password(password)
        user_from_db.set_password("newpassword")
        db.session.commit()

        assert len(User.query.filter_by(email=email).all()) == 1
        user_from_db2 = User.get_user_by_email(email)
        assert user_from_db2.email == email
        assert user_from_db2.check_password("newpassword")

    def test_user_already_exists_raises_integrity_error(self):
        add_to_database(User(email='email', password='password'))
        l = lambda: add_to_database(User(email='email', password='another'))
        self.assertRaises(IntegrityError, l)

    def test_user_doesnt_exist_returns_none(self):
        user = User.get_user_by_email("bla")
        assert user is None

    def test_user_incorrect_password(self):
        email = 'email'
        password = 'password'
        add_to_database(User(email=email, password=password))
        user = User.get_user_by_email(email)
        assert user.password != password
        assert bcrypt.check_password_hash(user.password, password)


def add_to_database(object):
    db.session.add(object)
    db.session.commit()

if __name__ == '__main__':
    unittest.main()
