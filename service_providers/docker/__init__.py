#!/usr/bin/env python3

from ..base import ServiceProvider
from config import cfg

from docker import Client


class Docker(ServiceProvider):
    name = "docker"

    def __init__(self, targets):
        self.targets = targets

    def create_service(self, opts):
        for target in self.targets:
            client = Client(target + ":2379")
            client.containers.run(**opts, detach=True)
