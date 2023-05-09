from http import HTTPStatus

from .models import MachineModel


class MachineController:
    @classmethod
    def get_machines(cls):
        machines = MachineModel.get_machines()
        machines_json = [machine.json for machine in machines]
        return machines_json, HTTPStatus.OK

    @classmethod
    def get_machine_by_id(cls, id):
        machine = MachineModel.find_machine_by_id(id)
        if machine:
            return machine.json, HTTPStatus.OK
        return {'message': 'Machine not found'}, HTTPStatus.NOT_FOUND

    @classmethod
    def add_machine(cls, ip, inventory):
        machine = MachineModel.find_machine_by_ip(ip)
        if machine:
            return {'message': f'Machine with IP {ip} already exists'}, HTTPStatus.UNAUTHORIZED

        new_machine = MachineModel(ip, inventory)

        try:
            new_machine.save_machine()
        except Exception:
            return {'message': 'An internal error occurred.'}, HTTPStatus.INTERNAL_SERVER_ERROR

        return new_machine.json, HTTPStatus.CREATED

    @classmethod
    def update_machine(cls, id, ip, inventory):
        machine = MachineModel.find_machine_by_id(id)
        if not machine:
            return {'message': 'Machine not found'}, HTTPStatus.NOT_FOUND

        machine.update_machine(ip, inventory)

        return {'message': 'Machine updated successfully'}, HTTPStatus.OK

    @classmethod
    def delete_machine(cls, id):
        machine = MachineModel.find_machine_by_id(id)
        if not machine:
            return {'message': 'Machine not found'}, HTTPStatus.NOT_FOUND

        machine.delete_machine()

        return {'message': 'Machine deleted successfully'}, HTTPStatus.OK