#!/usr/bin/env python3

from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory import Inventory
from ansible.vars import VariableManager
from ansible.parsing.dataloader import DataLoader

from .options import Options


class Ansible:

    def __init__(self):

        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.passwords = {}
        self.options = Options()
        self.options.verbosity = 5
        self.options.become_method = 'sudo'
        self.options.become_user = 'root'
        self.options.become = True
        self.options.private_key_file = '/home/iman/.ssh/id_rsa'
        self.options.connection = 'ssh'

        self.inventory = Inventory(
                loader=self.loader,
                variable_manager=self.variable_manager,
                host_list=['localhost']
                )

        self.options.hostlist = ['localhost']
        self.variable_manager.set_inventory(self.inventory)

    def execute(self):
        playbook = '/home/iman/Documents/Git/Orchestration/service_providers/ansible_driver/playbooks/apache.yml'
        pbex = PlaybookExecutor(
                playbooks=[playbook],
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords
                )
        pbex.run()
