from sql_alchemy import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password


    def json(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
        }

    @classmethod
    def find_user_by_id(cls, id):
        user = cls.query.filter_by(id=id).first()
        if user:
            return user
        return None

    @classmethod  
    def find_user_by_email(cls, email): 
        user = cls.query.filter_by(email = email).first()
        if user:
            return user
        return None

    @classmethod
    def find_last_user(cls):
        user_id = db.session.query(cls).order_by(cls.id.desc()).first()
        if user_id:
            return user_id.id + 1
        return 1

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def update_user(self, email, password):
        self.email = email
        self.password = password

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
