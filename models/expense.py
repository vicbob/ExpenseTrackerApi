from db import db


class ExpenseModel(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer,primary_key=True )
    name = db.Column(db.String(30),nullable = False)
    price = db.Column(db.Float(2),nullable = False)
    date = db.Column(db.Date,nullable = False)
    category = db.Column(db.String(30))
    user_id= db.Column(db.Integer,db.ForeignKey('users.id'),nullable = False)

    def __init__(self,name,category,price,date,user_id):
        self.name = name
        self.category = category
        self.price = price
        self.date = date
        self.user_id = user_id

    @classmethod
    def find_by_date_range_and_user(cls,user,start_date):
        return cls.query.with_parent(user).filter(cls.date >= start_date).all()

    @classmethod
    def user_find_by_name_and_date(cls,current_user,name,date):
        return cls.query.with_parent(current_user).filter_by(name=name,date=date).first()

    def json(self):
        return {"name":self.name,"price":self.price,"date":self.date.strftime('%Y-%m-%d'),"category":self.category}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
