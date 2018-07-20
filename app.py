from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.users import UserRegister
from resources.climate import Climate, ClimateList, ClimatePredict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'pareto'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Climate, '/climate/<int:_id>')
api.add_resource(ClimateList, '/climate')
api.add_resource(ClimatePredict, '/climate/predict')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
