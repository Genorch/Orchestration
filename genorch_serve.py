#!/usr/bin/env python3

import yaml
import click

from domain.server import Server


@click.command()
@click.option('--load', prompt='YAML file',
              help='Target yaml file to parse')
def parse(load):
    with open(load) as stream:
        m = yaml.load(stream)
        for vm in m['project']['vm']:
            provider = m['project']['provider'][vm['provider']]

            click.secho('boot vm at %s in %s' % (vm['provider'],
                                                 provider['region']),
                        fg="green")

            Server(vm['id'], vm['class'], provider['class']).create()


if __name__ == '__main__':
    parse()
