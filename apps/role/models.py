from ..sql_alchemy import db


class RoleModel(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        self.name = name

    @property
    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @classmethod
    def get_roles(cls):
        return [role.json for role in cls.query.all()]

    @classmethod
    def find_role_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_role_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def create_and_save_role(cls, name):
        role = cls(name=name)
        role.save_role()
        return role

    def save_role(self):
        db.session.add(self)
        db.session.commit()
