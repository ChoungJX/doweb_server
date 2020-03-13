from app.models import *
from app.Lib import uuid_generator

import flask_login


def login_as_user(username, password):
    get_user = User.query.filter_by(username=username).first()
    if get_user:
        if get_user.password == password:
            flask_login.login_user(get_user)
            return True

    return False


def create_user(username, password, ifAdmin):
    if ifAdmin:
        new_user = User(
            uuid_generator.create_new_uuid(),
            username,
            password,
            "100"
        )
    else:
        new_user = User(
            uuid_generator.create_new_uuid(),
            username,
            password,
            "0"
        )

    db.session.add(new_user)
    db.session.commit()


def ifCreated():
    hasUser = User.query.first()
    if hasUser:
        return True
    else:
        return False


def remove_user(u_uuid):
    get_user = User.query.filter_by(id=u_uuid).first()
    db.session.delete(get_user)
    db.session.commit()


def change_password(u_uuid, password):
    get_user = User.query.filter_by(id=u_uuid).first()
    get_user.password = password
    db.session.commit()


def create_server(server_ip, server_name, server_type):
    new_server = Server(
        uuid_generator.create_new_uuid(),
        server_ip,
        server_name,
        server_type
    )
    db.session.add(new_server)
    db.session.commit()


def change_server_name(s_uuid, server_name):
    get_server = Server.query.filter_by(id=s_uuid).first()
    get_server.server_name = server_name
    db.session.commit()


def remove_server(s_uuid):
    get_server = Server.query.filter_by(id=s_uuid).first()
    db.session.delete(get_server)
    db.session.commit()


def get_server_all():
    get_servers = Server.query.all()

    return_list = list()
    for i in get_servers:
        one_data = {
            'id': i.id,
            'server_ip': i.server_ip,
            'server_name': i.server_name
        }
        return_list.append(one_data)

    return return_list


def get_server_by_server_ip(server_ip):
    get_server = Server.query.filter_by(id=s_uuid).first()
    return get_server


def create_certification():
    new_c = Certification(uuid_generator.create_new_uuid())
    db.session.add(new_c)
    db.session.commit()
