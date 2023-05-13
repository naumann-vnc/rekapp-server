from flask_jwt_extended import create_access_token
import bcrypt

from http import HTTPStatus

from .models import UserModel


class UserController:
    @classmethod
    def get_users(cls):
        users = UserModel.get_users_without_role()
        users_json = [user.json for user in users]
        return users_json, HTTPStatus.OK

    @classmethod
    def get_user_by_email(cls, email):
        user = UserModel.find_user_by_email(email)
        if user:
            return user.json, HTTPStatus.OK
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

    @classmethod
    def add_user(cls, name, email, password, machine_id, area_id, role_id, job_role):
        user, status = cls.get_user_by_email(email)
        if status == HTTPStatus.OK:
            return {'message': f'User with email {email} already exists'}, HTTPStatus.UNAUTHORIZED

        hash_password = None
        if password:
            hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        new_user = UserModel(name=name, email=email, password=hash_password, machine_id=machine_id, area_id=area_id, role_id=role_id, job_role=job_role)

        try:
            new_user.save_user()
        except Exception as e:
            return {'message': 'An internal error occurred.'}, HTTPStatus.INTERNAL_SERVER_ERROR

        return new_user.json, HTTPStatus.CREATED

    @classmethod
    def update_user(cls, email, name, new_email, password, machine_id, area_id, role_id, job_role):
        user = UserModel.find_user_by_email(email)
        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        if new_email != email:
            new_email_user, status = cls.get_user_by_email(new_email)
            if status == HTTPStatus.OK:
                return {'message': f'Email {new_email} already exists'}, HTTPStatus.UNAUTHORIZED

        hash_password = None
        if password:
            hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user.name = name
        user.email = new_email
        user.password = hash_password
        user.machine_id = machine_id
        user.area_id = area_id
        user.role_id = role_id
        user.job_role = job_role
        user.save_user()

        return {'message': 'User updated successfully'}, HTTPStatus.OK

    @classmethod
    def delete_user(cls, email):
        user = UserModel.find_user_by_email(email)
        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        user_instance = UserModel.query.filter_by(email=email).first()
        user_instance.delete_user()

        return {'message': 'User deleted successfully'}, HTTPStatus.OK

class Login:
    @staticmethod
    def login(email, password):
        user, status = UserController.get_user_by_email(email)
        token = {}

        if status == HTTPStatus.OK and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            additional_claims = {
                'role': user.get('role_id'),
                'area_id': user.get('area_id')
            }

            token['token'] = create_access_token(identity=user['email'], additional_claims=additional_claims)
            return token, status

        return {'message': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED
