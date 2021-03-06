from app import app, sql
from flask import url_for, request, redirect, render_template, jsonify, current_app, make_response
import flask_login

from app import apis


@app.route('/version')
def version():
    return jsonify({
        "status": 0,
        "version": ""
    })


@app.route('/welcome_api', methods=['POST'])
def welcome():
    if sql.ifCreatedUser():
        return jsonify({
            "status": -2,
            'message': "this server has binded!"
        })
    else:
        if request.json.get('api'):
            callback = welcome_route_api.get(request.json.get('api'))
            return callback(request)
        else:
            return jsonify({
                "status": -1,
                'message': "no api!"
            })


welcome_route_api = {
    'create_user': apis.welcome_create_user,
}


@app.route('/api', methods=['POST'])
def api():
    print(request.json)
    if request.json.get('api'):
        if flask_login.current_user.is_authenticated:
            callback = access_route_management[flask_login.current_user.root_number].get(
                request.json.get('api'))
            if not callback:
                return jsonify({"status": -999, "message": "无权限执行该操作！"})
            return callback(request)
        else:
            callback = route_api_no_require_login.get(request.json.get('api'))
            if not callback:
                return jsonify({"status": -666, "message": "you have no access!"})
            return callback(request)

    return jsonify({"status": -1000, "message": "no api"})


route_api_no_require_login = {
    'login': apis.login,
    "check_login": apis.check_login,
    'ifUsed': apis.ifUsed,
}

route_api = {
    "server_info": apis.get_server_info,  # 服务器集群信息
    "server_check": apis.server_check,   # 检测服务器是否在线
    "server_add": apis.server_add,  # 绑定一个服务器
    "server_delete": apis.server_delete,  # 删除服务器
    "server_change_name": apis.server_change_name,  # 修改服务器名字
    "server_change_ssh": apis.server_change_ssh,  # 修改ssh ip
    "server_change_user": apis.server_change_user,  # 修改ssh用户名
    "server_change_psw": apis.server_change_psw,  # 修改ssh密码
    "server_one_info": apis.server_one_info,  # 获取一个服务器的详细信息
    'create_server': apis.server_add,  # 重复API
    "server_ssh_info": apis.server_ssh_info,  # 获取服务器ssh信息

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
    'system_use': apis.system_use,  # 获取系统docker资源用量
    'check_server_status': apis.check_server_status,  # 获取系统资源用量

    'login': apis.login,  # 登录
    "logout": apis.logout,  # 登出
    "check_login": apis.check_login,  # 检测登录状态
    'ifUsed': apis.ifUsed,  # 检测系统是否已经绑定服务器
    'psw_check': apis.psw_check,  # 获取系统密钥

    'user_info': apis.user_info,  # 获取用户信息
    'user_delete': apis.user_delete,  # 删除用户
    'create_user': apis.user_create,  # 创建新用户
    'search_user_by_name': apis.search_user_by_name,  # 搜索用户
    'change_user': apis.change_user,  # 修改用户信息
    "user_history_info": apis.user_history_info  # 获取用户登录记录
}

guest_route_api = {
    "server_info": apis.get_server_info,  # 服务器集群信息
    "server_check": apis.server_check,   # 检测服务器是否在线
    "server_one_info": apis.server_one_info,  # 获取一个服务器的详细信息
    "server_ssh_info": apis.server_ssh_info,  # 获取服务器ssh信息

    'container_info': apis.get_containers_info,  # 服务器的所有容器信息
    'container_inspect': apis.container_inpect,  # 获取一个容器的详细信息
    'container_process': apis.container_process,  # 容器的进程信息
    'container_log': apis.container_log,  # 容器的日志

    'image_info': apis.image_info,  # 服务器的所有镜像信息
    'image_inspect': apis.image_inspect,  # 获取一个镜像的详细信息

    'network_info': apis.server_network_info,  # 服务器docker的网卡信息
    'network_inspect': apis.network_inspect,  # 查看某个网卡的关键信息

    'volume_info': apis.volume_info,  # 查看服务器所有卷信息
    'volume_inspcet': apis.volume_inspcet,  # 查看某个卷的详细信息

    'system_infomation': apis.system_infomation,  # 获取系统信息
    'system_version': apis.system_version,  # 获取系统版本信息
    'system_use': apis.system_use,  # 获取系统docker资源用量
    'check_server_status': apis.check_server_status,  # 获取系统资源用量

    'login': apis.login,  # 登录
    "logout": apis.logout,  # 登出
    "check_login": apis.check_login,  # 检测登录状态
    'ifUsed': apis.ifUsed,  # 检测系统是否已经绑定服务器
    'psw_check': apis.psw_check,  # 获取系统密钥

    'user_info': apis.user_info,  # 获取用户信息
    'search_user_by_name': apis.search_user_by_name,  # 搜索用户
    "user_history_info": apis.user_history_info  # 获取用户登录记录
}


access_route_management = {
    '100': route_api,
    '0': route_api,
    '-1': guest_route_api
}
