from http import HTTPStatus

from .models import AreaModel


class AreaController:
    @classmethod
    def get_areas(cls):
        areas = AreaModel.get_areas()
        areas_json = [area.json for area in areas]
        return areas_json, HTTPStatus.OK
    
    @classmethod
    def get_areas_by_responsible(cls, responsible_id):
        areas = AreaModel.get_areas_by_responsible_id(responsible_id)
        areas_json = [area.json for area in areas]
        return areas_json, HTTPStatus.OK
    
    @classmethod
    def get_areas_with_users(cls, responsible_id):
        area_with_users = AreaModel.get_areas_with_users(responsible_id)

        if area_with_users:
            return area_with_users, HTTPStatus.OK
        return {'message': 'Area not found'}, HTTPStatus.NOT_FOUND

    @classmethod
    def get_area_by_id(cls, id):
        area = AreaModel.find_area_by_id(id)
        if area:
            return area.json, HTTPStatus.OK
        return {'message': 'Area not found'}, HTTPStatus.NOT_FOUND

    @classmethod
    def add_area(cls, name, responsible_id):
        area = AreaModel.find_area_by_name(name)
        if area:
            return {'message': f'Area {name} already exists'}, HTTPStatus.UNAUTHORIZED

        new_area = AreaModel(name, responsible_id)

        try:
            new_area.save_area()
        except Exception:
            return {'message': 'An internal error occurred.'}, HTTPStatus.INTERNAL_SERVER_ERROR

        return new_area.json, HTTPStatus.CREATED

    @classmethod
    def update_area(cls, id, name, responsible_id):
        area = AreaModel.find_area_by_id(id)
        if not area:
            return {'message': 'Area not found'}, HTTPStatus.NOT_FOUND

        area.name = name
        area.responsible_id = responsible_id
        area.save_area()

        return {'message': 'Area updated successfully'}, HTTPStatus.OK

    @classmethod
    def delete_area(cls, id):
        area = AreaModel.find_area_by_id(id)
        if not area:
            return {'message': 'Area not found'}, HTTPStatus.NOT_FOUND

        area.delete_area()

        return {'message': 'Area deleted successfully'}, HTTPStatus.OK
