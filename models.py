from flask.ext.login import UserMixin
import app


class User(UserMixin, app.db.Model):
    __tablename__ = 'users'
    id = app.db.Column(app.db.Integer, primary_key=True)
    email = app.db.Column(app.db.String(), unique=True)
    password = app.db.Column(app.db.LargeBinary(255))

    def __init__(self, email, password):
        self.email = email
        self.password = app.bcrypt.generate_password_hash(password)

    def __repr__(self):
        return '<USER:email- {}>'.format(self.email)

    def set_password(self, password):
        self.password = app.bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return app.bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def get_user_by_email(email):
            return User.query.filter_by(email=email).first()
