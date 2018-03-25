#!/usr/bin/env python3

from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.parsing.dataloader import DataLoader

import os

from .options import Options
from ..base import ServiceProvider
from config import cfg
from utils import common



class Ansible(ServiceProvider):
    name = "ansible"

    def __init__(self, targets):

        ansible_cfg = cfg['ansible']

        self.loader = DataLoader()
        self.passwords = {}
        self.options = Options()
        self.options.become_method = ansible_cfg['BECOME_METHOD']
        self.options.become_user = ansible_cfg['BECOME_USER']
        self.options.become = True
        self.options.private_key_file = ansible_cfg['PRIVATE_SSH_KEY']
        self.options.connection = ansible_cfg['CONNECTION']
        self.options.forks = 1

        ips = []
        for target in targets:
            ips.extend(common.translate_id(target))

        ips.append('')
        self.inventory = InventoryManager(
                loader=self.loader,
                sources=','.join(ips)
                )
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.passwords = {'become_pass': ansible_cfg['BECOME_PASS']}


        self.options.hostlist = ips

    def create_service(self, opts):
        os.environ['ANSIBLE_CONFIG'] = cfg.ansible['ANSIBLE_CONFIG']
        if 'vars' in opts:
            self.variable_manager.extra_vars = opts['vars']
        else:
            self.options.extra_vars = None
            self.variable_manager.extra_vars = {}
        pbex = ''
        if opts['playbook'].startswith('/'):
            pbex = PlaybookExecutor(
                    playbooks=[opts['playbook']],
                    inventory=self.inventory,
                    variable_manager=self.variable_manager,
                    loader=self.loader,
                    options=self.options,
                    passwords=self.passwords
                    )
        else:
            pbex = PlaybookExecutor(
                    playbooks=['service_providers/ansible/playbooks/' +
                               opts['playbook']],
                    inventory=self.inventory,
                    variable_manager=self.variable_manager,
                    loader=self.loader,
                    options=self.options,
                    passwords=self.passwords
                    )
        pbex.run()
