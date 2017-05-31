import json

from . import Runner


class AnsibleDriver:

    def __init__(self):
        ansible_cfg = json.load(open('config/ansible.json'))
        self.private_key = ansible_cfg['PRIVATE_SSH_KEY']
        self.become_pass = ansible_cfg['BECOME_USER_PASS']

    def run_service(self, playbook):
        runner = Runner(
                hostnames='localhost',
                playbook='playbooks/apache.yml',
                private_key=self.private_key,
                become_pass=self.become_pass,
                verbosity=0
                )
        stats = runner.run()
        print(stats)

