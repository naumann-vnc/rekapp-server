from ..sql_alchemy import db


class JobRoleModel(db.Model):
    __tablename__ = 'job_roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, name):
        self.name = name

    @property
    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @classmethod
    def get_job_roles(cls):
        return [job_role for job_role in cls.query.all()]

    @classmethod
    def find_job_role_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_job_role_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_job_role(self):
        db.session.add(self)
        db.session.commit()

    def update_job_role(self, name):
        self.name = name
        db.session.commit()

    def delete_job_role(self):
        db.session.delete(self)
        db.session.commit()
