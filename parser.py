#!/usr/bin/env python3

import yaml
import click

@click.command()
@click.option('--load', prompt='YAML file',
              help='Target yaml file to parse')
def parse(load):
    with open(load) as stream:
        m = yaml.load(stream)
        click.echo_via_pager(m)

if __name__ == '__main__':
    parse()
