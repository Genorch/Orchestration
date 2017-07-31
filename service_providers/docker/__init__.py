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
            docker_client = docker.DockerClient("tcp://" + target +
                                                ":" + cfg.docker['API_PORT'])
            if "sub_driver" in opts:
                sub_driver_name = opts['sub_driver']
                sub_driver = getattr(sub_driver_name, docker_client)

                del opts['sub_driver']

                if sub_driver_name == "swarm":
                    if opts['manager']:
                        sub_driver.init(listen_addr='0.0.0.0:5000')
                    else:
                        sub_driver.init(listen_addr='0.0.0.0:5000')
            else:
                docker_client.containers.run(**opts, detach=True)

