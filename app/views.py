from app import app
from flask import url_for, request, redirect, render_template, jsonify, current_app, make_response


from . import apis


@app.route('/api', methods=['POST'])
def api():
    print(request.json)
    if request.json.get('api'):
        callback = route_api.get(request.json.get('api'))
        return callback(request)

    return jsonify({"ststus": 0, "message": "no api"})


route_api = {
    "server_info": apis.get_server_info,
    'server_network_info':apis.server_network_info,

    'container_info': apis.get_containers_info,
    'container_delete': apis.container_delete,

    'test':apis.test,
}
