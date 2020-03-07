import json

from flask import jsonify
import requests

from app import app
from .Lib import uuid_generator


def check_status(data_dict):
    if data_dict.get("status") == 0:
        return True
    else:
        return False


def get_server_info(request):
    data = [
        {
            'id': uuid_generator.create_new_uuid(),
            'name': 'hk',
            'ip': '127.0.0.1'
        }
    ]

    return jsonify(
        {
            "data": data,
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
    get_id = request.json.get("id")
    get_server_ip = request.json.get("server_ip")

    data = {
        'api': 'docker_socks',
        'url': '/containers/%s?force=true' % (get_id),
        'method': "DELETE",
        'psw': 'tttest',
    }
    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)

    return jsonify(
        {
            'status': 0,
            'id': get_id,
        }
    )


def container_add(request):
    data = {
        'api':"docker_socks",
        'url':"/containers/create",
        "method": 'POST',
        'psw':"tttest",
        'data':dict(),
    }
    #===========get args============
    #选择的服务器
    get_server_ip = request.json.get("server_ip")

    
    #镜像
    get_image = request.json.get("image")
    if get_image:
        data["data"]["Image"] = get_image
    
    #名字
    get_name = request.json.get("name")
    if get_name:
        data["data"]["name"] = get_name

    #端口映射
    get_connect_port = request.json.get("connect_port")
    if get_connect_port:
        data["data"]["PortBindings"] = get_connect_port
    

        #========以下为高级设置=======
    #启动命令
    get_cmd = request.json.get("cmd")
    if get_cmd:
        data["data"]["Cmd"] = get_cmd
    
    #入口命令(代替Dockerfile)
    get_entrypoint = request.json.get("entrypoint")
    if get_entrypoint:
        data["data"]["Entrypoint"] = get_entrypoint
    
    #运行使用的用户
    get_user = request.json.get("user")
    if get_user:
        data["data"]['User'] = get_user
    
    #模拟终端
    get_tty = request.json.get("Tty")
    if get_tty:
        data["data"]["Tty"] = get_tty
    
    #交互模式
    get_interactive = request.json.get("interactive")
    if get_interactive:
        data["data"]["OpenStdin"] = get_interactive
    
    #工作目录
    get_workdir = request.json.get("workdir")
    if get_workdir:
        data["data"]["WorkingDir"] = get_workdir
    
    #网络配置
    get_network_model = request.json.get("network_model")
    if get_network_model:
        data["data"]["NetworkMode"] = get_network_model
        data["data"]["EndpointsConfig"] = request.json.get("network_config")
    else:
        data["data"]["NetworkMode"] = "bridge"

        #===========================
    #===============================

    get_return = requests.post('http://%s/server/api' %
                               (get_server_ip), json=data)
    import pdb; pdb.set_trace()


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

    return_data = list()
    for i in return2json['data']:
        try:
            temp_ip = ".".join(i.get("IPAM").get("Config")[0].get("Gateway").split('.')[:3])+"."
        except:
            temp_ip = "none"
        one_data = {
            'id': i.get('Id'),
            'name': i.get('Name'),
            'ip': temp_ip,
        }
        return_data.append(one_data)

    return jsonify(
        {
            'status': 0,
            "data": return_data
        }
    )


def test(requests):
    aaa = requests.json
    import pdb
    pdb.set_trace()
