#!/usr/bin/env python3

from ..base import ServiceProvider
from config import cfg

import docker


class Docker(ServiceProvider):
    name = "docker"

    def __init__(self, targets):
        self.targets = targets

    def create_service(self, opts):
        for target in self.targets:
            docker_client = docker.DockerClient(target + ":2379")
            docker_client.containers.run(**opts, detach=True)
