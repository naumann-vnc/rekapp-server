from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from controller.users import User, Users


app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

CORS(app)

DATABASE_URI = 'postgresql+psycopg2://postgres:admin@localhost:5432/dbpython'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "Senai2022"


@app.before_first_request
def create_database():
    database.create_all()

api.add_resource(Users, '/users')
api.add_resource(User, '/users/<int:id>', '/users')


if __name__ == '__main__':
    from sql_alchemy import database
    database.init_app(app)
    app.run(host='172.31.95.196', port=8090, debug=True)
