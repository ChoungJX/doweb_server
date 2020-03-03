from flask import Flask,request,jsonify
#from flask_cors import *
import uuid
import random
import time

app = Flask(__name__)
#CORS(app, supports_credentials=True)
#CORS(app, resources=r'/*')



@app.route("/login",methods=["POST"])
def login():
    uuu="123"
    psw="123"

    get_username = request.json.get("username")
    get_password = request.json.get("password")

    if get_username==uuu and get_password==psw:
        return jsonify(
            {
                'status':0
            }
        )
    else:
        return jsonify(
            {
                'status':-1
            }
        )



data1 = list()
for i in range(255):
    data1.append(
        {
            "ip":"172.18.2.%s"%(i),
            "name":"xxx",
            "status":'在线',
            "id":str(uuid.uuid4()),
        },
    )


@app.route("/api",methods=["POST"])
def aaa():
    time.sleep(1)
    print(request.json)
    method = request.json.get("api")

    if method == "server_info":
        page = request.json.get("page_current") - 1
        need_number = request.json.get("need")

        start = page*need_number

        data = data1[start:start+need_number]
        return jsonify(
            {
                "total":len(data1),
                "data":data
            }
        )
    elif method == "server_delete":
        get_id = request.json.get("id")
        for i in range(len(data1)):
            if data1[i]["id"] == get_id:
                del data1[i]
                break
        
        return jsonify(
            {
                "status":0,
            }
        )
    
    elif method == "server_renew":
        get_id = request.json.get("id")
        get_name = request.json.get('name')

        for i in range(len(data1)):
            if data1[i]["id"] == get_id:
                data1[i]["name"] = get_name
        
        return jsonify(
            {
                "status":0,
            }
        )
    elif method == "server_add":
        get_ip = request.json.get("ip")
        get_name = request.json.get("name")
        get_uuid = str(uuid.uuid4())
        data1.append(
            {
            "ip":get_ip,
            "name":get_name,
            "status":'在线',
            "id":get_uuid,
        },
        )
        return jsonify(
            {
                "status":0,
                "uuid":get_uuid,
            }
        )
    
    elif method == "login":
        uuu="123"
        psw="123"

        get_username = request.json.get("username")
        get_password = request.json.get("password")

        if get_username==uuu and get_password==psw:
            return jsonify(
                {
                    'status':0
                }
            )
        else:
            return jsonify(
                {
                    'status':-1
                }
            )

app.run(host="0.0.0.0",port=4000,debug=True)
