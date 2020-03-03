from app import app
from flask import url_for, request, redirect, render_template,jsonify,current_app,make_response


from . import apis



@app.route('/web/api',methods=['POST'])
def api():
    if request.json.get('api'):
        callback = route_api.get(request.json.get('api'))
        return callback(request)

    return jsonify({"ststus":0,"message":"no api"})

route_api = {

}

