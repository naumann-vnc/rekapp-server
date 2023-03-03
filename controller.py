from flask import Flask
from flask_restful import Api
from resources.movies import Movies, Movie
from resources.users import User, UserLogin
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import Column, Integer, String, create_engine, inspect, Sequence

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
jwt = JWTManager(app)

DATABASE_URI = 'postgresql+psycopg2://postgres:admin@localhost:5432/dbpython'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'Senai2022'
db = SQLAlchemy(app)

class Users(db.Model):
    user_id = db.Column(db.Integer, db.Sequence('my_table_id_seq'), primary_key=True)
    #name = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

@app.route('/register', methods=['POST'])
@cross_origin()

def register():
    engine = create_engine(DATABASE_URI)
    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    #if not database_exists(DATABASE_URI):
    create_database(DATABASE_URI)
    
    if 'users' not in table_names:
        db.Model.metadata.create_all(engine)

    data = request.get_json()
    #new_user = Users(user_id=data['user_id'], login=data['email'], password=data['password'])
    new_user = Users(login=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    db.session.close()
    return jsonify({'message': 'User registered successfully!'})

if __name__ == '__main__':
    #from sql_alchemy import database
    #database.init_app(app)
    app.run(host='172.31.95.196',port=8090,debug=True)

