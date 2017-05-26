from ansible.playbook import PlayBook


class AnsibleDriver:
    def __init__(self, _class):
        self.pb = PlayBook(
                playbook='ansible/playbooks/%s.yml' % _class,
                host_list=[],
                remote_user='ubuntu',
                private_key_file='/path/to/key.pem'
        )

    def setup(self):
        results = self.pb.run()
        return results
