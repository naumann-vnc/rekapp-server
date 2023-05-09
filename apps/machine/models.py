from ..sql_alchemy import db


class MachineModel(db.Model):
    __tablename__ = 'machines'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(255), nullable=False)
    inventory = db.Column(db.String(255))

    def __init__(self, ip, inventory):
        self.ip = ip
        self.inventory = inventory

    @property
    def json(self):
        return {
            'id': self.id,
            'ip': self.ip,
            'inventory': self.inventory,
        }

    @classmethod
    def get_machines(cls):
        return [machine for machine in cls.query.all()]

    @classmethod
    def find_machine_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_machine_by_ip(cls, ip):
        return cls.query.filter_by(ip=ip).first()

    def save_machine(self):
        db.session.add(self)
        db.session.commit()

    def update_machine(self, ip, inventory):
        self.ip = ip
        self.inventory = inventory
        db.session.commit()

    def delete_machine(self):
        db.session.delete(self)
        db.session.commit()
