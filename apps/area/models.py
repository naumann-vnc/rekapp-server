from ..sql_alchemy import db
from ..user.models import UserModel

class AreaModel(db.Model):
    __tablename__ = 'areas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    responsible_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, responsible_id):
        self.name = name
        self.responsible_id = responsible_id

    @property
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'responsible_id': self.responsible_id,
        }

    @classmethod
    def get_areas(cls):
        return [area for area in cls.query.all()]

    @classmethod
    def get_areas_by_responsible_id(cls, responsible_id):
        return [area for area in cls.query.filter_by(responsible_id=responsible_id).all()]
    
    @classmethod
    def get_areas_with_users(cls, responsible_id):
        areas = AreaModel.query.filter_by(responsible_id=responsible_id).all()
        areas_with_users = []

        for area in areas:
            users = UserModel.query.filter_by(area_id=area.id).all()
            users_data = [user.json for user in users]
            area_with_users = {
                'area': area.json,
                'users': users_data
            }
            areas_with_users.append(area_with_users)

        return areas_with_users

    @classmethod
    def find_area_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_area_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_area(self):
        db.session.add(self)
        db.session.commit()

    def update_area(self, name, responsible_id):
        self.name = name
        self.responsible_id = responsible_id
        db.session.commit()

    def delete_area(self):
        db.session.delete(self)
        db.session.commit()
