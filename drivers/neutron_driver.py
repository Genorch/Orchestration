import json
import httplib
from KeystoneDriver import KeystoneClient


class NeutronClient(object):

    def __init__(self, keystone_host, keystone_port=5000):
        self.keyClient = KeystoneClient(keystone_host, keystone_port)

    def list_networks(self, token, region, tenant):
        return self._send_request(
                tenant, token, region, "GET", "/v2.0/networks"
                )

    def show_network(self, token, region, tenant, network_id):
        return self._send_request(
                tenant, token, region, "GET", "/v2.0/networks/" + network_id
                )

    def show_subnet(self, token, region, tenant, subnet_id):
        return self._send_request(
                tenant, token, region, "GET", "/v2.0/subnets/" + subnet_id
                )

    def list_ports(self, token, region, tenant):
        return self._send_request(tenant, token, region, "GET", "/v2.0/ports")

    def get_network_id(self, token, region, tenant):
        networks = json.loads(
                self.list_networks(token, region, tenant)
                )['networks']
        for network in networks:
            if network['name'] == tenant+"-net":
                return network['id']

    def get_gateway(self, token, region, tenant):
        networks = json.loads(
                self.list_networks(token, region, tenant)
                )['networks']
        for network in networks:
            if network['name'] == tenant+"-net":
                subnet_id = network['subnets'][0]
                ip = json.loads(
                        self.show_subnet(token, region, tenant, subnet_id)
                        )['subnet']['gateway_ip']
                ports = json.loads(
                        self.list_ports(token, region, tenant)
                        )['ports']
                for port in ports:
                    if port['fixed_ips'][0]["ip_address"] == ip:
                        mac = port["mac_address"]
                        return dict(ip=ip, mac=mac)

    def _send_request(self, tenant, token, region, method, url):

        resp = self.keyClient.get_tokens_by_token(tenant, token)
        auth_token = resp['access']['token']['id']
        project = tenant
        headers = {'X-Auth-Project-Id': project, 'X-Auth-Token': auth_token}
        for service in resp['access']['serviceCatalog']:
            if service['name'] == "quantum":
                for endpoint in service['endpoints']:
                    if endpoint['region'] == region:
                        parts = endpoint['publicURL'].split(':')
                        host = parts[1].split('/')[2]
                        port = int(parts[2].partition("/")[0])
                        conn = httplib.HTTPConnection(host, port)
                        conn.request(method, url, None, headers)
                        res = conn.getresponse()
                        if res.status in (httplib.OK,
                                          httplib.CREATED,
                                          httplib.ACCEPTED,
                                          httplib.NO_CONTENT):
                            return res.read()
                        raise httplib.HTTPException(
                            res, 'Return status: %d; Reason: %s'
                            % (res.status, res.reason),
                            res.getheaders(), res.read())
