from flask_jwt_extended import create_access_token
import bcrypt

from flask_restful import Resource, reqparse
from models.user import UserModel


minha_requisicao = reqparse.RequestParser()
minha_requisicao.add_argument('email', type=str, required=True, help="email is required")
minha_requisicao.add_argument('password', type=str, required=True, help="password is required")


class Users(Resource):
    def get(self):
        return [user.json() for user in UserModel.query.all()]


class User(Resource):
    minha_requisicao = reqparse.RequestParser()
    minha_requisicao.add_argument('email', type=str, required=True, help="email is required")
    minha_requisicao.add_argument('password', type=str, required=True, help="password is required")


    def get(self, id):
        user = UserModel.find_user_by_id(id)
        if user:
            return [user.json()]
        return {'message': 'user not found'}, 204

    def post(self):
        dados = User.minha_requisicao.parse_args()

        if UserModel.find_user_by_email(dados['email']):
            return {'message':'Login {} already exists'.format(dados['email'])}, 200

        user_id = UserModel.find_last_user()
        dados['password'] = bcrypt.hashpw(dados['password'].encode('utf-8'), bcrypt.gensalt())
        new_user = UserModel(user_id, **dados)

        try:
            new_user.save_user()
        except:
            return {'message': 'An internal error ocurred.'}, 500

        return new_user.json(), 201

    def put(self, id):
        dados = User.minha_requisicao.parse_args()
        user = UserModel.find_user_by_id(id)

        if user:
            user.update_user(**dados)
            user.save_user()
            return user.json(), 200

        user_id = UserModel.find_last_user()
        new_user = UserModel(user_id, **dados)
        new_user.save_user()
        return new_user.json(), 201

    def delete(self, id):
        user = UserModel.find_user_by_id(id)
        if user:
            user.delete_user()
            return {'message': 'User deleted.'}
        return {'message': 'User not founded'}, 204


class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = minha_requisicao.parse_args()
        user = UserModel.find_user_by_email(dados['email'])

        if user and bcrypt.checkpw(dados['password'].encode('utf-8'), user.password.encode('utf-8')):
            token_acesso = create_access_token(identity=user.id)
            return {'token': token_acesso}, 200
        return {'message': 'User or password is not correct.'}, 401
