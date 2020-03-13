import requests
import json
from app.models import Certification

def send_request(r_type, server_ip, data_dict):
    print('%s://%s/server/api' % (r_type, server_ip))

    get_c = Certification.query.first()
    if get_c:
        data_dict["psw"] = get_c.id

    get_return = requests.post('%s://%s/server/api' %
                               (r_type, server_ip), json=data_dict)
    return2json = json.loads(get_return.text)
    return return2json



def send_request_server_bind(r_type, server_ip, data_dict):
    get_c = Certification.query.first()
    if get_c:
        data_dict["psw"] = get_c.id
    
    get_return = requests.post('%s://%s/server/bind' %
                               (r_type, server_ip), json=data_dict)
    return2json = json.loads(get_return.text)
    return return2json


def send_request_server_delete(r_type, server_ip, data_dict):
    get_c = Certification.query.first()
    if get_c:
        data_dict["psw"] = get_c.id
    
    get_return = requests.post('%s://%s/server/delete' %
                               (r_type, server_ip), json=data_dict)
    return2json = json.loads(get_return.text)
    return return2json