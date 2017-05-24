import httplib
from KeystoneDriver import KeystoneClient


class NovaClient(object):
    def __init__(self, keystone_host, keystone_port=5000):
        self.keyClient = KeystoneClient(keystone_host, keystone_port)

    def get_vms(self, token, region, tenant):
        return self._send_request(
                tenant, token, region, "GET",
                "/servers/detail"
                )

    def _send_request(self, tenant, token, region, method, url):
        resp = self.keyClient.get_tokens_by_token(tenant, token)
        auth_token = resp['access']['token']['id']
        project = tenant
        headers = {'X-Auth-Project-Id': project,
                   'X-Auth-Token': auth_token}
        for service in resp['access']['serviceCatalog']:
            if service['name'] == "nova":
                for endpoint in service['endpoints']:
                    if endpoint['region'] == region:
                        parts = endpoint['publicURL'].split(':')
                        i_url = "/" + parts[2].partition("/")[2] + url
                        host = parts[1].split('/')[2]
                        port = int(parts[2].partition("/")[0])
                        conn = httplib.HTTPConnection(host, port)
                        conn.request(method, i_url, None, headers)
                        res = conn.getresponse()
                        if res.status in (httplib.OK,
                                          httplib.CREATED,
                                          httplib.ACCEPTED,
                                          httplib.NO_CONTENT):
                            return res.read()
                        raise httplib.HTTPException(
                            res, 'Return status: %d; Reason: %s' %
                            (res.status, res.reason),
                            res.getheaders(), res.read())
