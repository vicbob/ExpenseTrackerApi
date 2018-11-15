from flask_restful import Api

from resources.expense import Expense
from resources.user import UserRegister, User, UserChangePassword, UserResetPassword


def routes(_app):
    api = Api(_app)
    api.add_resource(UserRegister,'/register')
    api.add_resource(User,'/user')
    api.add_resource(UserChangePassword,'/user/password-change')
    api.add_resource(Expense,'/user/expense')
    api.add_resource(UserResetPassword, '/user/password-reset/<email>')