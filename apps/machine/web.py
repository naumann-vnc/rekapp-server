from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_cors import CORS

from http import HTTPStatus

from .controller import MachineController


machine_api_v1 = Blueprint('machine_api_v1', 'machine_api_v1', url_prefix='/api/v1/machine')
CORS(machine_api_v1)


@machine_api_v1.route('/', methods=['GET'])
@jwt_required()
def api_get_machines():
    try:
        response, status = MachineController.get_machines()
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST


@machine_api_v1.route('/<id>', methods=['GET'])
@jwt_required()
def api_get_machine_by_id(id):
    try:
        response, status = MachineController.get_machine_by_id(id)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST


@machine_api_v1.route('/', methods=['POST'])
@jwt_required()
def api_add_machine():
    req = request.get_json()
    try:
        ip = req.get('ip')
        inventory = req.get('inventory')

        response, status = MachineController.add_machine(ip, inventory)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST


@machine_api_v1.route('/<id>', methods=['PUT'])
@jwt_required()
def api_update_machine(id):
    req = request.get_json()
    try:
        ip = req.get('ip')
        inventory = req.get('inventory')

        response, status = MachineController.update_machine(id, ip, inventory)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST


@machine_api_v1.route('/<id>', methods=['DELETE'])
@jwt_required()
def api_delete_machine(id):
    try:
        response, status = MachineController.delete_machine(id)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST
