from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from apps.user.web import user_api_v1
from apps.area.web import area_api_v1
from apps.machine.web import machine_api_v1
from apps.job_role.web import job_role_api_v1

# Necessário para a criaçao dos schemas
from apps.user.models import UserModel
from apps.role.models import RoleModel
from apps.job_role.models import JobRoleModel
from apps.machine.models import MachineModel
from apps.area.models import AreaModel


def create_app():
    app = Flask(__name__)
    CORS(app)
    jwt = JWTManager(app)

    app.register_blueprint(user_api_v1)
    app.register_blueprint(area_api_v1)
    app.register_blueprint(machine_api_v1)
    app.register_blueprint(job_role_api_v1)

    return app
