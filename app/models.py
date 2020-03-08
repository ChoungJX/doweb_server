from app import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(40), primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    root_number = db.Column(db.String(5))

    def __init__(self, get_id, username, password,root_number):
        self.id = get_id
        self.username = username
        self.password = password
        self.root_number = root_number

    def __repr__(self):
        return '<User %s>' % self.id

class Server(db.Model):
    __tablename__ = 'servers'
    id = db.Column(db.String(40), primary_key=True)
    server_name = db.Column(db.String(30))
    server_ip = db.Column(db.String(30))
    server_type = db.Column(db.String(30))

    def __init__(self, get_id, username, password, stype):
        self.id = get_id
        self.username = username
        self.password = password
        this.server_type = stype

    def __repr__(self):
        return '<User %s>' % self.id