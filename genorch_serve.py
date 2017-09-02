#!/usr/bin/env python3

import yaml
import click
from jinja2 import Environment, FileSystemLoader
import os

from domain.server import Server
from domain.service import Service
from domain.cluster import Cluster
from utils.common import translate_id, id_to_swarm

from database import db
from tinydb import where
from config import cfg


@click.group()
@click.version_option('0.0.1')
def cli():
    pass


@cli.command()
@click.option('--load', prompt='YAML file',
              help='Target yaml file to parse')
def parse(load):
    if os.environ.get('ANSIBLE_CONFIG') is None:
        os.environ['ANSIBLE_CONFIG'] = cfg.ansible['ANSIBLE_CONFIG']

    click.secho('ansible.cfg location: %s' % os.environ.get('ANSIBLE_CONFIG'),
                fg='yellow')
    env = Environment(
        loader=FileSystemLoader('./')
    )
    env.globals.update(translate_id=translate_id, id_to_swarm=id_to_swarm)

    m = env.get_template(load).render()

    m = yaml.load(m)
    for provider in m['project']['topology']['provider']:
        for region in provider['region']:
            for vm in region['vms']:
                click.secho('virtual machine => provider: %s, region: %s' %
                            (provider['name'], region['name']),
                            fg="green")

                servers = db.vms.search(where('name') == vm['id'])

                if len(servers) == 0:
                    Server(vm['id'], vm['image'], vm['flavor'],
                           region['name'], provider['name'],
                           vm['networks'], vm.get('key', None)).create()
                    if 'config' in vm:
                        Service(
                            vm['config']['provider'],
                            [vm['id']],
                            vm['config']['opts']).create()

    if 'services' in m['project']:
        for service in m['project']['services']:
            click.secho('service => provider: %s, type: %s' %
                        (service['provider'], service['type']),
                        fg="blue")
            Service(
                    service['provider'],
                    service['targets'],
                    service['opts']).create()

    if 'clusters' in m['project']:
        for cluster in m['project']['clusters']:
            Cluster(
                    cluster['id'], cluster['vms'], cluster['provider']
                    ).create()
            click.secho('cluster => provider: %s, id: %s' %
                        (cluster['provider'], cluster['id']),
                        fg="blue")


@cli.command()
def truncate():
    Server.truncate()
