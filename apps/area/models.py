from ..sql_alchemy import db
from ..user.models import UserModel

class AreaModel(db.Model):
    __tablename__ = 'areas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    area_up_id = db.Column(db.Integer, db.ForeignKey('areas.id'))

    sub_areas = db.relationship('AreaModel', backref=db.backref('parent_area', remote_side=[id]))

    def __init__(self, name, area_up_id=None):
        self.name = name
        self.area_up_id = area_up_id

    @property
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'area_up_id': self.area_up_id,
        }

    @classmethod
    def get_areas(cls):
        return [area for area in cls.query.all()]

    @classmethod
    def get_areas_by_parent_id(cls, area_up_id):
        return [area for area in cls.query.filter_by(area_up_id=area_up_id).all()]
    
    @classmethod
    def get_areas_with_users(cls, area_up_id):
        areas = AreaModel.query.filter_by(area_up_id=area_up_id).all()
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

    def update_area(self, name, area_up_id):
        self.name = name
        self.area_up_id = area_up_id
        db.session.commit()

    def delete_area(self):
        db.session.delete(self)
        db.session.commit()
