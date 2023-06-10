from ..sql_alchemy import db


class MachineModel(db.Model):
    __tablename__ = 'machines'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    receiver_ip = db.Column(db.String(255), nullable=False)
    receiver_port = db.Column(db.Integer, nullable=False)
    package_capture_time = db.Column(db.Integer, nullable=False)
    package_capture_interval = db.Column(db.Integer, nullable=False)
    inactivity_threshold = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, receiver_ip, receiver_port, package_capture_time, package_capture_interval, inactivity_threshold):
        self.user_id = user_id
        self.receiver_ip = receiver_ip
        self.receiver_port = receiver_port
        self.package_capture_time = package_capture_time
        self.package_capture_interval = package_capture_interval
        self.inactivity_threshold = inactivity_threshold

    @property
    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'receiver_ip': self.receiver_ip,
            'receiver_port': self.receiver_port,
            'package_capture_time': self.package_capture_time,
            'package_capture_interval': self.package_capture_interval,
            'inactivity_threshold': self.inactivity_threshold,
        }

    @classmethod
    def get_machines(cls):
        return [machine for machine in cls.query.all()]

    @classmethod
    def find_machine_by_id(cls, id):
        return cls.query.filter_by(user_id=id).first()

    @classmethod
    def find_machine_by_ip(cls, receiver_ip):
        return cls.query.filter_by(receiver_ip=receiver_ip).first()

    def save_machine(self):
        db.session.add(self)
        db.session.commit()

    def update_machine(self, receiver_ip, receiver_port, package_capture_time, package_capture_interval, inactivity_threshold):
        self.receiver_ip = receiver_ip
        self.receiver_port = receiver_port
        self.package_capture_time = package_capture_time
        self.package_capture_interval = package_capture_interval
        self.inactivity_threshold = inactivity_threshold
        db.session.commit()

    def delete_machine(self):
        db.session.delete(self)
        db.session.commit()
