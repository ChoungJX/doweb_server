from app.models import *
from app.Lib import uuid_generator, time_util

import flask_login


def login_as_user(username, password):
    get_user = User.query.filter_by(username=username).first()
    if get_user:
        if get_user.password == password:
            flask_login.login_user(get_user)
            new_login_history = LoginHistory(
                uuid_generator.create_new_uuid(),
                get_user.id,
                time_util.get_now()
            )
            db.session.add(new_login_history)
            db.session.commit()
            return True

    return False


def create_user(username, password, ifAdmin):
    get_user = User.query.filter_by(username=username).first()
    if get_user:
        return False

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
    flask_login.login_user(new_user)
    new_login_history = LoginHistory(
        uuid_generator.create_new_uuid(),
        new_user.id,
        time_util.get_now()
    )
    db.session.add(new_login_history)
    db.session.commit()
    return True


def create_user_nologin(username, password, ifAdmin):
    get_user = User.query.filter_by(username=username).first()
    if get_user:
        return False

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
    return True


def get_all_user():
    get_users = User.query.all()
    return_list = list()

    for i in get_users:
        return_list.append(
            {
                'id': i.id,
                'username': i.username,
                'ifadmin': i.root_number,
            }
        )
    return return_list


def ifCreated():
    hasUser = User.query.first()
    hasServer = Server.query.first()
    if hasUser and hasServer:
        return True
    else:
        return False


def ifCreatedUser():
    hasUser = User.query.first()
    if hasUser:
        return True
    else:
        return False


def remove_user(u_uuid):
    get_user = User.query.filter_by(id=u_uuid).first()
    if get_user:
        get_login_historys = LoginHistory.query.filter_by(u_id=u_uuid).all()
        for i in get_login_historys:
            db.session.delete(i)
        db.session.delete(get_user)
        db.session.commit()
        return 0
    return -1


def change_password(u_uuid, password):
    get_user = User.query.filter_by(id=u_uuid).first()
    get_user.password = password
    db.session.commit()


def create_server(server_ip, server_name, server_type, server_user, server_psw, server_ssh):
    new_server = Server(
        uuid_generator.create_new_uuid(),
        server_ip,
        server_name,
        server_type,
        server_user,
        server_psw,
        server_ssh
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


def get_server_by_id(server_id):
    get_server = Server.query.filter_by(id=server_id).first()
    return get_server


def create_certification():
    new_c = Certification(uuid_generator.create_new_uuid())
    db.session.add(new_c)
    db.session.commit()


def get_certification():
    get_c = Certification.query.first()
    return get_c.id
