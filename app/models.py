from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(40), primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    root_number = db.Column(db.String(5))

    def __init__(self, get_id, username, password, root_number):
        self.id = get_id
        self.username = username
        self.password = password
        self.root_number = root_number

    def __repr__(self):
        return '<User %s>' % self.id


class LoginHistory(db.Model):
    __tablename__ = 'login_history'
    id = db.Column(db.String(40), primary_key=True)
    u_id = db.Column(db.String(40))
    login_time = db.Column(db.String(30))

    def __init__(self, get_id, get_uid, get_login_time):
        self.id = get_id
        self.u_id = get_uid
        self.login_time = get_login_time

    def __repr__(self):
        return '<LoginHistory %s>' % self.id


class Server(db.Model):
    __tablename__ = 'servers'
    id = db.Column(db.String(40), primary_key=True)
    server_name = db.Column(db.String(30))
    server_ip = db.Column(db.String(30))
    server_type = db.Column(db.String(30))
    server_user = db.Column(db.String(30))
    server_psw = db.Column(db.String(30))

    def __init__(self, get_id, server_ip, server_name, server_type, server_user, server_psw):
        self.id = get_id
        self.server_name = server_name
        self.server_ip = server_ip
        self.server_type = server_type
        self.server_user = server_user
        self.server_psw = server_psw

    def __repr__(self):
        return '<Server %s>' % self.id


class Certification(db.Model):
    __tablename__ = "certification"
    id = db.Column(db.String(40), primary_key=True)

    def __init__(self, get_id):
        self.id = get_id

    def __repr__(self):
        return '<Certification %s>' % (self.id)
