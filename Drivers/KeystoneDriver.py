import json
import httplib
import traceback

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

    def _HTTPCall(self, host, port, method, url, header, body=None):

        res = None
        try:
            _conn = httplib.HTTPConnection(host, port)
            header['Content-Type']= "application/json"
            _conn.request(method, url, body=body, headers=header)
            res = _conn.getresponse()
            ret = res.read()
        except:
            traceback.print_exc()
            pass
        if res.status in (httplib.OK,
                          httplib.CREATED,
                          httplib.ACCEPTED,
                          httplib.NO_CONTENT):
            return ret

        raise httplib.HTTPException(
            res, 'code %d reason %s' % (res.status, res.reason),
            res.getheaders(), res.read())