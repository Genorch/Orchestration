import json


class KeystoneClient(object):

    def __init__(self, KeystoneHost, KeystonePort=5000):
        self.host = KeystoneHost
        self.port = KeystonePort

    def getTokensbyToken(self, tenant, token):
        ret = self._HTTPCall(self.host, self.port, 'POST', '/v2.0/tokens', {},
                             '{"auth": {"tenantName":"'+tenant+'",  "token": {"id":"'+token+'"}}}')
        return json.loads(ret)

    def getTokensbyUsername(self, tenant, username, password):
        ret = self._HTTPCall(self.host, self.port, 'POST', '/v2.0/tokens', {},
                             '{"auth": {"passwordCredentials": {"username": "'+
                             username+
                             '", "password": "'+password+'"}}}')
        return json.loads(ret)

