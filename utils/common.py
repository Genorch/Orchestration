from database import db
from tinydb import where
from config import cfg


def translate_id(id):
    ips = []
    network_interfaces = db.vms.search(where('name') == id)[0]['ips']
    for nic in network_interfaces:
        ips.append(network_interfaces[nic][0]['addr'])

    return ips


def id_to_swarm(id):
    ip = translate_id(id)[0]
    return ip + ':' + cfg.docker['SWARM_PORT']

