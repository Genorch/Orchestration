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
                sub_driver = getattr(sub_driver_name, docker_client)

                del opts['sub_driver']

                if sub_driver_name == 'swarm':
                    sub_driver_opts = opts['sub_driver']['opts']
                    node_type = sub_driver_opts['type']

                    del sub_driver_opts['sub_driver']

                    if node_type == 'manager':
                        sub_driver.init('0.0.0.0:' + cfg.docker['SWARM_PORT'])
                        db.vms.update(insert_join_token(sub_driver.attrs['JoinTokens']), where('name') == target)

            else:
                docker_client.containers.run(**opts, detach=True)

