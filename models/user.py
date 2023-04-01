from sql_alchemy import database


class UserModel(database.Model):
    __tablename__ = 'users'
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(50))
    password = database.Column(database.String(255))
    created_at = database.Column(database.DateTime, server_default=database.func.now())
    updated_at = database.Column(database.DateTime, server_default=database.func.now(), server_onupdate=database.func.now())

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
        user_id = database.session.query(cls).order_by(cls.id.desc()).first()
        if user_id:
            return user_id.id + 1
        return 1

    def save_user(self):
        database.session.add(self)
        database.session.commit()

    def update_user(self, email, password):
        self.email = email
        self.password = password

    def delete_user(self):
        database.session.delete(self)
        database.session.commit()
