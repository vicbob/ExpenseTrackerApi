from datetime import date, datetime

from flask_jwt import jwt_required, current_identity
from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp

from models.user import UserModel




class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="this field can not be blank")
    parser.add_argument("email", type=str, required=True, help="this field can not be blank")
    parser.add_argument("password", type=str, required=True, help="this field can not be blank")

    def post(self):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user:
            return {"message":"A user with that username already exists"},400

        user = UserModel.find_by_email(data['email'])
        if user:
            return {"message": "A user with that email already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {"message":"Successfully created user",'user':user.json()},201

class User(Resource):

    @jwt_required()
    def get(self):
        print(current_identity)
        return current_identity.json()

    @jwt_required()
    def delete(self):
        try:
            user = current_identity
            for expense in user.expenses:
                expense.delete_from_db()
            user.delete_from_db()
            return {"message":"Account deleted"}
        except:
            return {"message":"An error occured while deleting account"},500
       

class UserChangePassword(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('old_password',required =True, type=str, help="This field is required")
    parser.add_argument('new_password',required =True, type=str, help="This field is required")


    @jwt_required()
    def put(self):
        data = self.parser.parse_args()
        if (safe_str_cmp(data['old_password'],current_identity.password)):
            user = current_identity
            user.password = data['new_password']
            user.save_to_db()
            return {"message": "Password successfully updated"}

        return {"message":"Password is incorrect"},400


class UserResetPassword(Resource):

    def post(self,email):
        user = UserModel.find_by_email(email)
        if user:
            pass
            #to do
        pass