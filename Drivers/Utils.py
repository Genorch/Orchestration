import httplib
import traceback


class Utils(object):

    @staticmethod
    def http_call(host, port, method, url, header, body=None):

        res = None
        try:
            _conn = httplib.HTTPConnection(host, port)
            header['Content-Type'] = "application/json"
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
