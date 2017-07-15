#!/usr/bin/env python3

import yaml
import click

from domain.server import Server
from service_providers.ansible_driver import Ansible


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
                           vm['networks']).create()


@click.command()
def ansible():
    ansible = Ansible()
    ansible.execute([
        '/home/iman/Documents/Git/Orchestration' +
        '/service_providers/ansible_driver/playbooks/apache.yml']
        )


if __name__ == '__main__':
    ansible()
