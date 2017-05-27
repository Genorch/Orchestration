import json

from ansible.playbook import PlayBook


class AnsibleDriver:
    def __init__(self):
        pass

    def setup(self, playbook):
        ansible_cfg = json.load(open('../config/ansible.json'))
        pb = PlayBook(
                playbook='ansible/playbooks/%s.yml' % playbook,
                host_list=[],
                remote_user=ansible_cfg['REMOTE_USER'],
                private_key_file=ansible_cfg['PRIVATE_KEY']
        )
        results = pb.run()
        return results
