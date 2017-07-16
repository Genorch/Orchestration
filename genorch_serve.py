#!/usr/bin/env python3

import yaml
import click

from domain.server import Server
from domain.service import Service


@click.command()
@click.option('--load', prompt='YAML file',
              help='Target yaml file to parse')
def parse(load):
    with open(load) as stream:
        m = yaml.load(stream)
        for provider in m['project']['topology']['provider']:
            for region in provider['region']:
                for vm in region['vm']:
                    click.secho('virtual machine => provider: %s, region: %s' %
                                (provider['name'], region['name']),
                                fg="green")
                    Server(vm['id'], vm['image'], vm['flavor'],
                           region['name'], provider['name'],
                           vm['networks'], vm.get('key', None)).create()

        for service in m['project']['service']:
            click.secho('service => playbook: %s, type: %s' %
                        (service['playbook'], service['type']),
                        fg="red")
            Service(service['playbook'], service['targets']).create()


if __name__ == '__main__':
    parse()
