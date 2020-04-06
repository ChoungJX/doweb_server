import json
import base64

from flask import jsonify

import flask_login


from app.Lib import uuid_generator, send_request
import app.sql
from app.models import *


def login(request):
    get_username = request.json.get("username")
    get_password = request.json.get("password")

    if app.sql.login_as_user(get_username, get_password):
        return jsonify(
            {
                'status': 0
            }
        )
    else:
        return jsonify(
            {
                'status': -1
            }
        )


def check_login(request):
    if flask_login.current_user.is_authenticated:
        return jsonify(
            {
                "isLogin": True,
                "ifadmin": flask_login.current_user.root_number,
                "username": flask_login.current_user.username,
            }
        )
    else:
        return jsonify(
            {
                "isLogin": False
            }
        )


def logout(request):
    flask_login.logout_user()
    return jsonify({
        'status': 0
    })


def ifUsed(request):
    if app.sql.ifCreated():
        if flask_login.current_user.is_authenticated:
            return jsonify({
                "status": 1,
                "login": True,
            })
        else:
            return jsonify({
                "status": 1,
                "login": False,
            })
    else:
        return jsonify({
            "status": 0
        })


def get_server_info(request):
    data = app.sql.get_server_all()

    return jsonify(
        {
            "data": data,
        }
    )


def server_check(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    data = {
        'api': 'check_status',
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            'status': return2json.get("status")
        }
    )


def server_add(request):
    get_server_ip = request.json.get('server_ip')
    get_server_name = request.json.get('server_name')
    get_server_type = request.json.get('server_type')
    get_server_user = request.json.get('server_user')
    get_server_psw = request.json.get('server_psw')
    get_server_ssh = request.json.get('server_ssh_ip')

    return2json = send_request.send_request_server_bind(
        get_server_type, get_server_ip, {})

    if return2json.get("status") == 0:

        app.sql.create_server(get_server_ip, get_server_name,
                              get_server_type, get_server_user, get_server_psw, get_server_ssh)

        return jsonify(
            {
                'status': 0,
            }
        )
    else:
        return jsonify(
            {
                'status': -1,
                'message': return2json.get("message")
            }
        )


def server_delete(request):
    get_server_id = request.json.get('server_id')
    get_s = app.sql.get_server_by_id(get_server_id)
    return2json = send_request.send_request_server_delete(
        get_s.server_type, get_s.server_ip, {})

    if return2json.get("status") == 0:
        app.sql.remove_server(get_server_id)
        return jsonify(
            {
                'status': 0,
            }
        )
    else:
        return jsonify(
            {
                'status': -1,
                'message': return2json.get("message")
            }
        )


def server_change_name(request):
    get_server_id = request.json.get('server_id')
    get_server_name = request.json.get('server_name')
    app.sql.change_server_name(get_server_id, get_server_name)

    return jsonify(
        {
            'status': 0,
        }
    )


def server_change_ssh(request):
    get_server_id = request.json.get('server_id')
    get_server_ssh = request.json.get('server_ssh')
    get_s = Server.query.filter_by(id=get_server_id).first()
    get_s.server_ssh = get_server_ssh

    db.session.commit()
    return jsonify(
        {
            'status': 0,
        }
    )


def get_containers_info(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    data = {
        'api': 'docker_socks',
        'url': '/containers/json?all=true',
        'method': 'GET',
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            "status": 0,
            'data': return2json,
        }
    )


def container_delete(request):
    get_id = request.json.get("container_id")
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    data = {
        'api': 'docker_socks',
        'url': '/containers/%s?force=true' % (get_id),
        'method': "DELETE",
        'psw': 'tttest',
    }

    return2data = send_request.send_request(
        get_server_type, get_server_ip, data)
    return jsonify(
        {
            'status': 0,
            'id': get_id,
            'data': return2data,
        }
    )


def container_add(request):
    data = {
        'api': "docker_socks",
        'url': "/containers/create",
        "method": 'POST',
        'psw': "tttest",
        'data': dict(),
    }
    # ===========get args============
    # 选择的服务器
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    # 镜像
    get_image = request.json.get("image")
    if get_image:
        data["data"]["Image"] = get_image

    # 名字
    get_name = request.json.get("name")
    if get_name:
        data['url'] = "%s?name=%s" % (data['url'], get_name)

    # 端口映射
    get_connect_port = request.json.get("connect_port")
    get_export_port = request.json.get("export_port")
    if get_connect_port:
        data["data"]["HostConfig"] = {
            "PortBindings": get_connect_port
        }
        data["data"]["ExposedPorts"] = get_export_port
        # ========以下为高级设置=======
    # 启动命令
    get_cmd = request.json.get("cmd")
    if get_cmd:
        data["data"]["Cmd"] = get_cmd

    # 入口命令(代替Dockerfile)
    get_entrypoint = request.json.get("entrypoint")
    if get_entrypoint:
        data["data"]["Entrypoint"] = get_entrypoint

    # 运行使用的用户
    get_user = request.json.get("user")
    if get_user:
        data["data"]['User'] = get_user

    # 模拟终端
    get_tty = request.json.get("Tty")
    if get_tty:
        data["data"]["Tty"] = get_tty

    # 交互模式
    get_interactive = request.json.get("interactive")
    if get_interactive:
        data["data"]["OpenStdin"] = get_interactive

    # 工作目录
    get_workdir = request.json.get("workdir")
    if get_workdir:
        data["data"]["WorkingDir"] = get_workdir

    # 网络配置
    get_network_model = request.json.get("network_model")
    if get_network_model:
        data["data"]["NetworkingConfig"] = {
            "EndpointsConfig": get_network_model
        }

        # ===========================
    # ===============================

    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)
    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def container_inpect(request):
    get_container_id = request.json.get("container_id")
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    data = {
        'api': 'docker_socks',
        'psw': 'tttest',
        'method': "GET",
        'url': '/containers/%s/json' % (get_container_id)
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            'status': 0,
            'data': return2json
        }
    )


def server_network_info(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    data = {
        'api': 'docker_socks',
        'url': '/networks?dangling=true',
        'method': "GET",
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            'status': 0,
            "data": return2json
        }
    )


def container_process(request):
    get_container_id = request.json.get("container_id")
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    data = {
        'api': 'docker_socks',
        'url': '/containers/%s/top' % (get_container_id),
        'method': "GET",
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def container_log(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip
    get_container_id = request.json.get("container_id")

    data = {
        'api': 'docker_socks',
        'url': '/containers/%s/logs' % (get_container_id),
        'method': "GET",
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def container_start(request):
    get_container_id = request.json.get("container_id")
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    data = {
        'api': 'docker_socks',
        'url': '/containers/%s/start' % (get_container_id),
        'method': "POST",
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)
    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def container_restart(request):
    get_container_id = request.json.get("container_id")
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    data = {
        'api': 'docker_socks',
        'url': '/containers/%s/restart' % (get_container_id),
        'method': "POST",
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)
    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def container_stop(request):
    get_container_id = request.json.get("container_id")
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    data = {
        'api': 'docker_socks',
        'url': '/containers/%s/stop' % (get_container_id),
        'method': "POST",
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def container_rename(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    get_container_id = request.json.get("container_id")
    get_container_name = request.json.get("container_name")

    data = {
        'api': 'docker_socks',
        'url': '/containers/%s/rename?name=%s' % (get_container_id, get_container_name),
        'method': "POST",
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def container_delete_stoped(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    data = {
        'api': 'docker_socks',
        'url': '/containers/prune',
        'method': "POST",
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def image_info(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    data = {
        'api': 'docker_socks',
        'url': '/images/json',
        'method': "GET",
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def image_delete_cache(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    data = {
        'api': 'docker_socks',
        'url': "/build/prune",
        'method': "POST",
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def image_pull(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    get_image_name = request.json.get("image_name")
    if ":" not in get_image_name:
        get_image_name = "%s:latest"%(get_image_name)

    data = {
        'api': 'docker_socks',
        'url': "/images/create?fromImage=%s" % (get_image_name),
        'method': "POST",
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def image_inspect(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    get_image_id = request.json.get("image_id")

    data = {
        'api': 'docker_socks',
        'url': "/images/%s/json" % (get_image_id),
        'method': "GET",
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def image_delele(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    get_image_id = request.json.get("image_id")

    data = {
        'api': 'docker_socks',
        'url': "/images/%s?force=true" % (get_image_id),
        'method': "DELETE",
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def image_create_from_container(request):
    send_url = "/commit"
    # ======接收参数参数========
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    get_container_id = request.json.get("container_id")
    send_url = "%s?container=%s" % (send_url, get_container_id)

    get_image_name = request.json.get("image_name")
    send_url = "%s&repo=%s" % (send_url, get_image_name)
    # ========================

    data = {
        'api': 'docker_socks',
        'url': send_url,
        'method': "POST",
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def network_inspect(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    get_network_id = request.json.get("network_id")

    data = {
        'api': 'docker_socks',
        'url': "/networks/%s" % (get_network_id),
        'method': "GET",
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def network_delete(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    get_network_id = request.json.get("network_id")

    data = {
        'api': 'docker_socks',
        'url': "/networks/%s" % (get_network_id),
        'method': "DELETE",
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def network_create(request):
    data = {
        'api': 'docker_socks',
        'url': "/networks/create",
        'method': "POST",
        'psw': 'tttest',
        'data': dict()
    }

    # ========获取参数=============
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    data["data"]["EnableIPv6"] = False

    # 名字
    get_network_name = request.json.get("network_name")
    data["data"]["Name"] = get_network_name

    # 网卡类型
    get_network_drive = request.json.get("network_drive")
    data["data"]["Driver"] = get_network_drive

    # 网络配置
    if get_network_drive != "none":
        data["data"]["IPAM"] = {"Config": list()}
        ipv4_config = dict()
        if request.json.get("subnet"):
            ipv4_config["Subnet"] = request.json.get("subnet")
        if request.json.get("ip_range"):
            ipv4_config["IPRange"] = request.json.get("ip_range")
        if request.json.get("gateway"):
            ipv4_config["Gateway"] = request.json.get("gateway")
        data["data"]["IPAM"]["Config"].append(ipv4_config)

    # 选项
    if request.json.get("option"):
        data["data"]["Options"] = request.json.get("option")

    # ===========================

    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def network_connect_container(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    get_network_id = request.json.get("network_id")

    data = {
        'api': 'docker_socks',
        'url': "/networks/%s/connect" % (get_network_id),
        'method': "POST",
        'psw': 'tttest',
        'data': dict()
    }
    # ========获取参数=============
    # 容器id
    get_container_id = request.json.get("container_id")
    data["data"]["Container"] = get_container_id

    data["data"]["EndpointConfig"] = {
        "IPAMConfig": {
            "IPv4Address": request.json.get("network_ip")
        }
    }
    # ============================
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)
    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def network_disconnect_container(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    get_network_id = request.json.get("network_id")

    data = {
        'api': 'docker_socks',
        'url': "/networks/%s/disconnect" % (get_network_id),
        'method': "POST",
        'psw': 'tttest',
        'data': dict()
    }
    # ========获取参数=============
    # 容器id
    get_container_id = request.json.get("container_id")
    data["data"]["Container"] = get_container_id

    data["data"]["Force"] = True
    # ============================
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def volume_info(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    data = {
        'api': 'docker_socks',
        'url': '/volumes',
        'method': 'GET',
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            "status": 0,
            'data': return2json,
        }
    )


def volume_inspcet(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    get_volume_id = request.json.get('volume_id')

    data = {
        'api': 'docker_socks',
        'url': '/volumes/%s' % (get_volume_id),
        'method': 'GET',
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            "status": 0,
            'data': return2json,
        }
    )


def volume_delete(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    get_volume_id = request.json.get('volume_id')

    data = {
        'api': 'docker_socks',
        'url': '/volumes/%s' % (get_volume_id),
        'method': 'DELETE',
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            "status": 0,
            'data': return2json,
        }
    )


def volume_delete_unused(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    data = {
        'api': 'docker_socks',
        'url': '/volumes/prune',
        'method': 'POST',
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            "status": 0,
            'data': return2json,
        }
    )


def system_infomation(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    data = {
        'api': 'docker_socks',
        'url': '/info',
        'method': 'GET',
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            "status": 0,
            'data': return2json,
        }
    )


def system_version(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    data = {
        'api': 'docker_socks',
        'url': '/version',
        'method': 'GET',
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            "status": 0,
            'data': return2json,
        }
    )


def welcome_create_user(request):
    get_username = request.json.get("username")
    get_password = request.json.get("password")

    app.sql.create_certification()

    if app.sql.create_user(get_username, get_password, True):
        return jsonify({
            'status': 0
        })
    else:
        return jsonify({
            'status': -1
        })


def check_server_status(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    data = {
        'api': 'check_server_status',
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            "status": 0,
            'data': return2json,
        }
    )


def system_use(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_type = get_server.server_type
    get_server_ip = get_server.server_ip

    data = {
        'api': 'docker_socks',
        'url': "/system/df",
        'method': "GET",
        'psw': 'tttest',
    }
    return2json = send_request.send_request(
        get_server_type, get_server_ip, data)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def psw_check(request):
    return jsonify(
        {
            'id': app.sql.get_certification(),
            'status': 0
        }
    )


def user_info(request):
    return jsonify({
        'status': 0,
        'data': app.sql.get_all_user()
    })


def user_delete(request):
    c_u = flask_login.current_user.id
    get_uid = request.json.get("user_id")

    if c_u == get_uid:
        return jsonify({
            'status': 1
        })

    return jsonify({
        'status': app.sql.remove_user(get_uid)
    })


def user_create(request):
    get_username = request.json.get("username")
    get_password = request.json.get("password")
    get_admin = request.json.get("ifadmin")

    if get_admin:
        if app.sql.create_user_nologin(get_username, get_password, True):
            return jsonify({
                'status': 0
            })
        else:
            return jsonify({
                'status': -1
            })
    else:
        if app.sql.create_user_nologin(get_username, get_password, False):
            return jsonify({
                'status': 0
            })
        else:
            return jsonify({
                'status': -1
            })


def server_ssh_info(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_ip = get_server.server_ssh
    get_server_user = get_server.server_user
    get_server_psw = get_server.server_psw

    if request.json.get('base64'):
        get_server_psw = get_server_psw.encode()
        get_server_psw = base64.b64encode(get_server_psw).decode()

        return jsonify(
            {
                'status': 0,
                'data': {
                    'ip': get_server_ip,
                    'user': get_server_user,
                    'psw': get_server_psw,
                }
            }
        )
    else:
        if flask_login.current_user.root_number == "100":
            return jsonify(
                {
                    'status': 0,
                    'data': {
                        'ip': get_server_ip,
                        'user': get_server_user,
                        'psw': get_server_psw,
                    }
                }
            )
        else:
            return jsonify(
                {
                    'status': 0,
                    'data': {
                        'ip': get_server_ip,
                        'user': "暂无权限查看",
                        'psw': "暂无权限查看",
                    }
                }
            )


def server_one_info(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()
    get_server_ip = get_server.server_ip
    get_server_name = get_server.server_name

    return jsonify(
        {
            'status': 0,
            'name': get_server_name,
            'ip': get_server_ip
        }
    )


def server_change_user(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()

    get_server_user = request.json.get("server_user")
    get_server.server_user = get_server_user

    if flask_login.current_user.root_number == "100":
        db.session.commit()
        return jsonify({
            'status': 0,
        })
    else:
        return jsonify({
            'status': -1,
        })


def server_change_psw(request):
    get_server_id = request.json.get('server_id')
    get_server = Server.query.filter_by(id=get_server_id).first()

    get_server_psw = request.json.get("server_psw")
    get_server.server_psw = get_server_psw

    if flask_login.current_user.root_number == "100":
        db.session.commit()
        return jsonify({
            'status': 0,
        })
    else:
        return jsonify({
            'status': -1,
        })


def search_user_by_name(request):
    get_input = request.json.get("input")

    get_users = User.query.filter(
        User.username.like("%" + get_input +
                           "%") if get_input is not None else ""
    )

    return_list = list()
    for i in get_users:
        return_list.append(
            {
                "id": i.id,
                "name": i.username
            }
        )

    return jsonify({
        'status': 0,
        'data': return_list,
    })


def change_user(request):
    get_id = request.json.get("id")
    get_u = User.query.filter_by(id=get_id).first()

    get_username = request.json.get("username")
    get_password = request.json.get("password")
    get_admin = request.json.get("ifadmin")

    if get_username:
        if User.query.filter_by(username=get_username).first():
            return jsonify({
                'status': -1
            })
        else:
            get_u.username = get_username

    if get_password:
        get_u.password = get_password

    if get_admin:
        get_u.root_number = "100"
    else:
        get_u.root_number = "0"

    db.session.commit()
    return jsonify({
        'status': 0,
    })
