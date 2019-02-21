from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt import JWT

import config
from routes import routes
from security import authenticate, identity


def setup_app(_config):
    _app = Flask(__name__)
    _app.config.from_object(_config)
    db.init_app(_app)
    routes(_app)
    CORS(_app)
    return _app

    

if __name__ == '__main__':
    from db import db
    app = setup_app(config.Config)
    jwt = JWT(app, authenticate, identity)
    
    @app.route("/")
    def hello():
        return "Hello World!"

    @app.before_first_request
    def create_db():
        print("I got here")
        db.create_all()

    @jwt.auth_response_handler
    def customized_response_handler(access_token, identity):
        return jsonify({
            'access_token': access_token.decode('utf-8'),
            'username': identity.username
        })

    app.run(debug=True)
