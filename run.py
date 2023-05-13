import os
import configparser
import datetime

from apps.factory import create_app
from apps.sql_alchemy import db
from apps.role.models import RoleModel


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(os.path.abspath(os.path.join(".ini")))

    app = create_app()
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/rekapp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = '3Qv7SEEvX3TbkcNf'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=60)

    db.init_app(app)

    with app.app_context():
        db.create_all()

        if not RoleModel.get_roles():
            RoleModel.create_and_save_role('Admin')
            RoleModel.create_and_save_role('Manager')
            RoleModel.create_and_save_role('User')

    app.run()
