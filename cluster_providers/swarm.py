from .base import ClusterProvider
from config import cfg
from utils import common

import docker
import click

from database import db
from tinydb import where


def insert_join_token(tokens):
    def transform(element):
        if 'docker' not in element:
            element['docker'] = {}

        element['docker']['join_tokens'] = tokens
        return element
    return transform


class SwarmClusterProvider(ClusterProvider):
    name = 'swarm'

    def __init__(self, vms):
        self.vms = vms

    def create_cluster(self):
        self.init = {}
        for vm in self.vms:
            docker_client = docker.DockerClient('tcp://' +
                                                common.translate_id(vm['id'])[0]
                                                + ':' + cfg.docker['API_PORT'])
            swarm_client = docker_client.swarm
            if vm['role'] == 'manager':
                swarm_client.init('eth0:' + cfg.docker['SWARM_PORT'],
                                  '0.0.0.0:' + cfg.docker['SWARM_PORT'])
                db.vms.update(
                              insert_join_token(
                                  swarm_client.attrs['JoinTokens']
                                  ),
                              where('name') == vm['id'])

                self.vms.remove(vm)
                self.init = vm
                break

        for vm in self.vms:
            if vm['role'] == 'manager':
                self.add_manager(vm)
            elif vm['role'] == 'worker':
                self.add_worker(vm)

    def add_manager(self, vm):
            docker_client = docker.DockerClient('tcp://' +
                                                common.translate_id(vm['id'])
                                                + ':' + cfg.docker['API_PORT'])
            swarm_client = docker_client.swarm
            manager = db.vms.get(where('name') == self.init['id'])
            swarm_client.join(
                    [common.id_to_swarm(self.init['id'])],
                    manager['docker']['join_tokens']['Manager'],
                    '0.0.0.0:' + cfg.docker['SWARM_PORT']
                    )

    def add_worker(self, vm):
            docker_client = docker.DockerClient('tcp://' +
                                                common.translate_id(vm['id'])
                                                + ':' + cfg.docker['API_PORT'])
            swarm_client = docker_client.swarm
            manager = db.vms.get(where('name') == self.init['id'])
            swarm_client.join(
                    [common.id_to_swarm(self.init['id'])],
                    manager['docker']['join_tokens']['Worker'],
                    '0.0.0.0:' + cfg.docker['SWARM_PORT']
                    )
