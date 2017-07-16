#!/usr/bin/env python3

from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory import Inventory
from ansible.vars import VariableManager
from ansible.parsing.dataloader import DataLoader

from .options import Options
from config import cfg


class Ansible:

    def __init__(self):

        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.passwords = {}
        self.options = Options()
        self.options.become_method = cfg.BECOME_METHOD
        self.options.become_user = cfg.BECOME_USER
        self.options.become = True
        self.options.private_key_file = cfg.PRIVATE_SSH_KEY
        self.options.connection = cfg.CONNECTION

        self.passwords = {'become_pass': cfg.BECOME_PASS}

    def create_service(self, playbooks, hostslist=['localhost']):

        inventory = Inventory(
            loader=self.loader,
            variable_manager=self.variable_manager,
            host_list=hostslist
        )

        self.options.listhosts = hostslist
        self.variable_manager.set_inventory(inventory)

        pbex = PlaybookExecutor(
                playbooks=playbooks,
                inventory=inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords
                )
        pbex.run()
