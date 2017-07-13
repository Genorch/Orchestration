#!/usr/bin/env python

from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory import Inventory
from ansible.vars import VariableManager
from ansible.parsing.dataloader import DataLoader


class Ansible:

    def __init__(self):

        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.passwords = {}
        self.inventory = Inventory(
                loader=self.loader,
                variable_manager=self.variable_manager,
                host_list=self.options.inventory
                )

        self.variable_manager.set_inventory(self.inventory)

    def execute(self):
        pbex = PlaybookExecutor(
                playbooks=['playbooks/apache.yml'],
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options="", passwords=self.passwords
                )
        pbex.run()
