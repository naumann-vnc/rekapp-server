from flask import Blueprint, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import jwt_required

from http import HTTPStatus

from .controller import AreaController


area_api_v1 = Blueprint(
    'area_api_v1', 'area_api_v1', url_prefix='/api/v1/area')

CORS(area_api_v1)


@area_api_v1.route('/squads', methods=['GET'])
@jwt_required()
def api_get_areas():
    try:
        response, status = AreaController.get_areas()

        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@area_api_v1.route('/squads/<responsible_id>', methods=['GET'])
@jwt_required()
def api_get_areas_by_area_responsible_id(responsible_id):
    try:
        response, status = AreaController.get_areas_by_responsible(responsible_id)

        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@area_api_v1.route('/user/area/<responsible_id>', methods=['GET'])
@jwt_required()
def api_get_areas_with_users(responsible_id):
    try:
        response, status = AreaController.get_areas_with_users(responsible_id)

        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@area_api_v1.route('/<id>', methods=['GET'])
def api_get_area(id):
    try:
        response, status = AreaController.get_area_by_id(id)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@area_api_v1.route('/create', methods=['POST'])
@jwt_required()
def api_post_area():
    req = request.get_json()
    try:
        name = req.get('name')
        responsible_id = req.get('responsible_id')

        response, status = AreaController.add_area(name, responsible_id)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@area_api_v1.route('/<id>', methods=['PUT'])
def api_update_area(id):
    req = request.get_json()
    try:
        name = req.get('name')
        responsible_id = req.get('responsible_id')

        response, status = AreaController.update_area(id, name, responsible_id)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@area_api_v1.route('/<id>', methods=['DELETE'])
def api_delete_area(id):
    try:
        response, status = AreaController.delete_area(id)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST
