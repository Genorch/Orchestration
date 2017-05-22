import json
from Utils import Utils


class KeystoneClient(object):
    def __init__(self, keystone_host, keystone_port=5000):
        self.host = keystone_host
        self.port = keystone_port

    def get_tokens_by_token(self, tenant, token):
        body = '{"auth": {"tenantName":"' + tenant + '",  "token": {"id":"' + token + '"}}}'
        ret = Utils.http_call(self.host, self.port, 'POST', '/v2.0/tokens', {}, body)
        return json.loads(ret)

    def get_tokens_by_username(self, tenant, username, password):
        body = '{"auth": {"passwordCredentials": {"username": "' + username + '", "password": "' + password + '"}}}'
        ret = Utils.http_call(self.host, self.port, 'POST', '/v2.0/tokens', {}, body)
        return json.loads(ret)