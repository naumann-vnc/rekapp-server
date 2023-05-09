from ..sql_alchemy import db


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
