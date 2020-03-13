import requests
import json


def send_request(r_type, server_ip, data_dict):
    print('%s://%s/server/api' % (r_type, server_ip))

    get_return = requests.post('%s://%s/server/api' %
                               (r_type, server_ip), json=data_dict)
    return2json = json.loads(get_return.text)
    return return2json
