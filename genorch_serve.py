#!/usr/bin/env python3

import yaml
import click

from domain.server import Server
from domain.service import Service

from database import db
from tinydb import where

@click.group()
@click.version_option('0.0.1')
def cli():
    pass

@cli.command()
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

                    servers = db.vms.search(where('name') == vm['id'])

                    if len(servers) == 0:
                        Server(vm['id'], vm['image'], vm['flavor'],
                               region['name'], provider['name'],
                               vm['networks'], vm.get('key', None)).create()

        for service in m['project']['service']:
            click.secho('service => playbook: %s, type: %s' %
                        (service['playbook'], service['type']),
                        fg="red")
            Service(service['playbook'], service['targets']).create()





