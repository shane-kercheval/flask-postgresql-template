from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    temp = db.Column(db.String())

    def get_user_by_email(email):
            return User.query.filter_by(email=email).all()

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<USER:email- {}>'.format(self.email)
