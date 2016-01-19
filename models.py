from flask.ext.login import UserMixin
from app_factory import db, bcrypt


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.LargeBinary(255))

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def __repr__(self):
        return '<USER:email- {}>'.format(self.email)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
