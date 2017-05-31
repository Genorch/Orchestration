#!/usr/bin/env python

import os

from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play_context import PlayContext
from ansible.executor.playbook_executor import PlaybookExecutor


from callback import ResultCallback

Options = namedtuple('Options', ['connection', 'forks', 'become', 'become_method', 'become_user', 'check', 'listhosts', 'syntax'])
# initialize needed objects
variable_manager = VariableManager()
loader = DataLoader()
options = Options(connection='local', forks=100, become=None, become_method=None, become_user=None, check=False, listhosts=True, syntax=False)
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
    pbex = PlaybookExecutor(
            playbooks=["playbooks/apache.yml"],
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=passwords
            )

    results = pbex.run()
    for p in results:

        for idx, play in enumerate(p['plays']):
            if play._included_path is not None:
                loader.set_basedir(play._included_path)
            else:
                pb_dir = os.path.realpath(os.path.dirname(p['playbook']))
                loader.set_basedir(pb_dir)
                msg = "\n  play #%d (%s): %s" % (idx + 1, ','.join(play.hosts), play.name)
                mytags = set(play.tags)
                msg += '\tTAGS: [%s]' % (','.join(mytags))

                if options.listhosts:
                    playhosts = set(inventory.get_hosts(play.hosts))
                    msg += "\n    pattern: %s\n    hosts (%d):" % (play.hosts, len(playhosts))
                    for host in playhosts:
                        msg += "\n      %s" % host

                print(msg)


finally:
    if tqm is not None:
        tqm.cleanup()
