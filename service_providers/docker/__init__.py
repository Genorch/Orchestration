#!/usr/bin/env python3

from ..base import ServiceProvider
from config import cfg

import docker


class Docker(ServiceProvider):

    def __init__(self):
        self.client = docker.Client(cfg['docker']['base_url'])

