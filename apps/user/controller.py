from flask_jwt_extended import create_access_token
import bcrypt

import os
import json
import requests
from http import HTTPStatus

from .models import UserModel


class UserController:
    @classmethod
    def get_users(cls):
        users = UserModel.get_users_without_role()
        users_json = [user.json for user in users]
        return users_json, HTTPStatus.OK

    @classmethod
    def get_users_with_ip_and_windows_user(cls):
        users = UserModel.get_users_with_ip_and_windows_user()
        users_json = [{'ip': ip, 'windows_user': windows_user} for ip, windows_user in users]
        return users_json, HTTPStatus.OK

    @classmethod
    def get_user_by_email(cls, email):
        user = UserModel.find_user_by_email(email)
        if user:
            return user.json, HTTPStatus.OK
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

    @classmethod
    def get_user_by_windows_user(cls, windows_user):
        user = UserModel.find_user_by_windows_user(windows_user)
        if user:
            return user.json, HTTPStatus.OK
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

    @classmethod
    def add_user(cls, name, email, password, windows_user, ip, area_id, role_id, job_role, dashboard_uid):
        user, status = cls.get_user_by_email(email)
        if status == HTTPStatus.OK:
            return {'message': f'User with email {email} already exists'}, HTTPStatus.UNAUTHORIZED

        hash_password = None
        if password:
            hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        new_user = UserModel(name=name, email=email, password=hash_password, windows_user=windows_user, ip=ip, area_id=area_id, role_id=role_id, job_role=job_role, dashboard_uid=dashboard_uid)

        if not password:
            try:
                folder = Grafana.add_folder(name)
                dashboard = Grafana.add_dashboard(folder.get('uid'), windows_user)
                new_user.dashboard_uid = dashboard.get('uid')
            except Exception as e:
                return {'message': 'An internal error occurred.'}, HTTPStatus.INTERNAL_SERVER_ERROR

        try:
            user, status = cls.get_user_by_windows_user(windows_user)
            if status == HTTPStatus.OK:
                return cls.update_user_with_configure(name, email, password, windows_user, area_id, role_id, job_role, dashboard_uid=dashboard.get('uid'))

            new_user.save_user()
        except Exception as e:
            return {'message': 'An internal error occurred.'}, HTTPStatus.INTERNAL_SERVER_ERROR

        return new_user.json, HTTPStatus.CREATED

    @classmethod
    def add_configure(cls, name, email, password, windows_user, ip, area_id, role_id, job_role, dashboard_uid):
        user, status = cls.get_user_by_windows_user(windows_user)
        if status == HTTPStatus.OK:
            return {'message': f'User with user {windows_user} already exists'}, HTTPStatus.UNAUTHORIZED

        db_name = windows_user.replace(".", "")

        new_user = UserModel(name=name, email=email, password=password, windows_user=db_name, ip=ip, area_id=area_id, role_id=role_id, job_role=job_role, dashboard_uid=dashboard_uid)

        try:
            new_user.save_user()
        except Exception as e:
            return {'message': 'An internal error occurred.'}, HTTPStatus.INTERNAL_SERVER_ERROR

        return new_user.json, HTTPStatus.CREATED

    @classmethod
    def update_user(cls, email, name, new_email, password, windows_user, ip, area_id, role_id, job_role, dashboard_uid):
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
        user.windows_user = windows_user
        user.ip = ip
        user.area_id = area_id
        user.role_id = role_id
        user.job_role = job_role
        user.dashboard_uid = dashboard_uid
        user.save_user()

        return {'message': 'User updated successfully'}, HTTPStatus.OK

    @classmethod
    def update_user_with_configure(cls, name, new_email, password, windows_user, area_id, role_id, job_role, dashboard_uid):
        user = UserModel.find_user_by_windows_user(windows_user)

        user.name = name
        user.email = new_email
        user.password = password
        user.area_id = area_id
        user.role_id = role_id
        user.job_role = job_role
        user.dashboard_uid = dashboard_uid
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
                'id': user.get('id'),
                'name': user.get('name'),
                'job_role': user.get('job_role'),
                'role': user.get('role_id'),
                'area_id': user.get('area_id')
            }

            token['token'] = create_access_token(identity=user['email'], additional_claims=additional_claims)
            return token, status

        return {'message': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED


class Grafana:
    @staticmethod
    def add_folder(name):
        '''
            Após criar o usuário cria a pasta no grafana.
        '''
        url = "https://grafana.rekapp.net/api/folders"
        headers = {
            "Authorization": "Bearer eyJrIjoiVEU4Z05CNUxONHZPbkYyWXYyeFpJWFZSdFR0M2d1UnAiLCJuIjoiYXBpa2V5IiwiaWQiOjF9",
            "Content-Type": "application/json"
        }
        data = {
            "title": name
        }

        response_folder = requests.post(url, headers=headers, json=data)
        return response_folder.json()
    
    @staticmethod
    def add_dashboard(uid, windows_user):
        '''
            Cria o dashboard na folder com o uid da pasta.
        '''
        dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(dir, "template_grafana.json")
        if os.path.exists(path):
            with open(path, "r") as file:
                grafana_body = json.load(file)

        url = "https://grafana.rekapp.net/api/dashboards/db"
        headers = {
            "Authorization": "Bearer eyJrIjoiVEU4Z05CNUxONHZPbkYyWXYyeFpJWFZSdFR0M2d1UnAiLCJuIjoiYXBpa2V5IiwiaWQiOjF9",
            "Content-Type": "application/json"
        }

        grafana_body['folderUid'] = uid
        grafana_body['dashboard']['title'] = windows_user
        for target in grafana_body['dashboard']['panels']:
            if 'nedic' in target['targets'][0]['target']:
                new_target = target['targets'][0]['target']
                target['targets'][0]['target'] = new_target.replace('windows_user', windows_user)

        response_folder = requests.post(url, headers=headers, json=grafana_body)
        return response_folder.json()
