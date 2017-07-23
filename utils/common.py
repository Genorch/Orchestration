from database import db
from tinydb import where


def translate_id(id):
    ips = []
    network_interfaces = db.vms.search(where('name') == id)[0]['ips']
    for nic in network_interfaces:
        ips.append(network_interfaces[nic][0]['addr'])

    return ips
