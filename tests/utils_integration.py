from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

import unittest

from apps.user.web import user_api_v1


app = Flask(__name__)
app.config['TESTING'] = True
app.config['JWT_SECRET_KEY'] = 'secret_key_test'
CORS(app)
jwt = JWTManager(app)

app.register_blueprint(user_api_v1)

def signin_user(app):
    data = {
        'email': 'john@example.com',
        'password': '123'
    }
    response = app.post('/api/v1/user/signin', json=data)
    return response['token']


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_post_user(self):
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': '123',
            'windows_user': 'windows_user',
            'ip': '127.0.0.1',
            'machine_id': None,
            'area_id': 1,
            'role_id': 1,
            'job_role': 'Desenvolvedor'
        }
        response = self.app.post('/api/v1/user/signup', json=data)
        self.assertEqual(response.status_code, 200)

    def test_signin_user(self):
        data = {
            'email': 'john@example.com',
            'password': '123'
        }
        response = self.app.post('/api/v1/user/signin', json=data)
        self.assertEqual(response.status_code, 200)  

    def test_get_users(self):
        token = signin_user(self.app)
        response = self.app.get('/api/v1/user/', headers={'Authorization': f'{token}'})
        self.assertEqual(response.status_code, 200)

    def test_get_users_with_ip_and_windows_user(self):
        token = signin_user(self.app)
        response = self.app.get('/api/v1/user/configure', headers={'Authorization': f'{token}'})
        self.assertEqual(response.status_code, 200)

    def test_get_user(self):
        token = signin_user(self.app)
        response = self.app.get('/api/v1/user/john@example.com', headers={'Authorization': f'{token}'})
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        token = signin_user(self.app)
        data = {
            'name': 'John Doe',
            'new_email': 'new_email@example.com',
            'password': 'password',
            'windows_user': 'windows_user',
            'ip': '127.0.0.1',
            'machine_id': 'machine_id',
            'area_id': 1,
            'role_id': 'role_id',
            'job_role': 'job_role'
        }
        response = self.app.put('/api/v1/user/john@example.com', headers={'Authorization': f'{token}'}, json=data)
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        token = signin_user(self.app)
        response = self.app.delete('/api/v1/user/new_email@example.com', headers={'Authorization': f'{token}'})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
