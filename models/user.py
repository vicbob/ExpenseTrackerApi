from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20),unique = True, nullable=False)
    email = db.Column(db.String(40),unique = True,nullable=False)
    password = db.Column(db.String(30),nullable = False)
    expenses = db.relationship('ExpenseModel',lazy='dynamic')

    def __init__(self,username,password,email,**kwargs):
        super(**kwargs)
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return '<UserModel %r>' % self.username

    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username = username).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def json(self):
        return  {'username':self.username,
                 'email':self.email,
                 'expenses':[expense.json() for expense in self.expenses.all()]}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

