from app import app,sql
from flask import url_for, request, redirect, render_template, jsonify, current_app, make_response
import flask_login

from app import apis


@app.route('/welcome_api', methods=['POST'])
def welcome():
    pass




@app.route('/api', methods=['POST'])
def api():
    print(request.json)
    if request.json.get('api'):
        if flask_login.current_user.is_authenticated:
            callback = route_api.get(request.json.get('api'))
            return callback(request)
        else:
            callback = route_api_no_require_login.get(request.json.get('api'))
            return callback(request)

    return jsonify({"ststus": 0, "message": "no api"})


route_api_no_require_login = {
    'login': apis.login,
    "check_login": apis.check_login,
    'ifUsed': apis.ifUsed,
}

route_api = {
    "server_info": apis.get_server_info,  # 服务器集群信息
    "server_check": apis.server_check,
    "server_add": apis.server_add,
    "server_delete": apis.server_delete,
    "server_change_name": apis.server_change_name,

    'container_info': apis.get_containers_info,  # 服务器的所有容器信息
    'container_delete': apis.container_delete,  # 删除某一个容器
    'container_add': apis.container_add,  # 创建一个容器
    'container_inspect': apis.container_inpect,  # 获取一个容器的详细信息
    'container_process': apis.container_process,  # 容器的进程信息
    'container_log': apis.container_log,  # 容器的日志
    'container_start': apis.container_start,  # 启动容器
    'container_restart': apis.container_restart,  # 重启一个容器
    'container_stop': apis.container_stop,  # 停止一个容器
    'container_rename': apis.container_rename,  # 容器更名
    'container_delete_stoped': apis.container_delete_stoped,  # 删除已停止的容器

    'image_info': apis.image_info,  # 服务器的所有镜像信息
    'image_delete_cache': apis.image_delete_cache,  # 服务器镜像缓存删除
    'image_pull': apis.image_pull,  # 从dockerhub拉取一个镜像
    'image_inspect': apis.image_inspect,  # 获取一个镜像的详细信息
    'image_delele': apis.image_delele,  # 删除一个镜像
    'image_search:': '',  # 从dockerhub搜索镜像
    'image_create_from_container': apis.image_create_from_container,  # 将某个容器打包为镜像

    'network_info': apis.server_network_info,  # 服务器docker的网卡信息
    'network_inspect': apis.network_inspect,  # 查看某个网卡的关键信息
    "network_delete": apis.network_delete,  # 删除某个网卡
    'network_create': apis.network_create,  # 创建新网卡
    'network_connect_container': apis.network_connect_container,  # 为容器添加新网卡
    'network_disconnect_container': apis.network_disconnect_container,  # 移除某个容器的网卡

    'volume_info': apis.volume_info,  # 查看服务器所有卷信息
    'volume_inspcet': apis.volume_inspcet,  # 查看某个卷的详细信息
    'volume_delete': apis.volume_delete,  # 删除某个卷
    'volume_delete_unused': apis.volume_delete_unused,  # 删除未使用的卷

    'system_infomation': apis.system_infomation,  # 获取系统信息
    'system_version': apis.system_version,  # 获取系统版本信息

    'login': apis.login,
    "check_login": apis.check_login,


    'test': apis.test,
}
