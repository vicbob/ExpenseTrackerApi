from flask import Flask
from flask_jwt import JWT
from flask_cors import CORS
import config
from routes import routes
from security import authenticate, identity


def setup_app(_config):
    _app = Flask(__name__)
    _app.config.from_object(_config)
    db.init_app(_app)
    jwt = JWT(_app,authenticate,identity)
    routes(_app)
    CORS(_app)
    return _app

if __name__ == '__main__':
    from db import db
    app = setup_app(config.Config)

    @app.route("/")
    def hello():
        return "Hello World!"

    @app.before_first_request
    def create_db():
        print("I got here")
        db.create_all()

    app.run(debug=True)



