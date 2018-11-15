from datetime import timedelta


class Config(object):
    DEBUG = True
    BASE_URL = 'localhost:5000'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/expense_tracker_db'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'expensetrackerapi'
    JWT_AUTH_URL_RULE = '/login'
    JWT_EXPIRATION_DELTA = timedelta(hours=48)