#!/usr/bin/env python3

import yaml
import click

from domain.server import Server


@click.command()
@click.option('--load', prompt='YAML file',
              help='Target yaml file to parse')
def parse(load):
    with open(load) as stream:
        model = yaml.load(stream)
        for server in model['project']['service']:
            Server(server['id'], server['class'], 'openstack').create()


if __name__ == '__main__':
    parse()
