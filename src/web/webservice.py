import re
import httplib


class WebService:

    def __init__(self):
        pass

    @staticmethod
    def json_post(url, data):
        domain = re.findall(".*?(?=/)", "url")[0]
        hdr = {"content-type": "application/json"}
        conn = httplib.HTTPConnection(domain)
        conn.request('POST', url.replace(domain, ""), data, hdr)
        response = conn.getresponse()
        return response.read()
