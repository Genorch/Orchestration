#!/usr/bin/env python3

from ..base import ServiceProvider
from config import cfg
from utils import  common

from database import db
from tinydb import where

import docker


def insert_join_token(tokens):
    def transform(element):
        if 'docker' not in element:
            element['docker'] = {}

        element['docker']['join_tokens'] = tokens
        return element
    return transform


class Docker(ServiceProvider):
    name = "docker"

    def __init__(self, targets):
        self.targets = targets

    def create_service(self, opts):
        for target in self.targets:
            docker_client = docker.DockerClient('tcp://' + common.translate_id(target)[0] +
                                                ':' + cfg.docker['API_PORT'])
            if "sub_driver" in opts:
                sub_driver_name = opts['sub_driver']
                sub_driver = getattr(docker_client, sub_driver_name)

                del opts['sub_driver']

                if sub_driver_name == 'swarm':
                    sub_driver_opts = opts['opts']
                    node_type = sub_driver_opts['type']

                    if node_type == 'manager':
                        sub_driver.init('eth0:' + cfg.docker['SWARM_PORT'], '0.0.0.0:' + cfg.docker['SWARM_PORT'])
                        print(sub_driver.attrs['JoinTokens'])
                        db.vms.update(insert_join_token(sub_driver.attrs['JoinTokens']), where('name') == target)
                    elif node_type == 'worker':
                        manager = db.vms.get(where('name') == sub_driver_opts['managers'][0])
                        sub_driver.join([common.id_to_swarm(sub_driver_opts['managers'][0])], manager['docker']['join_tokens']['Worker'], '0.0.0.0:' + cfg.docker['SWARM_PORT'])

            else:
                docker_client.containers.run(**opts, detach=True)

