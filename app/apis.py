import json

from flask import jsonify
import requests


from app.Lib import uuid_generator
import app.sql


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


def get_server_info(request):
    data = app.sql.get_server_all()

    return jsonify(
        {
            "data": data,
        }
    )


def server_add(request):
    get_server_ip = request.json.get('server_ip')
    get_server_name = request.json.get('server_name')
    get_server_type = request.json.get('server_type')
    app.sql.create_server(get_server_ip, get_server_name, get_server_type)

    return jsonify(
        {
            'status': 0,
        }
    )


def server_delete(request):
    get_server_id = request.json.get('server_id')
    app.sql.remove_server(get_server_id)

    return jsonify(
        {
            'status': 0,
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


def get_containers_info(request):
    get_server_ip = request.json.get('server_ip')
    data = {
        'api': 'docker_socks',
        'url': '/containers/json?all=true',
        'method': 'GET',
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)
    return2json = json.loads(get_return.text)

    return jsonify(
        {
            "status": 0,
            'data': return2json,
        }
    )


def container_delete(request):
    get_id = request.json.get("container_id")
    get_server_ip = request.json.get("server_ip")

    data = {
        'api': 'docker_socks',
        'url': '/containers/%s?force=true' % (get_id),
        'method': "DELETE",
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)
    return2data = json.loads(get_return.text)
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
    get_server_ip = request.json.get("server_ip")

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
            "EndpointsConfig":get_network_model
        }
        

        # ===========================
    # ===============================

    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)
    return2data = json.loads(get_return.text)
    return jsonify(
        {
            'status': 0,
            'data': return2data,
        }
    )


def container_inpect(request):
    get_server_ip = request.json.get("server_ip")
    get_container_id = request.json.get("container_id")

    data = {
        'api': 'docker_socks',
        'psw': 'tttest',
        'method': "GET",
        'url': '/containers/%s/json' % (get_container_id)
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)
    return2json = json.loads(get_return.text)

    return jsonify(
        {
            'status': 0,
            'data': return2json
        }
    )


def server_network_info(request):
    get_server_ip = request.json.get("server_ip")

    data = {
        'api': 'docker_socks',
        'url': '/networks?dangling=true',
        'method': "GET",
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)

    return2json = json.loads(get_return.text)

    return jsonify(
        {
            'status': 0,
            "data": return2json
        }
    )


def container_process(request):
    get_server_ip = request.json.get("server_ip")
    get_container_id = request.json.get("container_id")

    data = {
        'api': 'docker_socks',
        'url': '/containers/%s/top' % (get_container_id),
        'method': "GET",
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)

    return2json = json.loads(get_return.text)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def container_log(request):
    get_server_ip = request.json.get("server_ip")
    get_container_id = request.json.get("container_id")

    data = {
        'api': 'docker_socks',
        'url': '/containers/%s/logs' % (get_container_id),
        'method': "GET",
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)

    return2json = json.loads(get_return.text)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def container_start(request):
    get_server_ip = request.json.get("server_ip")
    get_container_id = request.json.get("container_id")

    data = {
        'api': 'docker_socks',
        'url': '/containers/%s/start' % (get_container_id),
        'method': "POST",
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)

    return2json = json.loads(get_return.text)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def container_restart(request):
    get_server_ip = request.json.get("server_ip")
    get_container_id = request.json.get("container_id")

    data = {
        'api': 'docker_socks',
        'url': '/containers/%s/restart' % (get_container_id),
        'method': "POST",
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)

    return2json = json.loads(get_return.text)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def container_stop(request):
    get_server_ip = request.json.get("server_ip")
    get_container_id = request.json.get("container_id")

    data = {
        'api': 'docker_socks',
        'url': '/containers/%s/stop' % (get_container_id),
        'method': "POST",
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)

    return2json = json.loads(get_return.text)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def container_rename(request):
    get_server_ip = request.json.get("server_ip")
    get_container_id = request.json.get("container_id")
    get_container_name = request.json.get("container_name")

    data = {
        'api': 'docker_socks',
        'url': '/containers/%s/rename?name=%s' % (get_container_id, get_container_name),
        'method': "POST",
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)

    return2json = json.loads(get_return.text)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def container_delete_stoped(request):
    get_server_ip = request.json.get("server_ip")

    data = {
        'api': 'docker_socks',
        'url': '/containers/prune',
        'method': "POST",
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)

    return2json = json.loads(get_return.text)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def image_info(request):
    get_server_ip = request.json.get("server_ip")

    data = {
        'api': 'docker_socks',
        'url': '/images/json',
        'method': "GET",
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)

    return2json = json.loads(get_return.text)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def image_delete_cache(request):
    get_server_ip = request.json.get("server_ip")

    data = {
        'api': 'docker_socks',
        'url': "/build/prune",
        'method': "POST",
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)

    return2json = json.loads(get_return.text)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def image_pull(request):
    get_server_ip = request.json.get("server_ip")
    get_image_name = request.json.get("image_name")

    data = {
        'api': 'docker_socks',
        'url': "/images/create?fromImage=%s" % (get_image_name),
        'method': "POST",
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)

    return2json = json.loads(get_return.text)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def image_inspect(request):
    get_server_ip = request.json.get("server_ip")
    get_image_id = request.json.get("image_id")

    data = {
        'api': 'docker_socks',
        'url': "/images/%s/json" % (get_image_id),
        'method': "GET",
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)

    return2json = json.loads(get_return.text)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def image_delele(request):
    get_server_ip = request.json.get("server_ip")
    get_image_id = request.json.get("image_id")

    data = {
        'api': 'docker_socks',
        'url': "/images/%s?force=true" % (get_image_id),
        'method': "DELETE",
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)

    return2json = json.loads(get_return.text)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def image_create_from_container(request):
    send_url = "/commit"
    # ======接收参数参数========
    get_server_ip = request.json.get("server_ip")

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
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)

    return2json = json.loads(get_return.text)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def network_inspect(request):
    get_server_ip = request.json.get("server_ip")
    get_network_id = request.json.get("network_id")

    data = {
        'api': 'docker_socks',
        'url': "/networks/%s" % (get_network_id),
        'method': "GET",
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)

    return2json = json.loads(get_return.text)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def network_delete(request):
    get_server_ip = request.json.get("server_ip")
    get_network_id = request.json.get("network_id")

    data = {
        'api': 'docker_socks',
        'url': "/networks/%s" % (get_network_id),
        'method': "DELETE",
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)

    return2json = json.loads(get_return.text)

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
    get_server_ip = request.json.get("server_ip")
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
        ipv4_config = {
            "Subnet": request.json.get("subnet"),
            "IPRange": request.json.get("ip_range"),
            "Gateway": request.json.get("gateway"),
        }
        data["data"]["IPAM"]["Config"].append(ipv4_config)
    # ===========================

    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)

    return2json = json.loads(get_return.text)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def network_connect_container(request):
    get_server_ip = request.json.get("server_ip")
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
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)

    return2json = json.loads(get_return.text)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def network_disconnect_container(request):
    get_server_ip = request.json.get("server_ip")
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
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)

    return2json = json.loads(get_return.text)

    return jsonify(
        {
            'status': 0,
            'data': return2json,
        }
    )


def volume_info(request):
    get_server_ip = request.json.get('server_ip')

    data = {
        'api': 'docker_socks',
        'url': '/volumes',
        'method': 'GET',
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)
    return2json = json.loads(get_return.text)

    return jsonify(
        {
            "status": 0,
            'data': return2json,
        }
    )


def volume_inspcet(request):
    get_server_ip = request.json.get('server_ip')
    get_volume_id = request.json.get('volume_id')

    data = {
        'api': 'docker_socks',
        'url': '/volumes/%s' % (get_volume_id),
        'method': 'GET',
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)
    return2json = json.loads(get_return.text)

    return jsonify(
        {
            "status": 0,
            'data': return2json,
        }
    )


def volume_delete(request):
    get_server_ip = request.json.get('server_ip')
    get_volume_id = request.json.get('volume_id')

    data = {
        'api': 'docker_socks',
        'url': '/volumes/%s' % (get_volume_id),
        'method': 'DELETE',
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)
    return2json = json.loads(get_return.text)

    return jsonify(
        {
            "status": 0,
            'data': return2json,
        }
    )


def volume_delete_unused(request):
    get_server_ip = request.json.get('server_ip')

    data = {
        'api': 'docker_socks',
        'url': '/volumes/prune',
        'method': 'POST',
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)
    return2json = json.loads(get_return.text)

    return jsonify(
        {
            "status": 0,
            'data': return2json,
        }
    )


def system_infomation(request):
    get_server_ip = request.json.get('server_ip')

    data = {
        'api': 'docker_socks',
        'url': '/info',
        'method': 'GET',
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)
    return2json = json.loads(get_return.text)

    return jsonify(
        {
            "status": 0,
            'data': return2json,
        }
    )


def system_version(request):
    get_server_ip = request.json.get('server_ip')

    data = {
        'api': 'docker_socks',
        'url': '/version',
        'method': 'GET',
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)
    return2json = json.loads(get_return.text)

    return jsonify(
        {
            "status": 0,
            'data': return2json,
        }
    )


def test(requests):
    aaa = requests.json

    import pdb
    pdb.set_trace()
