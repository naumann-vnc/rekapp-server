from http import HTTPStatus

from .models import JobRoleModel


class JobRoleController:
    @classmethod
    def get_job_roles(cls):
        job_roles = JobRoleModel.get_job_roles()
        job_roles_json = [job_role.json for job_role in job_roles]
        return job_roles_json, HTTPStatus.OK

    @classmethod
    def get_job_role_by_id(cls, id):
        job_role = JobRoleModel.find_job_role_by_id(id)
        if job_role:
            return job_role.json, HTTPStatus.OK
        return {'message': 'Job role not found'}, HTTPStatus.NOT_FOUND

    @classmethod
    def get_job_role_by_name(cls, name):
        job_role = JobRoleModel.find_job_role_by_name(name)
        if job_role:
            return job_role.json, HTTPStatus.OK
        return {'message': 'Job role not found'}, HTTPStatus.NOT_FOUND

    @classmethod
    def add_job_role(cls, name):
        job_role = JobRoleModel.find_job_role_by_name(name)
        if job_role:
            return {'message': f'Job role {name} already exists'}, HTTPStatus.UNAUTHORIZED

        new_job_role = JobRoleModel(name)

        try:
            new_job_role.save_job_role()
        except Exception:
            return {'message': 'An internal error occurred.'}, HTTPStatus.INTERNAL_SERVER_ERROR

        return new_job_role.json, HTTPStatus.CREATED

    @classmethod
    def update_job_role(cls, id, name):
        job_role = JobRoleModel.find_job_role_by_id(id)
        if not job_role:
            return {'message': 'Job role not found'}, HTTPStatus.NOT_FOUND

        job_role.name = name
        job_role.update_job_role(name)

        return {'message': 'Job role updated successfully'}, HTTPStatus.OK

    @classmethod
    def delete_job_role(cls, id):
        job_role = JobRoleModel.find_job_role_by_id(id)
        if not job_role:
            return {'message': 'Job role not found'}, HTTPStatus.NOT_FOUND

        job_role.delete_job_role()

        return {'message': 'Job role deleted successfully'}, HTTPStatus.OK
