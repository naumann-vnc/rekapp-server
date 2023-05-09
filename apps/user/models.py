from ..sql_alchemy import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'))
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    job_role_id = db.Column(db.Integer, db.ForeignKey('job_roles.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, name, email, password, machine_id, area_id, role_id, job_role_id):
        self.name = name
        self.email = email
        self.password = password
        self.machine_id = machine_id
        self.area_id = area_id
        self.role_id = role_id
        self.job_role_id = job_role_id

    @property
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'machine_id': self.machine_id,
            'area_id': self.area_id,
            'role_id': self.role_id,
            'job_role_id': self.job_role_id
        }

    @classmethod
    def get_users(cls):
        return [user for user in cls.query.all()]

    @classmethod
    def find_user_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def update_user(self, name, email, password, machine_id, area_id, role_id, job_role_id):
        self.name = name
        self.email = email
        self.password = password
        self.machine_id = machine_id
        self.area_id = area_id
        self.role_id = role_id
        self.job_role_id = job_role_id
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
