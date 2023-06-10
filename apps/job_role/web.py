from flask import Blueprint, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import jwt_required

from http import HTTPStatus

from .controller import JobRoleController
from ..utils import expect


job_role_api_v1 = Blueprint(
    'job_role_api_v1', 'job_role_api_v1', url_prefix='/api/v1/job_role')

CORS(job_role_api_v1)


@job_role_api_v1.route('/', methods=['GET'])
def api_get_job_roles():
    try:
        response, status = JobRoleController.get_job_roles()

        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST


@job_role_api_v1.route('/', methods=['POST'])
def api_add_job_role():
    req = request.get_json()
    try:
        name = req.get('name')
        if not name:
            return jsonify({'error': 'Missing required parameter: name'}), HTTPStatus.BAD_REQUEST

        job_role, status = JobRoleController.add_job_role(name)
        return jsonify(job_role), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST
