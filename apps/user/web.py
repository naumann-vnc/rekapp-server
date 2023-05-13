from flask import Blueprint, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import jwt_required

from http import HTTPStatus

from .controller import UserController, Login
from ..utils import expect


user_api_v1 = Blueprint(
    'auth_api_v1', 'auth_api_v1', url_prefix='/api/v1/user')

CORS(user_api_v1)


@user_api_v1.route('/', methods=['GET'])
@jwt_required()
def api_get_users():
    try:
        response, status = UserController.get_users()

        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST


@user_api_v1.route('/<email>', methods=['GET'])
def api_get_user(email):
    try:
        response, status = UserController.get_user_by_email(email)

        if response:
            return jsonify(response), status
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST


@user_api_v1.route('/signup', methods=['POST'])
def api_post_user():
    req = request.get_json()

    try:
        name = expect(req.get('name'), str, 'name')
        email = expect(req.get('email'), str, 'email')
        password = req.get('password')
        machine_id = req.get('machine_id')
        area_id = req.get('area_id')
        role_id = req.get('role_id')
        job_role = expect(req.get('job_role'), str, 'job_role')

        response, status = UserController.add_user(
            name=name,
            email=email,
            password=password,
            machine_id=machine_id,
            area_id=area_id,
            role_id=role_id,
            job_role=job_role
        )

        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST


@user_api_v1.route('/<email>', methods=['PUT'])
# @jwt_required()
def api_update_user(email):
    req = request.get_json()

    try:
        name = expect(req.get('name'), str, 'name')
        new_email = expect(req.get('new_email'), str, 'new_email')
        password = req.get('password')
        machine_id = req.get('machine_id')
        area_id = expect(req.get('area_id'), int, 'area_id')
        role_id = req.get('role_id')
        job_role = expect(req.get('job_role'), str, 'job_role')

        response, status = UserController.update_user(
            email=email,
            name=name,
            new_email=new_email,
            password=password,
            machine_id=machine_id,
            area_id=area_id,
            role_id=role_id,
            job_role=job_role
        )

        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST


@user_api_v1.route('/<email>', methods=['DELETE'])
#@jwt_required()
def api_delete_user(email):
    try:
        response, status = UserController.delete_user(email)

        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST


@user_api_v1.route('/signin', methods=['POST'])
def api_signin_user():
    req = request.get_json()

    try:
        email = expect(req.get('email'), str, 'email')
        password = expect(req.get('password'), str, 'password')

        response, status = Login.login(email, password)

        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST
