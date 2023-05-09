from flask import Blueprint, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import jwt_required

from http import HTTPStatus

from .controller import AreaController


area_api_v1 = Blueprint(
    'area_api_v1', 'area_api_v1', url_prefix='/api/v1/area')

CORS(area_api_v1)


@area_api_v1.route('/', methods=['GET'])
def api_get_areas():
    try:
        response, status = AreaController.get_areas()

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

@area_api_v1.route('/', methods=['POST'])
def api_post_area():
    req = request.get_json()
    try:
        name = req.get('name')
        area_up_id = req.get('area_up_id')

        response, status = AreaController.add_area(name, area_up_id)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@area_api_v1.route('/<id>', methods=['PUT'])
def api_update_area(id):
    req = request.get_json()
    try:
        name = req.get('name')
        area_up_id = req.get('area_up_id')

        response, status = AreaController.update_area(id, name, area_up_id)
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
