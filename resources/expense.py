from datetime import date, datetime

from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse

from models.expense import ExpenseModel


class Expense(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name",type=str ,required=True,help="The name field is required")
    parser.add_argument("price",type=float ,required=True,help="The price field is required")
    parser.add_argument("category",type=str )

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()
        expense = ExpenseModel.user_find_by_name_and_date(current_identity,data['name'],date.today())
        if expense:
            return {"message":"Expense already exists for this date, modify the already existing expense"},400
        expense = ExpenseModel(date=date.today(),user_id=current_identity.id,**data)
        print(expense.json())
        print(current_identity.id)
        try:
            expense.save_to_db()
        except:
            return {'message':"An error occured while creating the expense"},500

        return {"message": "Expense successfully created"},201

    @jwt_required()
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("price", type=float, required=True, help="This field is required")
        parser.add_argument("name", type=str, required=True, help="This field is required")
        parser.add_argument("date", type=str, required=True, help="This field is required")
        parser.add_argument("category", type=str, help="This field is optional")
        data = parser.parse_args()
        expense = ExpenseModel.user_find_by_name_and_date(current_identity, data['name'], datetime.strptime(data['date'],"%Y-%m-%d").date())
        if not expense:
            return {"message":"The expense was not found"},400
        expense.price = data['price']
        expense.category = data['category']
        try:
            expense.save_to_db()
        except:
            return {'message': "An error occured while updating expense"},500

        return {'message': "Expense successfully updated",'expense':expense.json()}

    @jwt_required()
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("date", type=str, required=True, help="This field is required")
        parser.add_argument("name", type=str, required=True, help="This field is required")

        data = parser.parse_args()

        expense = ExpenseModel.user_find_by_name_and_date(current_identity,data['name'],datetime.strptime(data['date'],"%Y-%m-%d").date())
        if expense:
            expense.delete_from_db()
            return {"message":"expense successfully deleted"}
        return {"message":"expense not found in the database"},400

