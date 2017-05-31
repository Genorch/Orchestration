#!/usr/bin/env python

from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play_context import PlayContext
from ansible.executor.playbook_executor import PlaybookExecutor


from callback import ResultCallback

Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'listhosts', 'syntax'])
# initialize needed objects
variable_manager = VariableManager()
loader = DataLoader()
options = Options(connection='local', module_path='/path/to/mymodules', forks=100, become=None, become_method=None, become_user=None, check=False, listhosts=True, syntax=False)
passwords = dict(vault_pass='secret')

# Instantiate our ResultCallback for handling results as they come in
results_callback = ResultCallback()

# create inventory and pass to var manager
inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list='localhost')
variable_manager.set_inventory(inventory)

# create play with tasks

# actually run it
tqm = None
try:
    pbex = PlaybookExecutor(playbooks=["playbooks/apache.yml"], inventory=inventory, variable_manager=variable_manager, loader=loader, options=options, passwords=passwords)

    results = pbex.run()

finally:
    if tqm is not None:
        tqm.cleanup()
