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
    def add_machine(cls, user_id, receiver_ip, receiver_port, package_capture_time, package_capture_interval, inactivity_threshold):
        machine = MachineModel.find_machine_by_id(user_id)
        if machine:
            machine.update_machine(receiver_ip, receiver_port, package_capture_time, package_capture_interval, inactivity_threshold)
            return {'message': 'Machine updated successfully'}, HTTPStatus.OK

        new_machine = MachineModel(user_id, receiver_ip, receiver_port, package_capture_time, package_capture_interval, inactivity_threshold)

        try:
            new_machine.save_machine()
        except Exception:
            return {'message': 'An internal error occurred.'}, HTTPStatus.INTERNAL_SERVER_ERROR

        return new_machine.json, HTTPStatus.CREATED

    @classmethod
    def delete_machine(cls, id):
        machine = MachineModel.find_machine_by_id(id)
        if not machine:
            return {'message': 'Machine not found'}, HTTPStatus.NOT_FOUND

        machine.delete_machine()

        return {'message': 'Machine deleted successfully'}, HTTPStatus.OK
