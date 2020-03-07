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

    if check_status(return2json):
        page = request.json.get("page_current") - 1
        need_number = request.json.get("need")
        start = page*need_number
        need_data = return2json['data'][start:start+need_number]

        return_json = list()
        for i in need_data:
            one_data = {
                'id': i.get("Id"),
                'name': i.get("Names"),
                'ip': i.get('NetworkSettings').get('Networks').get('bridge').get('IPAddress'),
                'server_ip': get_server_ip,
                'status': i.get('Status'),
            }
            return_json.append(one_data)

        return jsonify(
            {
                "status": 0,
                'data': return_json,
                'total': len(return2json['data'])
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
    pass


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
